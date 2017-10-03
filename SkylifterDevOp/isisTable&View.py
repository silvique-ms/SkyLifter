import sys
from junos import Device
from junos.exception import *
"""from SkylifterTables.isis import IsisAdjacencyTable

try: 
    dev = Device (host = '172.16.226.10', user = 'msilvia', passwd = 'SilviaMurgescu')
    dev.open()

    isis_adj = IsisAdjacencyTable(dev).get()

    for adj in isis_adj:
        print ("{}:    {}    {}".format(adj.interface_name, adj.system_name, adj.level))

    dev.close()

except ConnectAuthError:
    print "Authentication Error!"
    sys.exit()
except Exception as error:
    print "There are a lot more exceptions to cover"
    print error
    sys.exit()"""