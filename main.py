import datetime as dt
from typing import Optional
from fastapi import APIRouter, FastAPI, HTTPException
from database import (prepare_trades_index, fetch_trades,
                      fetch_trade_by_id, search_db_trades)
from model import BuySellIndicator
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


routes = APIRouter(
    prefix="/api",
)


@routes.get("/trades")
def get_trades(
        limit: Optional[int] | None = None,
        assetClass: Optional[str] | None = None,
        minPrice: Optional[int] | None = None,
        maxPrice: Optional[int] | None = None,
        start: Optional[dt.datetime] | None = None,
        end: Optional[dt.datetime] | None = None,
        tradeType: Optional[BuySellIndicator] | None = None):
    response = fetch_trades(limit, assetClass, minPrice,
                            maxPrice, start, end, tradeType)
    if response:
        return response
    raise HTTPException(404, "Something went wrong")


@routes.post("/trades")
def create_trades_index():
    response = prepare_trades_index()
    if response:
        return response
    raise HTTPException(404, "Something went wrong")


@routes.get("/trade")
def get_trade_by_id(id: str):
    response = fetch_trade_by_id(id)
    if response:
        return response
    raise HTTPException(404, "Something went wrong")


@routes.get("/trades/search")
def search_trades(search: str):
    response = search_db_trades(search)
    if response:
        return response
    raise HTTPException(404, "Something went wrong")


app.include_router(routes)
