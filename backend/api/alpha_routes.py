from typing import List, Dict

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from decimal import Decimal

from backend.services.alpha_token_service import fetch_alpha_tokens
from backend.services.alpha_price_service import fetch_alpha_price

router = APIRouter(prefix="/api/alpha", tags=["alpha"])


class PriceResponse(BaseModel):
    symbol: str
    price_now: Decimal
    price_avg: Decimal
    price_vwap: Decimal
    timestamp: int


@router.get("/tokens", response_model=List[Dict[str, str]])
async def get_tokens():
    tokens = await fetch_alpha_tokens()
    return tokens


@router.get("/price", response_model=PriceResponse)
async def get_price(alphaId: str = Query(..., description="Alpha token id or symbol")):
    if not alphaId:
        raise HTTPException(status_code=400, detail="alphaId is required")
    try:
        data = await fetch_alpha_price(alphaId)
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
