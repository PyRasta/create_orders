from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from pydantic import BaseModel, Field, validator

from bot import run


class Data(BaseModel):
    side: str = Field(max_length=4, min_length=3)
    symbol: str = Field(max_length=10, min_length=1)
    volume: float = Field(gt=0)
    number: int = Field(gt=0)
    price_min: float = Field(gt=0)
    price_max: float = Field(gt=0)
    amount_dif: float = Field(gt=0)

    @validator('amount_dif')
    def validate_amount_dif(cls, amount_dif, values) -> float:
        if 'volume' in values and 'number' in values and values['volume'] / values['number'] <= amount_dif:
            raise ValueError('amount_dif must be less than the difference between volume and number')
        return amount_dif
    
    @validator('side')
    def validate_side(cls, side, values) -> str:
        if side.upper() != 'SELL' and side.upper() != 'BUY':
            raise ValueError('side must be equal to SELL or BUY')
        return side.upper()

    @validator('price_max')
    def validate_price_max(cls, price_max, values) -> float:
        if 'price_min' in values and price_max <= values['price_min']:
            raise ValueError('price_max must be greater than price_min')
        return price_max
    
    @validator('symbol')
    def validate_symbol(cls, symbol, values) -> str:
        return symbol.upper()
    

app = FastAPI()


@app.get('/')
async def home():
    return FileResponse('templates/index.html')

@app.post('/get_data')
async def get_data(data: Data):
    result = run(data)
    output = {'message': result}
    return output