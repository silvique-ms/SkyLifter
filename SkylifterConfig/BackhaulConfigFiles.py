#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""A library with specific function to generate variable and configuration files for Backhaul project """

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

import re, openpyxl, pprint, yaml

from time import strftime
from jinja2 import Template


def jinja2conf (jinja2file, yamlfile, conffile, foldername):
    
    ####################################################
    # Create configuration file using junja2 template  # 
    # and yaml variable files. Safe the configuration  # 
    # .conf on specified folder.                       #
    ####################################################
    
    try:   
        
        conffile=strftime("%Y.%m.%d_%H.%M.%S")+' - '+conffile+'.conf'
        full_file_path=foldername+'/'+conffile
        
        # Open and read file with variables
        yaml_file = open(yamlfile, 'r')
        variables = yaml.load(yaml_file.read())
        yaml_file.close()
    
        # Open and read file with template
        jinja2_file = open(jinja2file, 'r')
        template = Template(jinja2_file.read())
        jinja2_file.close()
    
        # Create and write final configuration
        conf_file = open(full_file_path, 'w')
        conf_file.write(template.render(variables))
        conf_file.close()
        
    except Exception,err:
        print("\nError: Encountered exception while creating configuration file %s from yaml variable file %s and jinja2 template file %s: \n%s\n")%(conffile, yamlfile, jinja2file, str(err))
        return False
    
    return conffile

def inet2iso(ipv4_address, iso_area, iso_net = '00'):

    ######################################################################
    # Obtain the iso address from ipv4 address needed for IS-IS protocol #                                    #
    ######################################################################

    ipv4_blocks = ipv4_address.split('.')
    for i in range(0,len(ipv4_blocks)):
        while len(ipv4_blocks[i]) < 3:
            ipv4_blocks[i] = '0' + ipv4_blocks[i]
        
    iso_sys_id = ''.join(ipv4_blocks)
    iso_sys_id = iso_area + '.' + '.'.join(re.findall('\d\d\d\d', iso_sys_id)) + '.' + iso_net
   
    return iso_sys_id

def system_xlsx2yaml2py (xlsxfile, sheetname, yamlfile, pyfile):
    
    #######################################################################################
    # Take as input an excel .xlsx file and generates system variable .yaml and .py files #
    #######################################################################################
    
    try: 
        
        print ('''
INFO: Opening workbook... and start creating system .yaml and .py variable files!
=================================================================================
        ''')
        wb = openpyxl.load_workbook(xlsxfile)
        sheet = wb.get_sheet_by_name(sheetname)
    
        LogicalSystemsData = {}
        LogicalSystemsData.setdefault('Logical_systems', {})

        print ('\nINFO: Reading rows...')   
        for row in range(2, sheet.max_row + 1):
            hostname = str(sheet['A'+ str(row)].value)
            
            if hostname != 'None':
                ifd_val = str(sheet['B'+ str(row)].value)
                ifl_val = str(sheet['C'+ str(row)].value)
                ifa_val = str(sheet['D'+ str(row)].value)
                mask_val = str(sheet['E'+ str(row)].value)
                iff_val = str(sheet['F'+ str(row)].value)
                desc_val = str(sheet['G'+ str(row)].value)
                area_val = str(sheet['H'+ str(row)].value)
    
                # Make sure the key for this hostname exists. If key exist, the function makes nothing. 
                LogicalSystemsData['Logical_systems'].setdefault(hostname, {})
                # Make sure the key for this ifd in this hostname exists. If key exist, the function makes nothing. 
                if_val = ifd_val+'.'+ifl_val
                LogicalSystemsData['Logical_systems'][hostname].setdefault(if_val, {'ifd':None, 'ifl':None, 'ipv4_ifa':None, 'ipv4_cidr':None, 'iff':None, 'description':None})

                LogicalSystemsData['Logical_systems'][hostname][if_val]['ifd'] = ifd_val
                LogicalSystemsData['Logical_systems'][hostname][if_val]['ifl'] = ifl_val
                LogicalSystemsData['Logical_systems'][hostname][if_val]['ipv4_ifa'] = ifa_val
                LogicalSystemsData['Logical_systems'][hostname][if_val]['ipv4_cidr'] = mask_val
                LogicalSystemsData['Logical_systems'][hostname][if_val]['iff'] = iff_val
                LogicalSystemsData['Logical_systems'][hostname][if_val]['description'] = desc_val
                
                if ifd_val == 'lo0' and 'iso' in iff_val:
                    iso_ifa_val = inet2iso(ifa_val, area_val)
                    LogicalSystemsData['Logical_systems'][hostname][if_val]['iso_ifa'] = iso_ifa_val
    
    except Exception, err:
        print("\nError: Encountered exception while deploying configuration:\n %s") % str(err)
        return False
    
    try: 
        
        print ('\nINFO: Writing results in .py file...')
        resultPyFile = open(pyfile, 'w')
        resultPyFile.write('---\n ' + pprint.pformat(LogicalSystemsData))
        resultPyFile.close()
    
    except Exception, err:
        print("\nError: Encountered exception while writing results in .py file:\n %s") % str(err)
        return False
    
    try: 
        
        print ('\nINFO: Writing results in .yaml file...')
        resultYAMLFile = open(yamlfile, 'w')
        resultYAMLFile.write('---\n\n' + yaml.dump(LogicalSystemsData, default_flow_style=False))
        resultYAMLFile.close()
    
    except Exception, err:
        print("\nError: Encountered exception while writing results in .yaml file:\n %s") % str(err)
        return False   
    
    print('\nINFO: Done! ')
    
    return True

