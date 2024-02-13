# encoding: utf-8
import hashlib
from datetime import datetime, timedelta
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from dbsession import async_session
from models.Transaction import Transaction
from server import app, kaspad_client


class RaspadResponse(BaseModel):
    raspadHost: str = ""
    serverVersion: str = "0.12.6"
    isUtxoIndexed: bool = True
    isSynced: bool = True
    p2pId: str = "1231312"


class HealthResponse(BaseModel):
    raspadServers: List[RaspadResponse]


@app.get("/info/health", response_model=HealthResponse, tags=["Raspa network info"])
async def health_state():
    """
    Returns the current hashrate for Raspa network in TH/s.
    """
    await kaspad_client.initialize_all()

    raspads = []

    async with async_session() as s:
        last_block_time = (await s.execute(select(Transaction.block_time)
                                           .limit(1)
                                           .order_by(Transaction.block_time.desc()))).scalar()

    time_diff = datetime.now() - datetime.fromtimestamp(last_block_time / 1000)

    if time_diff > timedelta(minutes=10):
        raise HTTPException(status_code=500, detail="Transactions not up to date")

    for i, kaspad_info in enumerate(kaspad_client.kaspads):
        raspads.append({
            "isSynced": kaspad_info.is_synced,
            "isUtxoIndexed": kaspad_info.is_utxo_indexed,
            "p2pId": hashlib.sha256(kaspad_info.p2p_id.encode()).hexdigest(),
            "raspadHost": f"RASPAD_HOST_{i + 1}",
            "serverVersion": kaspad_info.server_version
        })

    return {
        "raspadServers": raspads
    }
