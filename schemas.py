from pydantic import BaseModel
from datetime import date

class SIPCreate(BaseModel):
    scheme_name: str
    monthly_amount: int
    start_date: date

class SIPSummary(BaseModel):
    scheme_name: str
    total_invested: int
    months_invested: int
    units_purchased: int

class TokenCreate(BaseModel):
    email_id: str
    password: str