def mpls_xlsx2yaml2py (xlsxfile, sheetname, yamlfile, pyfile):
    
    #######################################################################################
    # Take as input an excel .xlsx file and generates mpls variable .yaml and .py files   #
    #######################################################################################
    

    try: 
    
        print ('''
INFO: Opening workbook... and start creating mpls .yaml and .py variable files!
=================================================================================
        ''')
        wb = openpyxl.load_workbook(xlsxfile)
        sheet = wb.get_sheet_by_name(sheetname)
    
        LSPData = {}
        LSPData.setdefault('LSPs', {})

        print ('\nINFO: Reading rows...')  
        for row1 in range(2, sheet.max_row + 1):
            source_ifd_val = str(sheet['B'+ str(row1)].value)
            if source_ifd_val == 'lo0':
                source_hostname = str(sheet['A'+ str(row1)].value)
                from_val = str(sheet['D'+ str(row1)].value)

                # Make sure the key for this hostname exists. If key exist, the function makes nothing. 
                LSPData['LSPs'].setdefault(source_hostname, {})


                for row2 in range(2, sheet.max_row +1):
                    destination_hostname = str(sheet['A'+ str(row2)].value)
                    destination_ifd_val = str(sheet['B'+ str(row2)].value)
                
                    if destination_ifd_val == 'lo0' and destination_hostname != source_hostname:
                        to_val = str(sheet['D'+ str(row2)].value)
                        lsp_name_val = source_hostname + '_to_' + destination_hostname
                        
                        if ('MA' in source_hostname and 'PAG' in destination_hostname) or ('PAG' in source_hostname and 'Core' not in destination_hostname) or ('AG' in source_hostname and 'MA' not in destination_hostname) or ('Core' in source_hostname and 'AG' in destination_hostname and 'PAG' not in destination_hostname):
                            LSPData['LSPs'][source_hostname].setdefault(lsp_name_val, {'from':None, 'to':None }) #, 'primary_path_name':None, 'secondary_path_name':None, 'primary_path_ip':None, 'secondary_path_ip':None})

                            LSPData['LSPs'][source_hostname][lsp_name_val]['from'] = from_val
                            LSPData['LSPs'][source_hostname][lsp_name_val]['to'] = to_val
     
    except Exception, err:
        print("\nError: Encountered exception while reading .xlsx file:\n %s") % str(err)
        return False           

    try: 
        print ('\nINFO: Writing results in .py file...')
        resultPyFile = open(pyfile, 'w')
        resultPyFile.write('---\n ' + pprint.pformat(LSPData))
        resultPyFile.close()
    
    except Exception, err:
        print("\nError: Encountered exception while writing results in .py file:\n %s") % str(err)
        return False

    try: 
        print ('\nINFO: Writing results in .yaml file...')
        resultYAMLFile = open(yamlfile, 'w')
        resultYAMLFile.write('---\n\n' + yaml.dump(LSPData, default_flow_style=False))
        resultYAMLFile.close()
    
    except Exception, err:
        print("\nError: Encountered exception while writing results in .yaml file:\n %s") % str(err)
        return False
    
    print('\nINFO: Done! ')
    
    return True

