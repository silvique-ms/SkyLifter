#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""A module to allow the creation of a new general_arguments.yaml file"""

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

from getpass import getpass

def insert_atributes(general_arguments_file_path):
    
    try: 
        arg_file = open(general_arguments_file_path, 'w')
    
        hostname = raw_input("Hostname:")
        username = raw_input("Username:")
        password = getpass ("Password:")
        
        arg_file.write(hostname + '  ' + username + '  ' + password)


        """        gen_arg_info = ''' 
Ubuntu_VM:
 vm_path: '/Users/silvia/Documents/Virtual Machines.localized/vMX.vmwarevm/vMX.vmx'
 vm_name: 'vMX'
 vm_host: '172.16.226.20'
 vm_username: 'silvia'
 vm_password: 'SilviaMurgescu'
 vm_sudo_password: 'SilviaMurgescu'  

vMX_router: 
 vmx_hostname: '172.16.226.10'
 vmx_username: 'silvia'
 vmx_password: 'SilviaMurgescu'
 
   
Skylifter_file_system:
 source_folder_name: 'SkylifterSourceFiles'
 base_conf_file_name: 'vmx_base.conf'
 
 new_conf_file_name: '_from_Template'
 new_conf_folder_name: 'NewConfFiles'
 save_conf_folder_name: 'SavedConfFiles'
 variable_folder_name: 'VariableFiles'
 
Backhaul_project:
  project_name: 'Backhaul'
  prj_source_folder_name: 'SkylifterSourceFiles'
  
  jinja2_system_file_name: 'system_template_config.j2'
  jinja2_mpls_file_name: 'mpls_template_config.j2'
  jinja2_bgp_file_name: 'bgp_template_config.j2'
  
  xlsx_file_name: 'Network_Information.xlsx'
  sheet_name: 'Interfaces'
  
  prj_destination_folder_name: 'SkylifterDestFiles'
  yaml_file_name: 'LSDataYAML'
  py_file_name: 'LSData' '''"""
        
    except Exception,err:
        print"\nError: Encountered exception! \nException is: %s.\n" %str(err)
        return 0
    
    return 1
        
if __name__ == '__main__':
    
    insert_atributes('general_arguments_file_name.yml', '')
    
