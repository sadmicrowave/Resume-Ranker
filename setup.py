#!/usr/bin/python

# Copyright (C) 2015 Emerus, Holdings
#
# This file is part of Resume Ranker.
#
# Hermes is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hermes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hermes.  If not, see <http://www.gnu.org/licenses/>.


from distutils.core import setup

setup(name='Resume Ranker',
      version='1.0',
      description='Rank resumes based on keywords',
      author='Corey Farmer',
      author_email='corey.m.farmer@gmail.com',
      packages=['docopt', 'pyPdf', 'docx'],
     )