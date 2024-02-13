# encoding: utf-8

from pydantic import BaseModel
from starlette.responses import PlainTextResponse

from helper import get_kas_market_data, get_kas_price
from server import app


class PriceResponse(BaseModel):
    price: float = 0.025235


@app.get("/info/price", response_model=PriceResponse | str, tags=["Raspa network info"])
async def get_price(stringOnly: bool = False):
    """
    Returns the current price for Raspa in USD.
    """
    if stringOnly:
        return PlainTextResponse(content=str(await get_kas_price()))

    return {"price": await get_kas_price()}


@app.get("/info/market-data",
         tags=["Raspa network info"],
         include_in_schema=False)
async def get_market_data():
    """
    Returns market data for raspa.
    """
    return await get_kas_market_data()
