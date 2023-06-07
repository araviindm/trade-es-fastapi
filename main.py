from fastapi import APIRouter, FastAPI, HTTPException
from database import prepare_trades_index
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


routes = APIRouter(
    prefix="/api",
)


@routes.post("/trade")
def create_trades_index():
    response = prepare_trades_index()
    if response:
        return response
    raise HTTPException(404, "Something went wrong")


app.include_router(routes)
