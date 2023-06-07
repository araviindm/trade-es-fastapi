from elasticsearch import Elasticsearch
import json
import os
from dotenv import load_dotenv

load_dotenv()

ELASTICSEARCH_URI = os.getenv('ELASTICSEARCH_URI')
es = Elasticsearch(ELASTICSEARCH_URI)
if es.ping():
    print("Pinged your deployment. You successfully connected to Elasticsearch!")
else:
    print("Error connecting to Elasticsearch!")


def prepare_trades_index():
    f = open('trades.json')
    trades = json.load(f)
    for trade in trades:
        response = es.index(index='trades', document=trade)
        print(response)
    return {"res": "inserted"}
