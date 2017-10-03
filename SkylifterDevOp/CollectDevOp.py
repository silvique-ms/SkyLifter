#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""A library to connect to vMX and collect DevOp - RPC and Table&views information"""

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

from SkylifterDevOp import CollectRPC

def collectDevOp (vmx_dict, files_dict, backhaul_dict, option):
    
    # Arguments for vMX router
    vmx_hostname = vmx_dict['vmx_hostname']
    vmx_username = vmx_dict['vmx_username']
    vmx_password = vmx_dict['vmx_password']
    
    # Arguments for Files
    variable_folder_name = files_dict['variable_folder_name']
    devop_rfc_folder_name = files_dict['devop_rfc_folder_name']
        
    # Arguments for Backhaul Project   
    prj_destination_folder_name = backhaul_dict['prj_destination_folder_name']
    yaml_file_name = backhaul_dict['yaml_file_name']
    
    rpc_devop_file_name = backhaul_dict['rpc_devop_file_name']
    tableviews_devop_file_name = backhaul_dict['tableviews_devop_file_name']
    
    try:
        if option=='7':
            print ('''
#============================================================================#
#  Running option 7: Collect devOp information.                              #
#  be saved into specified folder as [date]-[time]-name.conf                 #
#============================================================================#''')
            
            yaml_file = prj_destination_folder_name+'/'+variable_folder_name+'/'+yaml_file_name
            folder_name = prj_destination_folder_name+'/'+devop_rfc_folder_name
            CollectRPC.collectSystem(vmx_hostname, vmx_username, vmx_password, yaml_file, rpc_devop_file_name, folder_name)
            CollectRPC.collectISIS(vmx_hostname, vmx_username, vmx_password, yaml_file, rpc_devop_file_name, folder_name)
       
        elif option=='8':
            print ('''
#============================================================================#
#  Running option 8: Collect table and views information.                    #
#  be saved into specified folder as [date]-[time]-name.conf                 #
#============================================================================#''')
            print 'TO BE IMPLEMENTED'
            
    
    except Exception, err:
        print("\nError: \n %s") % str(err)
        return False
    
    return True           