#!/usr/bin/python


# The following section is neccesary in order for DocOpt command line argument parsing module to operate
# Do not change the following syntax unless you are familiar with DocOpt specifications.
"""Resume Ranker reviews resumes and assigns a score based on percentile matching file content.  Valid
file types include .docx, .pdf, and .txt. Any other filetype will be skipped automatically.

	Usage:
		ranker.py [-h | --help]
		ranker.py [-v | --verbose] [--rename=<rename>] --dir=<dir> --keyword-file=<keywordfile> [--output-type=<outputtype> --output-file=<outputfile>]
		ranker.py --version

	Options:
		-h,--help	: show this help message.
		-v,--verbose    : display more text output.
		--rename : explicitly turn on/off the file renamer with yes/no option [default: yes].
		--dir	: set the directory for resume review.
		--keyword-file	: set the file path of the keyword file used in ranking each resume file contents.
		--output-type	: set the output file type (csv or txt).  Must be used in conjunction with --output-file.
		--output-file	: set the directory and filename of the output file, including extension. Must be used in conjunction with --output-type.
		--version	: show version.
"""

__scriptname__	= "Resume Ranker"
__author__ 		= "Corey Farmer"
__copyright__ 	= "Copyright 2017"
__credits__ 	= []
__license__ 	= "GPL"
__version__ 	= "1.0.0"
__maintainer__ 	= "Corey Farmer"
__email__ 		= "corey.m.farmer@gmail.com"
__status__ 		= "Development"


import os, PyPDF2, csv

from docopt import docopt
from os import sys, path


from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph


class Environment:
	"""
	Setup the environment for the script; including opening any required files, checking
	validity of files and directories, etc.
	
	--
	:param string|None dir		- string containing the directory for iteration containing files
	:param string keyword_file	- string containing full file path to location of keyword file
	:return Object Environment
	"""
	
	def __init__(self, dir=None, keyword_file=None):
		self.dir 			= dir
		self.keyword_file	= keyword_file
		
	def is_directory_given(self):
		# check if the user provided a directory to iterate through
		if not self.dir :
			raise Exception("A directory must be provided.  See --help option for script usage details.")

		return self
		
	def is_valid_directory(self):
		# check if the directory provided by the user for files exists
		if dir and not os.path.isdir(self.dir) :
			raise Exception("The directory provided is not valid or found.")
		
		return self
	
	def is_valid_keyword_file(self):
		# check if the file provided by the user for keywords exists
		if not os.path.isfile(self.keyword_file):
			raise Exception("The keyword file path provided is not valid or does not exist.")

		return self
	
	
		
class Parsing:
	"""
	This class is designed to contain all necessary file parsing methodologies.
	Each file passed as object instantiation parameter will be parsed into plain text 
	form and provided back to calling function.
	
	--
	:param string path		- string containing the full file path of the file to open and parse into variable text
	:return Object Parsing
	"""
	def __init__(self, path):
		self.file 	 = path
		self.results = self.parse_file()
	
	
	def parse_file(self) :
		"""
		Check the file extension against known/valid extensions and call
		associated parsing method appropriately.
		"""		

		# get the file extension from the filename
		extension = os.path.splitext(self.file)[1]
		# create an empty string variable 
		results = None
		# if the file passed in is a valid file
		if os.path.isfile(self.file) :
			# figure out extension to determine what parsing methodology to use
			
			d = { '.docx'	: self.parse_word_doc
				 ,'.pdf' 	: self.parse_pdf_doc
				 ,'.txt'	: self.parse_txt_doc
			}			
			
			# invoke the value of the dict returned by extension key match
			results = d[extension]()
		
		return results
	
	def parse_word_doc(self):
		"""
		Open a word document filetype and parse contents to string variable
		for matching comparison.
		"""
		
				
		def iter_block_items(parent):
			"""
			Generate a reference to each paragraph and table child within *parent*,
			in document order. Each returned value is an instance of either Table or
			Paragraph. *parent* would most commonly be a reference to a main
			Document object, but also works for a _Cell object, which itself can
			contain paragraphs and tables.
			"""
			if isinstance(parent, _Document):
				parent_elm = parent.element.body
			elif isinstance(parent, _Cell):
				parent_elm = parent._tc
			
			for child in parent_elm.iterchildren():
				if isinstance(child, CT_P):
					yield Paragraph(child, parent)
				elif isinstance(child, CT_Tbl):
					yield Table(child, parent)
		
		# create empty string variable for storing file content
		docText	 = ''
		# set the document object with the file
		document = Document(self.file)

		# iterate over blocks in the document object
		for block in iter_block_items(document) :
			# if block type is paragraph, simply grab text from paragraph
			if isinstance(block, Paragraph) :
				# append block text to text variable 
				docText += block.text
			
			# if block type is table, we must iterate over the table components to get
			# content out of the cells
			elif isinstance(block, Table) :
				# iterate over the rows inside the table
				for row in block.rows :
					# iterate over each cell inside each row
					for cell in row.cells :
						# append cell text to text variable
						docText += cell.text
						
		return docText.strip() or None
	

	def parse_pdf_doc(self):
		"""
		Open a pdf document filetype and parse contents to string variable
		for matching comparison.
		"""
		
		docText = ''
		# open the file, with read/binary priviledges
		f = open(self.file, 'rb')
		pdf = PyPDF2.PdfFileReader(f)
		for page in pdf.pages :
			docText += page.extractText()
		
		f.close()
		return docText.strip() or None

	def parse_txt_doc(self):
		"""
		Open a text document filetype and parse contents to string variable
		for matching comparison.
		"""
		
		# open the file, with read priviledges
		with open(self.file, 'r') as f :
			docText = f.read()
		
		return docText.strip() or None
	


