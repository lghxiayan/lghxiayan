import os
import configparser

os.environ['PYTHONIOENCODING'] = 'utf-8'

config = configparser.ConfigParser()
config['DEFAULT'] = {'ServerAliveInterval': '145',
                     'Compression': 'yes',
                     'CompressionLevel': '9'}

config['forge.example'] = {}
config['forge.example']['User'] = 'hg'
config['topsecret.server.example'] = {}
topsecret = config['topsecret.server.example']
topsecret['Port'] = '50022'  # 更改解析器
topsecret['ForwardX11'] = 'no'  # same here
config['DEFAULT']['ForwardX11'] = 'yes'

with open('example.ini', 'w') as configfile:
    config.write(configfile)

print(config.sections())
