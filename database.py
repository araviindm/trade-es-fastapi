import datetime as dt
from typing import Optional
from elasticsearch import Elasticsearch
import json
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from model import BuySellIndicator, Trade

load_dotenv()

ELASTICSEARCH_URI = os.getenv('ELASTICSEARCH_URI')
es = Elasticsearch(ELASTICSEARCH_URI)
if es.ping():
    print("Pinged your deployment. You successfully connected to Elasticsearch!")
else:
    print("Error connecting to Elasticsearch!")


def prepare_trades_index():
    """To create the Index, add mappings and add data from the trades.json file"""
    mapping = {
        'properties': {
            'asset_class': {'type': 'text'},
            'counterparty': {'type': 'text'},
            'instrument_id': {'type': 'text'},
            'instrument_name': {'type': 'text'},
            'trade_date_time': {'type': 'date'},
            'trade_details': {
                'properties': {
                    'buySellIndicator': {'type': 'keyword'},
                    'price': {'type': 'float'},
                    'quantity': {'type': 'integer'}
                },
                'type': 'object'
            },
            'trade_id': {'type': 'text'},
            'trader': {'type': 'text'}
        }}
    try:
        es.indices.create(
            index="trades", mappings=mapping)
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


def fetch_trades(limit: Optional[int], assetClass: Optional[str], minPrice: Optional[int],
                 maxPrice: Optional[int], start: Optional[dt.datetime], end: Optional[dt.datetime], tradeType: Optional[BuySellIndicator]):
    """To fetch a list of trades"""
    if tradeType:
        print(tradeType.name)
    try:
        resp = es.search(index="trades", size=limit, body={
            "query": {
                "bool": {
                    "must": [
                        {"range": {"trade_details.price": {
                            "gte": minPrice, "lte": maxPrice}}},

                        {"prefix": {"asset_class": {
                            "value": assetClass if assetClass else ""
                        }}},
                        # {"match": {
                        #     "trade_details.buySellIndicator": tradeType.name if tradeType else None
                        # }}
                        # {"range": {"trade_date_time": {
                        #     "gte": start if start else "", "lte": end if end else dt.datetime.now()}}},
                    ],
                }
            }})
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
    """search on counterparty, instrument_id, instrument_name, trader"""
    try:
        resp = es.search(index="trades", body={
            "query": {"query_string": {
                "query": "*"+search+"*",
                "fields": ["counterparty", "instrument_id", "instrument_name", "trader"]
            }}})

        """This matches only prefix from search text"""
        # resp = es.search(index="trades", body={
        #     "query": {"multi_match": {
        #         "query": search,
        #         "fields":["counterparty", "instrument_id", "instrument_name", "trader"],
        #         "type": "phrase_prefix"
        #     }}})
    except Exception as e:
        raise HTTPException(e.args[0],
                            detail=e.args[1])
    return resp['hits']['hits']
