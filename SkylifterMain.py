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

from SkylifterOp import SelectOptions
from SkylifterLabSetup import LabSetup
from SkylifterDeploy import RouterDeploy
from SkylifterConfig import BackhaulConfigFiles #, PrjFileSystem


def main(argfile):
    
    #############################################################
    #  All defined fuctions are called inside th main function  #
    #############################################################
    
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
        vm_path = ubuntu_vm_dict['vm_path']
        vm_name = ubuntu_vm_dict['vm_name']
        vm_host = ubuntu_vm_dict['vm_host']
        vm_username = ubuntu_vm_dict['vm_username']
        vm_password = ubuntu_vm_dict['vm_password']
        vm_sudo_password = ubuntu_vm_dict['vm_sudo_password']
        
        # Arguments for vMX router
        vmx_dict = GenArguments['vMX_router']
        vmx_hostname = vmx_dict['vmx_hostname']
        vmx_username = vmx_dict['vmx_username']
        vmx_password = vmx_dict['vmx_password']

        # Arguments for General File System
        files_dict = GenArguments['Skylifter_file_system']
        # File arguments
        base_conf_file_name = files_dict['base_conf_file_name']
        new_conf_file_name =  files_dict['new_conf_file_name']
        # File and Folder for new variable and configurations files
        source_folder_name = files_dict['source_folder_name']
        new_conf_folder_name = files_dict['new_conf_folder_name']
        save_conf_folder_name = files_dict['save_conf_folder_name']
        variable_folder_name = files_dict['variable_folder_name']
        
        # Arguments for Backhaul Project 
        backhaul_dict = GenArguments['Backhaul_project']
        
        project_name = backhaul_dict['project_name']
        prj_source_folder_name = backhaul_dict['prj_source_folder_name']
        
        jinja2_system_file_name = backhaul_dict['jinja2_system_file_name']
        jinja2_mpls_file_name = backhaul_dict['jinja2_mpls_file_name']
        jinja2_bgp_file_name = backhaul_dict['jinja2_bgp_file_name']
        
        xlsx_file_name = backhaul_dict['xlsx_file_name']
        sheet_name = backhaul_dict['sheet_name']
        
        prj_destination_folder_name = backhaul_dict['prj_destination_folder_name']
        yaml_file_name = backhaul_dict['yaml_file_name']
        py_file_name = backhaul_dict['py_file_name']
         
    except Exception,err:
        print("\nError: Encountered exception while opening %s file! \n\n%s\n")% (argfile,str(err))
        return False
    
    while True:

        if option=='1':
            print ('''
#==========================================================================#
#  Running option 1: Start Host Ubuntu VM and vMX router                    #
#==========================================================================#''')          
            start_rez = LabSetup.start_Ubuntu_vm(vm_path, vm_name)
            # Ubuntu Host is off
            if start_rez == 1: 
                print ("\nINFO: Ubunu Host VM have been Started!")             
                if LabSetup.start_vMX(vm_host, vm_username, vm_password, vm_sudo_password):
                    print ("\nINFO: Guest vMX router have been Started!") 
            # Ubuntu Host is on and restart have been selected
            elif start_rez == 2:
                print ("\nINFO: Host Ubuntu VM have been Restarted!")             
                if LabSetup.start_vMX(vm_host, vm_username, vm_password, vm_sudo_password):
                    print ("\nINFO: Guest vMX router have been Started!") 
            # Ubuntu Host is on and no restart have been selected
            elif start_rez == 3:
                print ("\nINFO: Skip Host Ubuntu VM restarting!")   
                opt='n'
                opt=raw_input("\nWould you like to restart guest vMX router? (y/N) _") 
                if opt=='y' or opt=='Y':
                    print '\nINFO: Reboot of vMX router has been intiated! Please wait ...'                           
                    if LabSetup.start_vMX(vm_host, vm_username, vm_password, vm_sudo_password):
                        print ("\nINFO: Guest vMX router have been restarted!") 
                else: 
                    print ("\nINFO: No Restart for guest vMX router has been selected!")
                    
        elif option=='2':
            print ('''
#==========================================================================#
#  Running option 2: Apply and commit a base configuration into            #
#  the Guest vMX virtual router                                            #
#==========================================================================#''')
            conf_file = source_folder_name+'/'+base_conf_file_name  
            RouterDeploy.overwriteConfig(vmx_hostname, vmx_username, vmx_password, conf_file)
               
        elif option=='3':
            print ('''
#==========================================================================#
#  Running option 3: Create a yaml file with variables taken from a csv    #
#  file. The csv file can be created directly or using excel export funct. #
#==========================================================================#''') 
            xlsx_file = prj_source_folder_name+'/'+xlsx_file_name
            
            sys_yaml_file = prj_destination_folder_name+'/'+variable_folder_name+'/'+yaml_file_name+'System.yaml'
            sys_py_file = prj_destination_folder_name+'/'+variable_folder_name+'/'+py_file_name+'System.py'
            if BackhaulConfigFiles.system_xlsx2yaml2py (xlsx_file, sheet_name, sys_yaml_file, sys_py_file):
                print ("\nINFO: The variables from excel file %s were exported into py file %s and yaml file %s.") %(xlsx_file_name, py_file_name, yaml_file_name)
            
            mpls_yaml_file = prj_destination_folder_name+'/'+variable_folder_name+'/'+yaml_file_name+'LSP.yaml'
            mpls_py_file = prj_destination_folder_name+'/'+variable_folder_name+'/'+py_file_name+'LSP.py'
            if BackhaulConfigFiles.mpls_xlsx2yaml2py(xlsx_file, sheet_name, mpls_yaml_file, mpls_py_file):
                print ("\nINFO: The variables from excel file %s were exported into py file %s and yaml file %s.") %(xlsx_file_name, py_file_name+'LSP.py', yaml_file_name+'LSP.yaml')
            
            bgp_yaml_file = prj_destination_folder_name+'/'+variable_folder_name+'/'+yaml_file_name+'BGP.yaml'
            bgp_py_file = prj_destination_folder_name+'/'+variable_folder_name+'/'+py_file_name+'BGP.py'
            if BackhaulConfigFiles.bgp_xlsx2yaml2py(xlsx_file, sheet_name, bgp_yaml_file, bgp_py_file):
                print ("\nINFO: The variables from excel file %s were exported into py file %s and yaml file %s.") %(xlsx_file_name, py_file_name+'BGP.py', yaml_file_name+'BGP.yaml')
        
        
        elif option=='4':
            print ('''
#============================================================================#
#  Running option 4: Create the configuration files using the existing yaml  #
#  variable files and junja2 template files. The configuration files will    #
#  be saved into specified folder as [date]-[time]-name.conf                 #
#============================================================================#''')
            new_conf_folder=prj_destination_folder_name+'/'+new_conf_folder_name
            
            print ('''
#============================================================================#
#  System Configuration:                                                     #
#      -> interfaces                                                         #
#      -> protocols                                                          #
#      -> system groups                                                      #
#      -> system                                                             #
#============================================================================#''')
            # System configuration
            jinja2_system_file = prj_source_folder_name+'/'+jinja2_system_file_name
            new_conf_file = 'system'+new_conf_file_name
            sys_yaml_file = prj_destination_folder_name+'/'+variable_folder_name+'/'+yaml_file_name+'System.yaml'
            
            system_conf_file_name = BackhaulConfigFiles.jinja2conf(jinja2_system_file, sys_yaml_file, new_conf_file, new_conf_folder)
            if system_conf_file_name:
                print ("\nINFO: The configuration file %s has been created from yaml variable file %s and jinja2 template file %s.") %(system_conf_file_name, yaml_file_name, jinja2_system_file_name)
                
                opt='n'
                opt=raw_input("\nWould you like to apply the configuration? (y/N) _") 
                if opt=='y' or opt=='Y':  
                    system_conf_file = new_conf_folder+'/'+system_conf_file_name                       
                    if RouterDeploy.mergeConfig(vmx_hostname, vmx_username, vmx_password, system_conf_file):
                        print ("\nINFO: The configuration file %s has been applyed to Guest vMX router.") % system_conf_file_name
                else: 
                    print ("\nINFO: The configuration was not appied on the system!")
            
            
            print ('''
#============================================================================#
#  MPLS Configuration:                                                       #
#      -> LSPs                                                               #
#      -> system groups                                                      #
#============================================================================#''')
            # MPLS configuration
            jinja2_mpls_file = prj_source_folder_name+'/'+jinja2_mpls_file_name
            new_conf_file = 'mpls'+new_conf_file_name
            mpls_yaml_file = prj_destination_folder_name+'/'+variable_folder_name+'/'+yaml_file_name+'LSP.yaml'
            
            mpls_conf_file_name = BackhaulConfigFiles.jinja2conf(jinja2_mpls_file, mpls_yaml_file, new_conf_file, new_conf_folder)
            if mpls_conf_file_name:
                print ("\nINFO: The configuration file %s has been created from yaml variable file %s and jinja2 template file %s.") %(mpls_conf_file_name, yaml_file_name, jinja2_mpls_file_name)

                opt='n'
                opt=raw_input("\nWould you like to apply the configuration? (y/N) _") 
                if opt=='y' or opt=='Y':  
                    mpls_conf_file = new_conf_folder+'/'+mpls_conf_file_name                        
                    if RouterDeploy.mergeConfig(vmx_hostname, vmx_username, vmx_password, mpls_conf_file):
                        print ("\nINFO: The configuration file %s has been applyed to Guest vMX router.") % mpls_conf_file_name
                else: 
                    print ("\nINFO: The configuration was not appied on the system!")
             
            
            print ('''
#============================================================================#
#  BGP Configuration:                                                        #
#      -> groups and neighbors                                               #
#      -> system groups                                                      #
#============================================================================#''')
            # BGP configuration
            jinja2_bgp_file = prj_source_folder_name+'/'+jinja2_bgp_file_name
            new_conf_file = 'bgp'+new_conf_file_name
            bgp_yaml_file = prj_destination_folder_name+'/'+variable_folder_name+'/'+yaml_file_name+'BGP.yaml'
            
            bgp_conf_file_name = BackhaulConfigFiles.jinja2conf(jinja2_bgp_file, bgp_yaml_file, new_conf_file, new_conf_folder)
            if bgp_conf_file_name:
                print ("\nINFO: The configuration file %s has been created from yaml variable file %s and jinja2 template file %s.") %(bgp_conf_file_name, yaml_file_name, jinja2_bgp_file_name)

                opt='n'
                opt=raw_input("\nWould you like to apply the configuration? (y/N) _") 
                if opt=='y' or opt=='Y':  
                    bgp_conf_file = new_conf_folder+'/'+bgp_conf_file_name                        
                    if RouterDeploy.mergeConfig(vmx_hostname, vmx_username, vmx_password, bgp_conf_file):
                        print ("\nINFO: The configuration file %s has been applyed to Guest vMX router.") % bgp_conf_file_name
                else: 
                    print ("\nINFO: The configuration was not appied on the system!")
                   
  
  
        elif option=='5':
            print ('''
#==========================================================================#
#  Running option 5: Save the running configuration file from vMX into     #
#  specified folder as [date]-[time]-project_name.conf                      #
#==========================================================================#''')
            save_conf_folder = prj_destination_folder_name+'/'+save_conf_folder_name
            save_file_name=RouterDeploy.saveConfig(vmx_hostname, vmx_username, vmx_password, save_conf_folder, project_name)  
            if save_file_name:
                print ("\nINFO: A new configuration file has been created and saved in %s as %s.") %(save_conf_folder_name, save_file_name) 
     

  
        elif option=='6':
            print ('''
#==========================================================================#
#  Running option 6: Stop vMX Ubuntu Host.                                 #
#==========================================================================#''')
            if LabSetup.stop_Ubuntu_vm(vm_path, vm_name):
                print ("\nINFO: Host VM have been Stoped!")   
                          
         
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
    #PrjFileSystem.list_files('SkylifterDestFiles/')
    


    