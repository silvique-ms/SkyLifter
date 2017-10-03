#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""A module to allow the selection of different application options"""

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

import sys
from cowpy import cow

def enterOpt():
    
    ###################################################
    #  Ask the user to insert an option               #
    ###################################################
    print ('''
#==========================================================================#
#  Selecting an OPTION!                                                    #
#==========================================================================#''') 
    print ('''
Happy Silvia, you can use the following options: 

    0.    - project presentation 
               - list file system 
               - list readme.txt for each folder/module
    
    Virtual Lab administration:
    
    1.     - start/restart Host Ubuntu VM and start/restart Guest vMX router
    2.     - reset Guest vMX router with base/static config (overwrite)
    3.     - stop Host Ubuntu VM
    
    Bachaul project configuration and operation:
    
    Configuration:
    
    4.     - create YAML .yaml and Python .py variable file using info from Excel .xlsx file
               - interface and IGP protocol variables
               - LSP variables
    5.     - create configuration from template using 
               a jinja2 template file and a yaml variable files, 
               - save the configuration file into the specified folder and 
               - apply the configuration if requested
    6.     - save existing configuration from Guest vMX router
               - single configuration file
               - multiple configuration files for each Logical System
    
    Operation and verification:
    
    7.     - colect operational information RPC
    8.     - colect operational information tables and views
    
    STOP:
    SPACE  -  quit application
    
Please enter your option or press space to quit:  ''')
    
    option_list=['0','1','2','3','4','5','6', '7', '8']
    option=raw_input ('')
    option.strip()
        
    while option not in option_list:
        if option==' ':
            print ('''
#==========================================================================#
#  Getting OUT!                                                            #
#==========================================================================#''') 
            cowsayMessage('May All Beings Be Free & Happy!\nHave a wonderful day, Silvia!')
            sys.exit()
        else:
            cowsayMessage('\nThis is not a valid option.')
            print ('''
#==========================================================================#
#  Please RETRY!                                                           #
#==========================================================================#''') 
            print ('\nThe available options are the following:')
            print option_list
            print ('\nPlease enter your option or press space to quit:')
            option=raw_input('')
    
    return option

def cowsayMessage(message):
    
    ###################################################
    #  Print a messsage usig COW library              #
    ###################################################
    
    # Create a Cow
    my_cow = cow.Moose()
    # Get a cowsay message by milking the cow
    msg = my_cow.milk(message)
    # do something with the message
    print(msg)
        
    return True