class Rank :
	"""
	Use this function to determine the appropriate ranking/score of each file.
	When instantiated, this class will first load the keywords file
	
	--
	:param list keyword_list	- list containing each keyword found in keyword_file
	:return Object Rank
	"""
	
	def __init__(self, keyword_list):
		self.keywords	= keyword_list		
		self.total_keys = len(self.keywords)
	
	def get_rank(self, text):
		"""
		Get the rank of the file based on total count of keywords found in the file
		contents.
		"""
		# set the initial rank and count to 0
		rank = count = 0
		
		# get the percentage that each keyword is worth
		word_percentage = round(float(100)/float(len(self.keywords)), 2)
		# iterate over list of keywords	
		for keyword in self.keywords :
			keyword, multiplier = self.get_multiplier(keyword)
			
			# was the keyword found in the file? increase overall percentage if true
			rank += word_percentage if keyword.upper() in text.upper() else 0
			
			# get the number of occurrences of the keyword in the file
			count +=  text.upper().count( keyword.upper() ) * int( multiplier )
						
		return (rank,count)
			
	
	def get_multiplier(self, keyword):
		"""
		Split the keyword on multiplier delimiter if found. Otherwise provide 1 for multiplier
		"""
		
		multiplier 	= 1 
		# set the multiplier if found in the file
		if ' *' in keyword :
			keyword,multiplier = keyword.split(' *')
		
		return (keyword, multiplier)
		
		



