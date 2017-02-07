
Resume Ranker
===================

This package serves as a small CLI utility to rank resumes, or other files, based on keyword criteria.  The utility reviews files and assigns a score based on percentile match of the file's content.  Valid
file types include .docx, .pdf, and .txt.   Any other filetype will be skipped automatically.

Resume Ranker will rename each valid file with a prefixed calculated percentile rank and matching total word count by default (unless explicitly told not to).

Use the script's built-in help command to view extended usages and argument definition.  


### Requirements

Please see the **[requirements documentation](/documentation/requirements.md)** for system requirements and more information about the supported operating systems.

### Usage

Resume Ranker is a CLI script built on [`Python 2.7.10`](https://www.python.org/downloads/release/python-2710/) and is executed using the syntax formation below.  Where the required arguments `--dir` references the directory where the files to iterate are found, and `--keyword_file` references a valid keyword file.

    $ python ranker.py --dir=directory/containing/files/to/rank --keyword-file=directory/containing/keyword_file.txt


### The Keyword File

The keyword file is a runtime requirement and must be supplied as an argument of the script at the time of execution.  A sample file can be found here: [`keyword_file`](/tests/samples/keywords.txt).  

The example provides keywords, separated by line breaks (with spaces allowed in the keyword(s)) followed by a keyword weight, if desired.  The weight is multiplied by the total occurrences of the word in the file to produce a heavier weight for each weighted word, compared to other words.  

    Bachelor *2
	Master
	SQL
	C#
	Python
	Software Developer
	Black Belt Ninja *5

In the example above, `Bachelor` is weighted twice as heavy as other 'non-weighted' words.  While `Black Belt Ninja` is weighted five times heavier. 

The formatting of each word is normalized to an all uppercase format upon load within the script; therefore, word capitalization will not have any bearing. 



### Contributing

Resume Ranker is an open source project and we are very happy to accept community contributions. Please refer to [CONTRIBUTING.md](/documentation/CONTRIBUTING.md) for details.



### Caveats

As of this time, Resume Ranker only iterates over the following file types `.pdf`, `.docx`, `.txt`.  Older Microsoft Office versions producing `.doc` file types require ancillary system level packages that are out of the scope of this original project.


> **Note:**

> - This project is accepting merge requests to extend functionality.
> - Please review the [CONTRIBUTING.md](/documentation/CONTRIBUTING.md) documentation before beginning development.


