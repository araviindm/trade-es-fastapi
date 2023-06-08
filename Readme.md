## Trade-ES-FastAPI store

## .env file

ELASTICSEARCH_URI=elasticsearch_uri_to_connect

## To install dependencies

python -m venv venv  
.\venv\Scripts\activate  
pip install -r requirements.txt

## To run

uvicorn main:app --reload

## API Description


- DB setup (create_trades_index)
    - I created a dummy data from a online JSON generator
    - Used es_odm to change Models into es mappings 
    - Dumped the data from the JSON file to es index
 
- Get Trades (get_trades)
    - Wrote queries for all parameters seperately and kept them as optional
  
- Single Trade (get_trade_by_id)
  - I Queried for an exact match of the trade_id field
  - I also had another approach which will use the elasticsearch's get to fetch by elasticsearch default _id

- Search Trade (search_trades)
    - I used the query_string query to query multiple fields with a wildcard
    - I also had another approach to use multi_match with phrase_prefix
