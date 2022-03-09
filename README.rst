RudicsReroute
-------------

This is a simple module that allows you to reroute network traffic from 
one port to another. Something along the lines

`$ mkfifo pipe`

`$ nc -l -p 6565 <pipe | nc 192.168.0.104 8181 >pipe`

except that the python version does not need respawning each time the
connection drops, and can handle multiple connections.

After installation (`python setup.py install --user` or something similar) you can reroute the 
network traffic as

`$ rudicsrerouter 6565 192.168.0.104 8181`

which would forward all traffic arriving at 6565 to 192.168.0.104:8181, allowing bi-directional communication.
