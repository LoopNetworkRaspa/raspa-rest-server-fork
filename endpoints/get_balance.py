# encoding: utf-8
import os

from fastapi import HTTPException, Path
from pydantic import BaseModel

from server import app, kaspad_client

ADDRESS_TYPE = os.getenv("ADDRESS_TYPE")
REGEX = os.getenv("REGEX")


class BalanceResponse(BaseModel):
    address: str = "kaspa:pzhh76qc82wzduvsrd9xh4zde9qhp0xc8rl7qu2mvl2e42uvdqt75zrcgpm00"
    balance: int = 38240000000


@app.get(
    "/addresses/{kaspaAddress}/balance",
    response_model=BalanceResponse,
    tags=["Kaspa addresses"],
)
async def get_balance_from_kaspa_address(
    kaspaAddress: str = Path(
        description=f"Kaspa address as string e.g. {ADDRESS_TYPE}:qr0tcyacqqvglzzn6pz3qggjarvwkcfaesc96mnapr6p54pp9k00yszc2cz2g",
        # regex="^kaspacustom\:[a-z0-9]{61,63}$",
        regex=REGEX,
    )
):
    """
    Get balance for a given kaspa address
    """
    resp = await kaspad_client.request(
        "getBalanceByAddressRequest", params={"address": kaspaAddress}
    )

    try:
        resp = resp["getBalanceByAddressResponse"]
    except KeyError:
        if (
            "getUtxosByAddressesResponse" in resp
            and "error" in resp["getUtxosByAddressesResponse"]
        ):
            raise HTTPException(
                status_code=400, detail=resp["getUtxosByAddressesResponse"]["error"]
            )
        else:
            raise

    try:
        balance = int(resp["balance"])

    # return 0 if address is ok, but no utxos there
    except KeyError:
        balance = 0

    return {"address": kaspaAddress, "balance": balance}
