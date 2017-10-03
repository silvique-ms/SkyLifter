#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""A library to start, restart and stop the virtual laboratory: Host Ubuntu VM and Guest vMX Router"""

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

import paramiko
import time
from vmfusion import vmrun

from SkylifterDeploy import RouterDeploy

def start_Ubuntu_vm(vm_path, vm_name):
    
    ###################################################
    #   Start Ubuntu Host VM                          #          
    #   Return:                                       #
    #   - 0 - Error                                   #
    #   - 1 - Start                                   #
    #   - 2 - Restart                                 #     
    #   - 3 - No Restart                              #
    ###################################################
    
    try:
        vmlist = vmrun.list()
        for machine in vmlist['machines']:
            if vm_name in machine:
                print '\nList of running VMs: '
                print vmlist['machines']
                print '\nINFO: Ubuntu Host VM is allready ON!'
                opt='n'
                opt=raw_input("\nWould you like to restart it? (y/N) _") 
                if opt=='y' or opt=='Y':
                    print '\nINFO: Reboot has been intiated! Please wait ...'
                    vmrun.reset( vm_path, soft=True )
                    time.sleep(180)
                    return 2
                else:
                    print '\nNo Restart has been selected!'
                    return 3
            else:
                print '\nINFO: Ubuntu Host VM is OFF! Power ON has been initiated! Please wait ...'
                vmrun.start(vm_path)
                time.sleep(180)
                return 1
        if vmlist['machines'] == []:
            print '\nINFO: Ubuntu Host VM is OFF! Power ON has been initiated! Please wait ...'
            vmrun.start(vm_path)
            time.sleep(180)
            return 1
            
    except Exception,err:
        print"\nError: Encountered exception while starting the Ubuntu Host VM. \nException is: %s.\n" %str(err)
        return 0

def stop_Ubuntu_vm(vm_path, vm_name):
    
    ###################################################
    #     Stop Ubuntu Host VM                         #
    ###################################################
      
    try:
        vmlist = vmrun.list()
        if vmlist['machines'] == []:
            print '\nAll VMs are OFF!'
            return False
        else:
            print '\nHere is the list of running VMs: '
            print vmlist['machines']
            for machine in vmlist['machines']:
                if vm_name in machine:
                    print '\nINFO: Host Ubuntu VM is ON! Power off has been intiated!'
                    vmrun.stop(vm_path, soft=True)
                    
    except Exception,err:
        print"\nError: Encountered exception while stopping the Host Ubuntu VM. Exception is: %s.\n" %str(err)
        return False
     
    return True
    
def start_vMX(vm_host, my_username, my_password, sudo_password):
    
    ##############################################################
    #  Connect to Host Ubuntu Server and Start Guest vMX router  #
    ##############################################################
    
    ubuntu_commands = 'cd vmx-15.1F4-3/; sudo -S ./vmx.sh -lv --install; ./vmx.sh --bind-dev'

    try: 
        # Connect to the Ubuntu Server
        u_ssh = paramiko.SSHClient()
        u_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        u_ssh.connect(vm_host, username=my_username, password=my_password)
    except Exception,err:
        print"\nError: Encountered exception while connecting to Host Ubuntu VM. \nException is: %s.\n" %str(err)
        return False   
      
    try:  
        # start and setup vMX
        stdin,stdout,stderr = u_ssh.exec_command(ubuntu_commands)
        stdin.write(sudo_password)
        stdin.write('\n')
        stdin.flush()

        # Print output and errors
        print('\nINFO: Wait three minutes for the Guest vMX router to start!\n')
        time.sleep(180)
    
        print('\nWarning and Errors:\n')
        for line in stderr.readlines():
            print line.rstrip()
    
        print ('\n\n\nProcessing outputs:\n')
        for line in stdout.readlines():
            print line.rstrip()
        
        # Close Session
        u_ssh.close()
    
    except Exception,err:
        print"\nError: Encountered exception while starting the Guest vMX router. \nException is: %s.\n" %str(err)
        return False
        
    return True


def virtualLabAdmin(ubuntu_vm_dict, vmx_dict, files_dict, option):
    
    # Arguments for Ubuntu VM
    vm_path = ubuntu_vm_dict['vm_path']
    vm_name = ubuntu_vm_dict['vm_name']
    vm_host = ubuntu_vm_dict['vm_host']
    vm_username = ubuntu_vm_dict['vm_username']
    vm_password = ubuntu_vm_dict['vm_password']
    vm_sudo_password = ubuntu_vm_dict['vm_sudo_password']
        
    # Arguments for vMX router
    vmx_hostname = vmx_dict['vmx_hostname']
    vmx_username = vmx_dict['vmx_username']
    vmx_password = vmx_dict['vmx_password']

    # Arguments for General File System
    base_conf_file_name = files_dict['base_conf_file_name']
    source_folder_name = files_dict['source_folder_name']

    try:
        if option=='1':
            print ('''
#==========================================================================#
#  Running option 1: Start Host Ubuntu VM and vMX router                    #
#==========================================================================#''')          
            start_rez = start_Ubuntu_vm(vm_path, vm_name)
            # Ubuntu Host is off
            if start_rez == 1: 
                print ("\nINFO: Ubunu Host VM have been Started!")             
                if start_vMX(vm_host, vm_username, vm_password, vm_sudo_password):
                    print ("\nINFO: Guest vMX router have been Started!") 
            # Ubuntu Host is on and restart have been selected
            elif start_rez == 2:
                print ("\nINFO: Host Ubuntu VM have been Restarted!")             
                if start_vMX(vm_host, vm_username, vm_password, vm_sudo_password):
                    print ("\nINFO: Guest vMX router have been Started!") 
            # Ubuntu Host is on and no restart have been selected
            elif start_rez == 3:
                print ("\nINFO: Skip Host Ubuntu VM restarting!")   
                opt='n'
                opt=raw_input("\nWould you like to restart guest vMX router? (y/N) _") 
                if opt=='y' or opt=='Y':
                    print '\nINFO: Reboot of vMX router has been intiated! Please wait ...'                           
                    if start_vMX(vm_host, vm_username, vm_password, vm_sudo_password):
                        print ("\nINFO: Guest vMX router have been restarted!") 
                else: 
                    print ("\nINFO: No Restart for guest vMX router has been selected!")
                    
        elif option=='2':
            print ('''
#==========================================================================#
#  Running option 2: Apply and commit a base configuration into            #
#  the Guest vMX virtual router: reset vMX to base config!                 #
#==========================================================================#''')
            conf_file = source_folder_name+'/'+base_conf_file_name  
            RouterDeploy.overwriteConfig(vmx_hostname, vmx_username, vmx_password, conf_file)
        
        elif option=='3':
            print ('''
#==========================================================================#
#  Running option 6: Stop vMX Ubuntu Host.                                 #
#==========================================================================#''')
            if stop_Ubuntu_vm(vm_path, vm_name):
                print ("\nINFO: Host VM have been Stoped!")   
        
    except Exception, err:
        print("\nError: \n %s") % str(err)
        return False
    
    return True