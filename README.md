# Lab configuration

This playbook uses a git repositry to manage local network configuration

Layout:

repo/<fqdn>/config
------------------

interface: ens19
network: 10.0.0.129/24
routing: 192.168.100.0/24 10.0.0.129

# interrface
This is the name of the interface

# network
Which network address should the interface use

# routing ( optional )
If this is defined, add the route to interface routing

