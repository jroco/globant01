#!/usr/bin/python3
# Author : Jonathan Roco

import requests,json,sys,hashlib,os,time,threading,logging,sched
from flask import Flask, make_response, request
from flask_restful import Api, Resource, reqparse
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError,ConnectionFailure
from datetime import datetime
from requests.exceptions import Timeout
from urllib3.exceptions import HTTPError as BaseHTTPError
from bson.json_util import dumps
import urllib.parse
import socket
from influxdb import InfluxDBClient
import io, PIL.Image as Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
import configparser
import shutil
import base64
import boto3
import re
import pika
import pickle

api01 = Flask(__name__)
api = Api(api01)
scheduler = sched.scheduler(time.time, time.sleep)


