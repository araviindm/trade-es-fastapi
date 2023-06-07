## Trade-ES-FastAPI store

## To install dependencies

python -m venv venv  
.\venv\Scripts\activate  
pip install -r requirements.txt

## To run

uvicorn main:app --reload

<!-- {
    'properties': {
        'asset_class': {'type': 'text'},
        'counterparty': {'type': 'text'},
        'instrument_id': {'type': 'text'},
        'instrument_name': {'type': 'text'},
        'trade_date_time': {'type': 'date', 'format': 'yyyy-MM-dd HH:mm:ss'},
        'trade_details': {
            'properties': {
                'buySellIndicator': {'type': 'text'},
                'price': {'type': 'float'},
                'quantity': {'type': 'integer'}
            },
            'type': 'object'
        },
        'trade_id': {'type': 'text'},
        'trader': {'type': 'text'}
        }
    } -->

    [

                        # {"match": {
                        #     "trade_details.buySellIndicator": tradeType.name if tradeType else None
                        # }}
                        # {"range": {"trade_date_time": {
                        #     "gte": start if start else "", "lte": end if end else dt.datetime.now()}}},
                    ]
