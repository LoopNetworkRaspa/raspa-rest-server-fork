# encoding: utf-8

from pydantic import BaseModel

from server import app, kaspad_client


class KaspadInfoResponse(BaseModel):
    mempoolSize: str = "1"
    serverVersion: str = "0.12.2"
    isUtxoIndexed: bool = True
    isSynced: bool = True


@app.get("/info/kaspad", response_model=KaspadInfoResponse)
async def get_kaspad_info():
    """
    Retrieves some kaspad information for kaspad instance, which is currently connected.
    """
    resp = kaspad_client.request("getInfoRequest")
    resp["getInfoResponse"].pop("p2pId")
    return resp["getInfoResponse"]