class File :
	"""
	Use this method to hold any method related to file interaction including,
	gathering list of valid files, acting upon that list, and renaming files.
	
	--
	:param string|None dir		- string containing the directory for iteration containing files
	:param string keyword_file	- string containing full file path to location of keyword file
	:return Object File
	"""
	
	def __init__(self, dir=None, keyword_file=None):
		self.dir 			= dir
		self.keyword_file 	= keyword_file
		self.keywords_list	= []
		self.file_buf		= []
		self.files			= None
		
		
	def get_keyword_list(self, keyword_file=None):
		"""
		Create the list of keywords from the keywords file defined by user.
		
		--
		:param string keyword_file|None	- string containing full file path to location of keyword file
		:return Object Environment
		"""
		# allow keyword file override
		self.keyword_file = keyword_file or self.keyword_file
		
		with open(self.keyword_file, 'r') as f:
			content = f.readlines()
		
		if len(content) == 0 :
			raise Exception("No keywords found for ranking, in %s." % self.keyword_file)
		
		self.keywords_list = [l.strip() for l in content]
		# return self for method chaining
		return self


	def get_files(self, valid_types):
		"""
		Get a list of valid files found in iteration directory.
		
		--
		:param list valid_types	- list containing valid file extensions for parsing.
		:return Object File
		"""
		# get a list of files in the directory (files only)
		self.files = [f for f in os.listdir( self.dir ) if os.path.isfile(os.path.join(self.dir, f )) and os.path.splitext(f)[1] in valid_types and f != os.path.basename(self.keyword_file) and "~$" not in f]
		
		# throw error if no valid files are found in directory
		if len(self.files) == 0 :
			raise Exception("The directory provided has no valid files. Valid types include: .docx, .pdf, .txt")
		# return self for method chaining
		return self


	
	def file_iterator(self):
		# iterate over the valid files list
		for f in self.files :
			# remove the last character in the dir string if it is a slash for another directory
			path = os.path.join( self.dir.rstrip('//'), f )
			
			# instantiate an empty parsing object
			p = Parsing(path)
			
			# are there any results?
			if p.results :
				# instantiate the Rank object with the keyword_file passed as argument
				r = Rank(self.keywords_list)
				# pass the location of the keyword file, and the results to review into the rank class
				# get_rank returns a tuple of (rank, total_count)
				rank,total_count = r.get_rank(p.results)
									
				# get the filename, regardless of if there is already a percentage in front of filename or not
				filename_li = f.split('] - ')
				# reverse the filename split so the actual file name is always in position 0 of the list
				filename_li.reverse()
				
				# add the file information to the file buffer to be used for the last iteration
				self.file_buf.append({ 	 'orig_path'	: path
										,'orig_name'	: filename_li[0]
										,'dir'			: self.dir.rstrip('//')
										,'percent_rank' : rank
										,'total_count'  : total_count
									})
		# return self for method chaining
		return self


	def calc_percentile(self):
		# if file_buf has information in it
		if len(self.file_buf) :
			# resort the file list based on the total_count, in descending order so the first element is always the highest count	
			self.files = sorted(self.file_buf, key=lambda k: k['total_count'], reverse=True)

			# iterate over the newly sorted files list				
			for i, d in enumerate(self.files):
				percentile = self.get_percentile(d, self.files[0])

				# set the new filename with percentile and count included in filename
				d['new_name'] = "%s%% [%s] - %s" % (percentile, d['total_count'], d['orig_name'])
				d['percentile'] = percentile
				
		# return self for method chaining
		return self						
		

	def get_percentile(self, d, f):
		return round( ( float(d['total_count']) / float(f['total_count']) ) * 100, 2)



	def finish_output(self, output_type=None, output_file=None, rename=None, verbose=None) :
		"""
		Finally output the results in the preferred method specified by the user.  Or defaulted to file renaming.
		
		--
		:param string|None output_type	- user defined string containing the intended output file extension type from available values
		:param string|None output_file	- user defined string of full path location and filename of output file
		:param bool|None rename			- boolean flag defining whether original file names should be renamed with new filenames including percentile
		:param bool|None verbose		- boolean flag defining whether output resulting filenames should be printed to console
		"""
		
		try :
			f = None
			
			# open the file pointer if output_file is specified
			if output_file :
				f = open(output_file, 'w')
			
			# if the file type is csv then initialize the csv writer object
			if output_type and output_type.upper() == 'CSV' : 
				writer = csv.writer(f)
				# write the header row to the 
				writer.writerow( ('Percentile', 'Total Count', 'File Name') )
			
			for i, d in enumerate(self.files) :
			
				if verbose:
					# print the new filename to the console for the user
					print( os.path.basename(d['new_name']) )		
			
				# only rename the files if the rename option is set to true			
				if rename:
					self.rename_file( d['orig_path'], os.path.join(d['dir'], d['new_name']) )
	
				# append the filename to a string to be used to write to a file at the end of this iteration
				if output_type and output_type.upper() == 'TXT' :
					f.write( "%s\n" % d['new_name'] )
				
				if output_type and output_type.upper() == 'CSV' :
					writer.writerow( (d['percentile'], d['total_count'], d['new_name']) )
				
		finally :
			# close the file pointer if it exists
			if f :
				f.close()
			

	def rename_file(self, opath, npath):
		# rename the file name with the new rank
		os.rename(opath, npath)
	





if __name__ == "__main__" :
	# Docopt will check all arguments, and exit with the Usage string if they don't pass.
	# If you simply want to pass your own modules documentation then use __doc__,
	# otherwise, you would pass another docopt-friendly usage string here.
	# You could also pass your own arguments instead of sys.argv with: docopt(__doc__, argv=[your, args])
	docopt_args 	= docopt(__doc__, version='Resume Ranker 1.0.0')	
	verbosity 		= docopt_args["-v"]
	rename			= docopt_args["--rename"] or 'YES'
	dir				= docopt_args["--dir"]
	keyword_file 	= docopt_args["--keyword-file"]
	output_type		= docopt_args["--output-type"]
	output_file		= docopt_args["--output-file"]
	
	## -------------- CLI Argument Normalization ---------------- ##
	
	# normalize the rename option text to True/False
	rename = True if rename and rename.upper() == 'YES' else False
	
	# ensure the user input conforms to the available output types
	if output_type and output_type.upper() not in ['CSV', 'TXT']:
		raise Exception("Invalid value supplied to --output-type argument.  See --help for details.")
		
		# ensure the output file is a valid directory first
		e = Environment(path.dirname(output_file)).is_valid_directory()
	
	
	try :
		# instantiate the environment object where we will check that all environment paths and file names are valid
		# begin checking the paths and files, throw exception if something is not right
		e = Environment(dir, keyword_file).is_directory_given()\
			.is_valid_directory()\
			.is_valid_keyword_file()
			
		# set a list of the valid file types we can use, .docx, .pdf, .txt
		valid_types = ['.docx', '.txt', '.pdf']

		f = File(e.dir, e.keyword_file).get_keyword_list()\
			.get_files(valid_types)\
			.file_iterator()\
			.calc_percentile()\
			.finish_output(output_type, output_file, rename, verbosity)

			
						
				
		
	except Exception:
		raise
	
		
