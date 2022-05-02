#!/usr/bin/python3
# Author : Jonathan Roco

import requests,json,sys,hashlib,os,time,threading,logging,sched
from flask import Flask, make_response, request
from flask_restful import Api, Resource, reqparse
from datetime import datetime
import configparser
import socket

api01 = Flask(__name__)
api = Api(api01)

#############################
# Reading Configuration
#############################
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
fileconfig = '../conf/api01.conf'
config = configparser.ConfigParser()
config.read(fileconfig)
Api01Version=config.get("global","Api01Version")
Api01Port=int(config.get("global","Api01Port"))


class loader(Resource):
        def post(self):
            threadName=threading.current_thread()
            logging.info('[loader] #################### Initial Messages ####################')
            logging.info('[loader] [POST] method Reached Thread Number: %s Thread Ident %s',threading.current_thread(),threading.get_ident())
            return 


###################### Main Loop ######################
if __name__ == '__main__':
        logging.basicConfig(filename='../log/Api01.log',format='%(asctime)s.%(msecs)03d %(threadName)s %(message)s', datefmt='%Y%m%d %H:%M:%S', level=logging.INFO)
        logging.info('**** Starting Appliaton API for Globant (V%s) (Info Level)',Api01Version)
        api.add_resource(loader ,'/loader')
        api01.run(host=local_ip,port=Api01Port,threaded=True,debug=False)
