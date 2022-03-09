RudicsReroute
-------------

This is a simple module that allows you to reroute network traffic from 
one port to another. Something along the lines

```
mkfifo pipe

nc -l -p 6565 <pipe | nc 192.168.0.104 8181 >pipe

```

except that the python version does not need respawning each time the
connection drops, and can handle multiple connections.
