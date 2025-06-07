from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
from database import get_db, Base, engine
from models import SIP
from schemas import SIPCreate, SIPSummary,TokenCreate
from auth import get_current_user_id, get_token
from crud import create_sip, get_sip_summary


import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(bind=engine)

app = FastAPI()

# APScheduler setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def simulate_monthly_sip():
    db = SessionLocal()
    try:
        from models import SIP
        from datetime import date
        sips = db.query(SIP).all()
        for sip in sips:
            # Simulate a new month by incrementing start_date by 1 month if needed
            # (For demo, just print or log)
            print(f"Simulating SIP for user {sip.user_id}, scheme {sip.scheme_name}, startdate {sip.start_date}")
        print("[APScheduler] Monthly SIP simulation executed.")
    finally:
        db.close()

scheduler = BackgroundScheduler()
# Run every 60 seconds for demo; change to weeks=4 for real monthly
scheduler.add_job(simulate_monthly_sip, 'interval', seconds=60)
scheduler.start()

@app.post("/sips/")
def add_sip(sip_data:SIPCreate, db: Session = Depends(get_db), user_id: str =Depends(get_current_user_id)):
    print("sip_data::::",sip_data)
    return create_sip(db, user_id, sip_data)

@app.get("/sips/summary", response_model=list[SIPSummary])
def sip_summary(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    return get_sip_summary(db, user_id)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


@app.post("/get_token")
def gettoken(token_data:TokenCreate):
    return get_token(token_data)