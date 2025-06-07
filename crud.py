from sqlalchemy.orm import Session
from models import SIP
from schemas import SIPCreate
from datetime import date
from collections import defaultdict

def create_sip(db: Session, user_id: str, sip_data: SIPCreate):
    sip = SIP(user_id=user_id, **sip_data.model_dump())
    db.add(sip)
    db.commit()
    db.refresh(sip)
    return sip

def get_sip_summary(db: Session, user_id: str):
    sips = db.query(SIP).filter(SIP.user_id == user_id).all()
    summary = defaultdict(lambda: {"total_invested": 0, "months_invested": 0, "units_purchased": 0.0})
    MOCK_NAV = 50  # Mock NAV value

    for sip in sips:
        delta_months = (date.today().year - sip.start_date.year) * 12 + (date.today().month - sip.start_date.month)
        months = max(delta_months, 1)
        invested = sip.monthly_amount * months
        units = invested / MOCK_NAV
        summary[sip.scheme_name]["total_invested"] += invested
        summary[sip.scheme_name]["months_invested"] += months
        summary[sip.scheme_name]["units_purchased"] += units
        print("summary ::::: ", summary)
    return [
        {
            "scheme_name": name,
            "total_invested": data["total_invested"],
            "months_invested": data["months_invested"],
            "units_purchased": round(data["units_purchased"], 2)
        } for name, data in summary.items()
    ]

