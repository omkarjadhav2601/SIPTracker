from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class SIP(Base):
    __tablename__ = "sips"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    scheme_name = Column(String)
    monthly_amount = Column(Integer)
    start_date = Column(Date)

