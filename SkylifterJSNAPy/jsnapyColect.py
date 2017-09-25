#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

### Example showing how to pass yaml data in same file ###
from jsnapy import SnapAdmin
from pprint import pprint
# from junos import Device

js = SnapAdmin()

config_data = """
hosts:
  - device: 172.16.226.10
    username : silvia
    passwd: SilviaMurgescu
tests:
  - collect_isis.yml
    #format: text
"""

#snapchk = js.snapcheck(config_data, "pre")
snapchk = js.snap(config_data, "pre")
pprint (snapchk)
'''for val in snapchk:
    print "Tested on", val.device
    print "Final result: ", val.result
    print "Total passed: ", val.no_passed
    print "Total failed:", val.no_failed
    pprint(dict(val.test_details))'''
