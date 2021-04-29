import elytica_dss as edss
from configparser import ConfigParser
from os import path
import time
import json
import logging
import sys
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)
config = ConfigParser()
config_path = 'config.ini'
key=''
if path.exists(config_path):
  config.read(config_path)
  if 'elytica' in config.sections() and 'key' in config['elytica']:
    key = config['elytica']['key']

def fcb(data):
  if json.loads(data)['finished']:
    print("finished...")

def stdcb(data):
  print(json.loads(data)['stdout'])

service = edss.Service(key)
service.login()
service.selectProjectByName('Untitled')
service.selectJobByName('Untitled')
service.queueJob(finished_callback=fcb, stdout_callback=stdcb)
while True:
  time.sleep(1)
