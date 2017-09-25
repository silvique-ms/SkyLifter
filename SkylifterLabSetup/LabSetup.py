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
