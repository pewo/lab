#!/usr/bin/env python3

import yaml
import os
import sys
import argparse

def read_config(config_file):
   #  str => json
   """ read_config reads a config file and return a json object """
   config = yaml.safe_load(open(config_file))

   print("config: ", config)
   if 'port' in config:
       print("port: ", config['port'])

   if 'directory' in config:
       print("directory: ", config['directory'])



print("script: ", __file__ )
print("dirname: ", os.path.dirname(__file__))

parser = argparse.ArgumentParser(description='Labconf web services')
parser.add_argument("-p", '--port',  type=int, help="Defines which port the services should bind to")
parser.add_argument("-c", '--config',  type=str, help="Where is the config file located (optional)")
parser.add_argument("-d", '--dir',  type=str, help="Where is the datadir located")

args = parser.parse_args()

print("args: ", args)
if args.port: 
    print("port number: ", args.port)

if args.config: 
    print("config file: ", args.config)

if args.dir: 
    print("data directory: ", args.dir)

read_config("/tmp/config.yaml")

