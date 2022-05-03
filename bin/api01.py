#!/usr/bin/python3
# Author : Jonathan Roco

import requests,json,sys,hashlib,os,time,threading,logging,sched
from flask import Flask, make_response, request
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from dateutil.parser import *
import configparser
import socket
import mariadb

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

def loadData(query):
    # This function must be implemented in other way (only one connection when app start)
    # Open Connection with MariaDB
    logging.info('Entering to loadData function with query: %s', query)
    try:
        conn = mariadb.connect(
        user = os.getenv('DBUSER'),
        password = os.getenv('DBPASSWORD'),
        host = os.getenv('DBHOST'),
        port = int(os.getenv('DBPORT')),
        database = os.getenv('DBNAME')
        )
    except mariadb.Error as e:
        logging.info('[loadData] WARNING: "Error connecting to MariaDB Platform: {e}"')
        sys.exit(1)
    # Get Cursor
    cur = conn.cursor()
    cur.execute(query)
    logging.info('[loadData] Count Cursor: %s',cur.rowcount)
    conn.commit()
    conn.close()
    return 

class loader(Resource):
        def post(self):
            threadName=threading.current_thread()
            logging.info('[loader] #################### Initial Messages ####################')
            logging.info('[loader] [POST] method Reached Thread Number: %s Thread Ident %s',threading.current_thread(),threading.get_ident())
            # Read the JSON file
            if request.is_json:
                logging.info('[loader] request data: %s',request.data)
                argumentINB = request.data
                string01 = argumentINB.decode('utf-8')
                json01 = json.loads(string01)
                logging.info('[loader] type json01: %s size %s',type(json01),len(json01))
                if len(json01) > 1001:
                    dataresponse = {'Response':'Too much lines'}
                    resp = make_response(dataresponse.json())
                    resp.status_code = 400
                    return resp
                for record in json01:
                    logging.info('[loader] record: %s',record)
                    try:
                        logging.info('[loader] txnType: %s id: %s ',record['txnType'],record['id'])
                        txnType = record['txnType']
                    except Exception as e:
                        logging.info('[loader] [ERROR] Argument error %s',str(e))
                        dataresponse = {'Response':'No instance incoming for this messages.'}
                        resp = make_response(dataresponse.json())
                        resp.status_code = 400
                        return resp
                    recordIsues = {}
                    if txnType == "job":
                        query=''
                        logging.info('[loader] JOB formatter')
                        try:
                            query = f"INSERT INTO company.job values('{record['id']}','{record['job']}')"
                        except Exception as e:
                            logging.info('[loader] ERROR Possibly not enought variables %e',e)
                            pass
                        try:
                            loadData(query)
                        except Exception as e:
                            logging.info('[loader] [ERROR] Trying to load record to DB: %s', e)
                            pass
                    elif txnType == "department":
                        query=''
                        logging.info('[loader] DEPARTMENT formatter')
                        try:
                            query = f"INSERT INTO company.department values('{record['id']}','{record['department']}')"
                        except Exception as e:
                            logging.info('[loader] ERROR Possibly not enought variables %e',e)
                            pass
                        try:
                            loadData(query)
                        except Exception as e:
                            logging.info('[loader] [ERROR] Trying to load record to DB: %s', e)
                            pass
                    elif txnType == "employee":
                        query=''
                        logging.info('[loader] EMPLOYEE formatter')
                        try:
                            now=parse(record['datetime'])
                            date01=now.strftime("%y-%m-%d %H:%M:%S")
                            query = f"INSERT INTO company.employee values(null,'{record['name']}','{date01}','{record['department_id']}','{record['job_id']}')"
                        except Exception as e:
                            logging.info('[loader] ERROR Possibly not enought variables %s',e)
                            pass
                        try:
                            loadData(query)
                        except Exception as e:
                            logging.info('[loader] [ERROR] Trying to load record to DB: %s', e)
                            pass

                    else:
                        logging.info('[loader] [ERROR] Txn not identified')
                        dataresponse = {'Response':'Txn not identified.'}
                        resp = make_response(dataresponse.json())
                        resp.status_code = 400
                        return resp
                dataresponse = {'Response':'Ok'}
                resp = make_response(dataresponse)
                resp.status_code = 200
                return resp
                # data format { 'txnType':'employee/job/department', data }
                # Check conditions (format and number of files)
                # data format { 'type':'employee/job/department', data }
                # Insert to database if error log into a batch file
            else:
                logging.info('[loader] No JSON Object detected!')
            return 

###################### Main Loop ######################
if __name__ == '__main__':
        logging.basicConfig(filename='../log/Api01.log',format='%(asctime)s.%(msecs)03d %(threadName)s %(message)s', datefmt='%Y%m%d %H:%M:%S', level=logging.INFO)
        logging.info('**** Starting Appliaton API for Globant (V%s) (Info Level)',Api01Version)
        api.add_resource(loader ,'/loader')
        api01.run(host=local_ip,port=Api01Port,threaded=True,debug=False)
