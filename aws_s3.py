import sys, os
from pprint import pprint
from functools import wraps
import boto3
import botocore
import pandas as pd
import numpy as np
# ---------------------------------------------------------------
s3 = boto3.resource('s3')
client = boto3.client('s3')
  
def set_s3_bucket(bkt_name: str) -> dict:
    def read_s3_data(f: callable):
        """read s3 records"""
        @wraps(f)
        def wrapper(*args, **kwargs):
            func = f(*args, **kwargs)
            s3_dict = dict()
            for i, _ in enumerate(func):
                obj_ = client.get_object(Bucket=str(bkt_name), Key=func[i])
                body_ = obj_['Body']\
                                .read()\
                                .decode('utf-8')
                s3_dict.update({func[i]: body_})
            return s3_dict
        return wrapper
    return read_s3_data

@set_s3_bucket(bkt_name='mha-nyc-poc-logstash-output-bucket')       
def get_s3_objects(bkt_name: str, chunksize: int) -> list:
    """get a list of json records"""
    bucket = s3.Bucket(str(bkt_name))
    s3_bkts = list()
    n_chunk = 0
    for obj in bucket.objects.filter(Prefix='http-2'):
        s3_bkts.append(obj.key)
        n_chunk += 1
        if n_chunk >= chunksize:
            return s3_bkts        
# ---------------------------------------------------------------
def main():
    west_s3_json = get_s3_objects(bkt_name='mha-nyc-poc-logstash-output-bucket', chunksize=2)
    print(west_s3_json)
    
if __name__=='__main__':
