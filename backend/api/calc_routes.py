from decimal import Decimal
from typing import Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.calculation_service import compute_diff_range

router = APIRouter(prefix="/api/calc", tags=["calc"])


class CalcRequest(BaseModel):
    price_now: Decimal = Field(..., gt=0)
    per_volume: Decimal = Field(..., gt=0)
    waste_lower: Decimal = Field(..., ge=0)
    waste_upper: Decimal = Field(..., ge=0)
    fee_amount_token: Decimal = Field(..., ge=0)


class CalcResponse(BaseModel):
    diff_lower: Decimal
    diff_upper: Decimal


@router.post("/price-range", response_model=CalcResponse)
async def price_range(req: CalcRequest) -> Dict[str, Decimal]:
    try:
        result = compute_diff_range(
            price_now=req.price_now,
            per_volume=req.per_volume,
            waste_lower=req.waste_lower,
            waste_upper=req.waste_upper,
            fee_amount_token=req.fee_amount_token,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
