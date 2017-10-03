#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""A library to connect to vMX and overwrite, merge ar save the configuration"""

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

from time import strftime
from lxml import etree

from junos import Device
from junos.utils.config import Config



def saveConfig(my_host, my_user, my_password, folder_name, project_name):
    
    ####################################################
    # Connect to vMX router and save existing          #
    # configuration as .xml and .conf into specified   #
    # folder.                                          #
    #                                                  #
    # The configuration file name is generated based   # 
    # on date_time-project_name.                        #
    ####################################################
    
    try:
        print("\nINFO: Connecting to the device!")
        dev=Device(host=my_host, user=my_user, password=my_password)
        dev.open()
        dev.timeout=3*60
        
        config_xml = dev.rpc.get_config()
  
        options = {'database':'committed', 'format': 'text'}
        cnf = dev.rpc.get_config(options=options)
        config_txt = cnf.xpath('//configuration-text')[0].text
        
        dev.close()

    except Exception,err:
        print("\nError: Encountered exception while connecting to the device %s: \n%s")%(my_host, str(err))
        return False
        
    try:
        print("\nINFO: Saving configuration!")
        if not os.path.isdir(folder_name):
            folder_name=folder_name.replace(" ", "_")
            os.makedirs(folder_name)
            print("\nINFO: A new folder was created!")
        
    except Exception,err:
        print("\nError: Encountered exception while creating the folder %s: \n%s")%(folder_name, str(err))
        return False
            
    try:
        # Save file in .xml format
        savefilename_xml=strftime("%Y.%m.%d_%H.%M.%S")+' - '+project_name+'.xml'
        full_file_path_xml=folder_name+'/'+savefilename_xml
        
        f=open(full_file_path_xml, 'w')
        f.write(etree.tostring(config_xml))
        f.close()
        
    except Exception,err:
        print("\nError: Encountered exception while saving the configuration file:\n %s \nError is %s")%(savefilename_xml, str(err))
        return False
    
    try:
        #save file in .conf format
        savefilename_conf=strftime("%Y.%m.%d_%H.%M.%S")+' - '+project_name+'.conf'
        full_file_path_conf=folder_name+'/'+savefilename_conf
        
        f_conf=open(full_file_path_conf, 'w')
        f_conf.write(config_txt)
        f_conf.close()
        
    except Exception,err:
        print("\nError: Encountered exception while saving the configuration file:\n %s \nError is %s")%(savefilename_conf, str(err))
        return False
        
    except Exception,err:
        print("\nError: Encountered exception while saving the configuration file %s: \n%s")%(savefilename_xml, str(err))
        return False
        
    return savefilename_xml

def mergeConfig(my_host, my_user, my_password, my_conf_file):
    
    ############################################################################
    # Add some configuration from a predefined configuration file - MERGE      #
    ############################################################################
    
    try:
        dev=Device(host=my_host, user=my_user, password=my_password)
        dev.open()
        dev.timeout=3*60
        
        cu=Config(dev)
        cu.lock()
        cu.load(template_path=my_conf_file, merge=True)
        conf_diff=cu.diff()
     
        if conf_diff:
            print "\nINFO: The following changes will be applied: \n %s" %conf_diff
            
            if cu.commit_check():
                cu.commit()
                print ("\nINFO: The configuration file %s has been preccesed for the device.") % my_conf_file
            else:
                cu.rollback()
                print ("\nERROR: Commit check error!")
                
            cu.unlock()
            dev.close()
                
        else:
            print "\nINFO: No new configuration need to be applied."
            cu.rollback()
            cu.unlock()
            dev.close()
            return False
        
    except Exception, err:
        print("\nError: Encountered exception while deploying configuration:\n %s") % str(err)
        return False
        
    return True

def overwriteConfig(my_host, my_user, my_password, my_conf_file):
    
    ####################################################################################
    # Apply a complete configuration from a predefined configuration file - OVERWRITE  #
    ####################################################################################
    
    try:
        
        dev=Device(host=my_host, user=my_user, password=my_password)
        dev.open()
        dev.timeout=3*60
        
        cu=Config(dev)
        cu.lock()
        cu.load(template_path=my_conf_file, overwrite=True)
        conf_diff=cu.diff()
     
        if conf_diff:
            print "\nINFO: The following changes will be applied: \n %s" %conf_diff
            
            if cu.commit_check():
                cu.commit()
                print ("\nINFO: The configuration file %s has been preccesed for the device.") % my_conf_file
            else:
                cu.rollback()
                print ("\nERROR: Commit check error!")
                
            cu.unlock()
            dev.close()
                
        else:
            print "\nINFO: No new configuration need to be applied."
            cu.rollback()
            cu.unlock()
            dev.close()
            return False
        
    except Exception, err:
        print("\nError: Encountered exception while deploying configuration:\n %s") % str(err)
        return False 
        
    return True