def bgp_xlsx2yaml2py (xlsxfile, sheetname, yamlfile, pyfile):

    #######################################################################################
    # Take as input an excel .xlsx file and generates bgp variable .yaml and .py files #
    #######################################################################################

    try: 
    
        print ('''
INFO: Opening workbook... and start creating bgp .yaml and .py variable files!
=================================================================================
        ''')
        wb = openpyxl.load_workbook(xlsxfile)
        sheet = wb.get_sheet_by_name(sheetname)
    
        BGPData = {}
        BGPData.setdefault('BGP_values', {})

        print ('\nINFO: Reading rows...')   
        for row1 in range(2, sheet.max_row + 1):
            local_ifd_val = str(sheet['B'+ str(row1)].value)
            if local_ifd_val == 'lo0':
                local_hostname = str(sheet['A'+ str(row1)].value)
                local_ip_val = str(sheet['D'+ str(row1)].value)

                # Make sure the key for this hostname exists. If key exist, the function makes nothing. 
                BGPData['BGP_values'].setdefault(local_hostname, {})

                for row2 in range(2, sheet.max_row +1):
                    peer_hostname = str(sheet['A'+ str(row2)].value)
                    peer_ifd_val = str(sheet['B'+ str(row2)].value)
                
                    if peer_ifd_val == 'lo0' and peer_hostname != local_hostname:
                        peer_ip_val = str(sheet['D'+ str(row2)].value)
                        
                        if ('MA' in local_hostname and 'PAG' in peer_hostname):
                            BGPData['BGP_values'][local_hostname].setdefault('to-PAG-RR', {})
                        
                            BGPData['BGP_values'][local_hostname]['to-PAG-RR']['local-ip'] = local_ip_val
                            BGPData['BGP_values'][local_hostname]['to-PAG-RR'][peer_hostname] = peer_ip_val
                            
                        if ('PAG' in local_hostname and 'MA' in peer_hostname):
                            BGPData['BGP_values'][local_hostname].setdefault('to-MA-Clients', {})
                        
                            BGPData['BGP_values'][local_hostname]['to-MA-Clients']['local-ip'] = local_ip_val
                            BGPData['BGP_values'][local_hostname]['to-MA-Clients'][peer_hostname] = peer_ip_val
                        
                        if ('PAG' in local_hostname and 'MA' not in peer_hostname and 'PAG' not in peer_hostname and 'Core' not in peer_hostname):
                            BGPData['BGP_values'][local_hostname].setdefault('to-AG-RR', {})
                        
                            BGPData['BGP_values'][local_hostname]['to-AG-RR']['local-ip'] = local_ip_val
                            BGPData['BGP_values'][local_hostname]['to-AG-RR'][peer_hostname] = peer_ip_val
                        
                        if ('PAG' in local_hostname and 'PAG' in peer_hostname):
                            BGPData['BGP_values'][local_hostname].setdefault('to-PAG', {})
                        
                            BGPData['BGP_values'][local_hostname]['to-PAG']['local-ip'] = local_ip_val
                            BGPData['BGP_values'][local_hostname]['to-PAG'][peer_hostname] = peer_ip_val
                        
                        if ('PAG' not in local_hostname and 'MA' not in local_hostname and 'Core' not in local_hostname and 'PAG' in peer_hostname):
                            BGPData['BGP_values'][local_hostname].setdefault('to-PAG-Clients', {})
                        
                            BGPData['BGP_values'][local_hostname]['to-PAG-Clients']['local-ip'] = local_ip_val
                            BGPData['BGP_values'][local_hostname]['to-PAG-Clients'][peer_hostname] = peer_ip_val
                        
                        if ('PAG' not in local_hostname and 'MA' not in local_hostname and 'Core' not in local_hostname and 'PAG' not in peer_hostname and 'MA' not in peer_hostname and 'Core' not in peer_hostname):
                            BGPData['BGP_values'][local_hostname].setdefault('to-AG', {})
                        
                            BGPData['BGP_values'][local_hostname]['to-AG']['local-ip'] = local_ip_val
                            BGPData['BGP_values'][local_hostname]['to-AG'][peer_hostname] = peer_ip_val
                        
                        if ('PAG' not in local_hostname and 'MA' not in local_hostname and 'Core' not in local_hostname and 'Core' in peer_hostname):
                            BGPData['BGP_values'][local_hostname].setdefault('to-Core-RR', {})
                        
                            BGPData['BGP_values'][local_hostname]['to-Core-RR']['local-ip'] = local_ip_val
                            BGPData['BGP_values'][local_hostname]['to-Core-RR'][peer_hostname] = peer_ip_val
                        
                        if ('Core' in local_hostname and 'MA' not in peer_hostname and 'PAG' not in peer_hostname and 'Core' not in peer_hostname):
                            BGPData['BGP_values'][local_hostname].setdefault('to-AG-Clients', {})
                        
                            BGPData['BGP_values'][local_hostname]['to-AG-Clients']['local-ip'] = local_ip_val
                            BGPData['BGP_values'][local_hostname]['to-AG-Clients'][peer_hostname] = peer_ip_val
                        
                                        
                  
    except Exception, err:
        print("\nError: Encountered exception while reading .xlsx file:\n %s") % str(err)
        return False           

    try: 
        print ('\nINFO: Writing results in .py file...')
        resultPyFile = open(pyfile, 'w')
        resultPyFile.write('---\n ' + pprint.pformat(BGPData))
        resultPyFile.close()
    
    except Exception, err:
        print("\nError: Encountered exception while writing results in .py file:\n %s") % str(err)
        return False

    try: 
        print ('\nINFO: Writing results in .yaml file...')
        resultYAMLFile = open(yamlfile, 'w')
        resultYAMLFile.write('---\n\n' + yaml.dump(BGPData, default_flow_style=False))
        resultYAMLFile.close()
    
    except Exception, err:
        print("\nError: Encountered exception while writing results in .yaml file:\n %s") % str(err)
        return False
    
    print('\nINFO: Done! ')
    
    return True
