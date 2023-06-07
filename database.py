from elasticsearch import Elasticsearch
import json
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from model import Trade

load_dotenv()

ELASTICSEARCH_URI = os.getenv('ELASTICSEARCH_URI')
es = Elasticsearch(ELASTICSEARCH_URI)
if es.ping():
    print("Pinged your deployment. You successfully connected to Elasticsearch!")
else:
    print("Error connecting to Elasticsearch!")


def prepare_trades_index():
    """To create the Index, add mappings and add data from the trades.json file"""
    trade_cls = Trade
    trade_mapping = trade_cls._index.to_dict()
    try:
        es.indices.create(
            index="trades", mappings=trade_mapping['mappings'])
    except Exception as e:
        raise HTTPException(e.args[0],
                            detail=e.args[1])

    f = open('trades.json')
    trades = json.load(f)
    for trade in trades:
        try:
            es.index(index="trades", document=trade)
        except Exception as e:
            raise HTTPException(e.args[0],
                                detail=e.args[1])

    # es.indices.delete("trades")

    return {"res": "inserted"}


def fetch_trades(limit: int):
    """To fetch a list of trades"""
    try:
        resp = es.search(index="trades", size=limit, body={
                         "query": {"match_all": {}}})
    except Exception as e:
        raise HTTPException(e.args[0],
                            detail=e.args[1])
    return resp['hits']['hits']


def fetch_trade_by_id(id: str):
    """To fetch a single trade by trade_id or by the default elastic _id(which is commented)"""
    try:
        full_resp = es.search(index="trades", size=1, body={
            "query": {"match": {"trade_id": id}}})
        resp = full_resp['hits']['hits'][0]
        # resp = es.get(index="trades", id=id)
    except Exception as e:
        raise HTTPException(e.args[0],
                            detail=e.args[1])
    return resp


def search_db_trades(search: str):
    """To fetch a single trade by trade_id or by the default elastic _id(which is commented)"""
    try:
        resp = es.search(index="trades", body={
            "query": {"query_string": {
                "query": "*"+search+"*",
                "fields": ["counterparty", "instrument_id", "instrument_name", "trader"]
            }}})
    except Exception as e:
        raise HTTPException(e.args[0],
                            detail=e.args[1])
    return resp['hits']['hits']
