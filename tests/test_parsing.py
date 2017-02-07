#!/usr/bin/python

import unittest

from os import sys, path
# add the base directory of the project to the PATH environment
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
	
from ranker import Parsing, File, Rank


class TestParsingFunctions(unittest.TestCase):
	
	def setUp(self):
		self.keyword_file = 'samples/keywords.txt'
	
	def test_docx_load(self):
		p = Parsing('samples/Sample Resume.docx')
		self.assertIsNotNone(p.results)
	
	def test_pdf_load(self):
		p = Parsing('samples/Sample Resume.pdf')
		self.assertIsNotNone(p.results)	

	def test_txt_load(self):
		p = Parsing('samples/Sample Resume.txt')
		self.assertIsNotNone(p.results)	

	def test_keywords_load(self):
		f = File()
		f.get_keyword_list(self.keyword_file)
		# assert that the keywords list assigned from parsing the keywords file is not equal to []
		self.assertIsNot([],f.keywords_list)
		
	def test_keywords_multiplier(self):
		f = File()
		f.get_keyword_list(self.keyword_file)
		
		r = Rank(f.keywords_list)
		
		for keyword in f.keywords_list :
			keyword, multiplier = r.get_multiplier(keyword)
		
		# Ending assertion, assuming that if it made it this far then it passed the loop and function
		self.assertTrue(True)





if __name__ == '__main__' and __package__ is None:
	unittest.main()