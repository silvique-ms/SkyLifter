================================================================
# This is a tool to configure and operate a virtual laboratory #
================================================================

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

Files: 
======
- README.txt	
- SkylifterMain.py
- SkylifterSourceFiles 
- SkylifterProjectPresentation
- SkylifterDestFiles

Python Modules:
===============
- SkylifterMainOp         	   		
- SkylifterLabSetup
- SkylifterConfig			
- SkylifterDeploy
- SkylifterDevOp (not ready)
- SkylifterLabSetup
- SkylifterTables					
- SkylifterJSNAPy (not ready)	


TO DO Next:
===========
- CollectTables.py:
	- an interface table with int_name, admin-stat, op-stat, description, protocols, MTU, ip add, iso add	
	- make collect RPC for all the design layers: mpls, bgp, service
- Option 0 - project description
- Skylifter JSNAPy module
- finish all J2 templates: mpls, bgp, service, isis with routing policies, system with RE-FF and all stuf
- Check functions
- Small youtube mouvie with program presentation
- Telemetry interface for vMX - implementat
⁃ Construieste un LSP catre PAG1 cu path bine ales si unul catre PAG2 cu path bine ales pe bucla cu metrica de la igp: va sti singur in ce directie sa ruteze! :)) 

Topics to study:
=============
-> Telemetry
-> InfluxDB
-> Kafka
-> Telegraf
-> Grafana