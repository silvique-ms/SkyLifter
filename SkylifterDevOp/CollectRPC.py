#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""A library to connect to vMX and collect RPC information"""

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
from time import strftime

from junos import Device

def collectSystem(my_host, my_user, my_password, yaml_file, rpc_devop_file, folder_name):
    
    ########################################################
    # Connect to vMX router and collect System operational #
    # commands outputs                                     #
    #                                                      #
    # The operational file name is generated based         # 
    # on date_time-SYSTEM_rpc_devop_file.txt.              #
    ########################################################
    
    try:
        
        print("\nINFO: Connecting to the device to collect System Operational info!")
        dev=Device(host=my_host, user=my_user, password=my_password)
        dev.open()
        dev.timeout=3*60
        
        print("\nINFO: Create rpc_devop_file file!") 
        systemopfile=strftime("%Y.%m.%d_%H.%M.%S")+' - SYSTEM_'+rpc_devop_file+'.txt'
        full_file_path=folder_name+'/'+systemopfile  
        print full_file_path      
        opfile = open(full_file_path, 'w')
        
        print("\nINFO: Open variable .yaml file!")  
        var_data = yaml.load(open(yaml_file))
        
        
        print("\nINFO: Start collecting the info and writting into the file ...") 
        
        opfile.write('''
        
# Set context '> set cli logical-system <>'
# Get '> show interface descriptions' output
# Clear context '> clear cli logical-system'
=============================================
''')
        ls_int_descr = ''
        for ls in var_data['Logical_systems']:
            dev.rpc.set_logical_router(logical_system=ls)
            
            intd_info = dev.rpc.get_interface_information({'format':'text'}, descriptions=True)
            if intd_info == True:
                ls_int_descr = ls_int_descr + '\n> show interface descriptions logical-system ' + ls +'\n'
            else:
                ls_int_descr = ls_int_descr + '\n> show interface descriptions logical-system ' + ls +'\n'+ intd_info.text
            
            dev.rpc.clear_cli_logical_system()
            
        opfile.write(ls_int_descr)
        
        opfile.write('''
        
# Set context '> set cli logical-system <>'
# Get '> show interface terse' output
# Clear context '> clear cli logical-system'
=============================================
''')
        ls_int_terse = ''
        for ls in var_data['Logical_systems']:
            dev.rpc.set_logical_router(logical_system=ls)
            
            intt_info = dev.rpc.get_interface_information({'format':'text'}, terse=True)
            if intt_info == True:
                ls_int_terse = ls_int_terse + '\n> show interface terse logical-system ' + ls +'\n'
            else:
                ls_int_terse = ls_int_terse + '\n> show interface terse logical-system ' + ls +'\n'+ intt_info.text
            
            dev.rpc.clear_cli_logical_system()
            
        opfile.write(ls_int_terse)
        
        opfile.write('''
        
# Set context '> set cli logical-system <>'
# Get '> show interface' output
# Clear context '> clear cli logical-system'
=============================================
''')
        ls_int = ''
        for ls in var_data['Logical_systems']:
            dev.rpc.set_logical_router(logical_system=ls)
            
            int_info = dev.rpc.get_interface_information({'format':'text'})
            if int_info == True:
                ls_int = ls_int + '\n> show interface logical-system ' + ls +'\n'
            else:
                ls_int = ls_int + '\n> show interface logical-system ' + ls +'\n'+ int_info.text
            
            dev.rpc.clear_cli_logical_system()
            
        opfile.write(ls_int)
        
        opfile.close()
        dev.close()

    except Exception,err:
        print("\nError: Encountered exception: \n%s")%str(err)
        return False
    
    print("\nINFO: The SYSTEM DevOp file %s have been created!")%full_file_path
    return True 
 
def collectISIS(my_host, my_user, my_password, yaml_file, rpc_devop_file, folder_name):
    
    ######################################################
    # Connect to vMX router and collect ISIS operational #
    # commands output                                    #
    #                                                    #
    # The operational file name is generated based       # 
    # on date_time-ISIS_rpc_devop_file.txt.              #
    ######################################################
    
    try:
        
        print("\nINFO: Connecting to the device to collect ISIS operational info!")
        dev=Device(host=my_host, user=my_user, password=my_password)
        dev.open()
        dev.timeout=3*60
        
        print("\nINFO: Create rpc_devop_file file!") 
        isisopfile=strftime("%Y.%m.%d_%H.%M.%S")+' - ISIS_'+rpc_devop_file+'.txt'
        full_file_path=folder_name+'/'+isisopfile  
        print full_file_path      
        opfile = open(full_file_path, 'w')
        
        print("\nINFO: Open variable .yaml file!")  
        var_data = yaml.load(open(yaml_file))
        
        
        print("\nINFO: Start collecting the info and writting into the file ...") 
        
        opfile.write('''
        
# Get '> show isis adjacency logical-system all' output
======================================================
''')
        ls_isis_adj = ''
        for ls in var_data['Logical_systems']:
            adj_info = dev.rpc.get_isis_adjacency_information({'format':'text'}, logical_system=ls)
            if adj_info == True:
                ls_isis_adj = ls_isis_adj + '\n> show isis adjacency logical-system ' + ls +'\n'
            else:
                ls_isis_adj = ls_isis_adj + '\n> show isis adjacency logical-system ' + ls +'\n'+ adj_info.text
        opfile.write(ls_isis_adj)
        
        opfile.write ('''
        
# Get '> show isis interface logical-system all' output
========================================================
''')          
        ls_isis_int = ''
        for ls in var_data['Logical_systems']:
            int_info = dev.rpc.get_isis_interface_information({'format':'text'}, logical_system=ls)
            if int_info == True:
                ls_isis_int = ls_isis_int + '\n> show isis interface logical-system ' + ls +'\n'
            else:
                ls_isis_int = ls_isis_int + '\n> show isis interface logical-system ' + ls +'\n'+ int_info.text
        opfile.write(ls_isis_int)
        
        opfile.write('''
        
# Get '> show isis route logical-system all' output
=============================================================
''')
        ls_isis_route = ''
        for ls in var_data['Logical_systems']:
            route_info = dev.rpc.get_isis_route_information({'format':'text'}, logical_system=ls)
            if route_info == True:
                ls_isis_route = ls_isis_route + '\n> show isis route logical-system ' + ls +'\n'
            else:
                ls_isis_route = ls_isis_route + '\n> show isis route logical-system ' + ls +'\n'+ route_info.text
        opfile.write(ls_isis_route)
        
        opfile.close()
        dev.close()

    except Exception,err:
        print("\nError: Encountered exception: \n%s")%str(err)
        return False
    
    print("\nINFO: The ISIS DevOp file %s have been created!")%full_file_path
    return True 
    
        