#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""A tool to configure and operate a virtual laboratory"""

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

import yaml

from SkylifterMainOp import SelectOptions
from SkylifterConfig import BackhaulConfigFiles, PrjFileSystem
from SkylifterDevOp import CollectDevOp
from SkylifterLabSetup import LabSetup


def main(argfile):
    
    ##############################################################
    #  All defined fuctions are called inside the main function  #
    ##############################################################
    
    print ('''
#==========================================================================#
#        NAMASTE, Silvia!!                                                 #
#                                                                          #
# "Namaste: My soul recognizes your soul, I honor the light, love, beauty, #
# truth and kindness within you because it is also within me, in sharing   #
# these things there is no distance and no difference between us, we are   #
# the same, we are one."                                                   #
#                                                                          #
#  Welcome to Junos configuration deployment tool!                         #
#==========================================================================#''')

    # Get user options and react accordingly
    option = SelectOptions.enterOpt()
    
    # Get General Arguments from YAML file
    try:
        
        GenArguments = yaml.load(open(argfile))
        # Arguments for Ubuntu VM
        ubuntu_vm_dict = GenArguments['Ubuntu_VM']
        # Arguments for vMX router
        vmx_dict = GenArguments['vMX_router']
        # Arguments for General File System
        files_dict = GenArguments['Skylifter_file_system']
        # Arguments for Backhaul Project 
        backhaul_dict = GenArguments['Backhaul_project']
        
    except Exception,err:
        print("\nError: Encountered exception while opening %s file! \n\n%s\n")% (argfile,str(err))
        return False
    
    while True:
        
        if option=='0':
            PrjFileSystem.list_files('./')
            print "\n Here I will insert a summary for the program! \n ================================================!!!!!"
        
        elif option in ['1','2','3']:
            LabSetup.virtualLabAdmin(ubuntu_vm_dict, vmx_dict, files_dict, option)
        
        elif option in ['4', '5', '6']:
            BackhaulConfigFiles.configurationOption(backhaul_dict,files_dict,vmx_dict,option)
            
        elif option in ['7','8']:
            CollectDevOp.collectDevOp (vmx_dict, files_dict, backhaul_dict, option)

        opt='n'
        opt=raw_input ('''
#==============================================================================#
#  Would you like to continue having fun and find the God within you?  (y/N) _ ''')
        print ("#==============================================================================#")  
        if opt=='n' or opt=='N': 
            print ('''
#==========================================================================#
#  Getting OUT!                                                            #
#==========================================================================#''') 
            SelectOptions.cowsayMessage('May All Beings Be Free & Happy!\nHave a wonderful day, Silvia!')
            return  
        
        option = SelectOptions.enterOpt()     

if __name__ == '__main__':
    
    GeneralArgumentFile = 'SkylifterSourceFiles/general_arguments.yaml'   
    main(GeneralArgumentFile)
    
    #PrjFileSystem.list_files('./SkylifterDestFiles/')
    #print "\n NEXT! \n"
    #PrjFileSystem.list_files('SkylifterDestFiles/')

    
    


    