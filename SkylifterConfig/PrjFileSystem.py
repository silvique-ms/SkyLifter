#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""A tool to check and create the file system needed for the specify project """

# Copyright (c) 2017 Silvia Murgescu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__author__ = "Silvia Murgescu"
__copyright__ = "Copyright 2017, Skylifter Personal Project"

__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Silvia Murgescu"
__email__ = "silvique_ms@yahoo.com"
__status__ = "Deployment"

import os

def CreateFileSystem (root_folder, project_name):
    
    try:

        if not os.path.isdir(root_folder):
            os.makedirs(root_folder)
            print("\nINFO: A new folder was created!")
        
    except Exception,err:
        print("\nError: Encountered exception while creating the folder %s: \n%s")%(root_folder, str(err))
        return False
    
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))