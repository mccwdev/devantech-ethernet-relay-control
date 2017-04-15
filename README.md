# devantech-ethernet-relay-control
Control your Devantech programmable Ethernet Relay such as http://www.robot-electronics.co.uk/ds1242.html

### Usage 

Example, turn on relay 1:

    $ relay_control.py 1 on
    

Commandline options

    $ relay_control.py [-h] [--host HOST] [--port PORT] relay_id command
     
    Control Devantech Ethernet Relays
     
    positional arguments:
      relay_id     ID number of relay
      command      Command: 'on' or 'off'
     
    optional arguments:
      -h, --help   show this help message and exit
      --host HOST  Hostname or IP-address of Ethernet Relay Control device
      --port PORT  Control port of Ethernet Relay Control device


### Advanced relay control

See updatecron.py for an implementation example. Control external lights