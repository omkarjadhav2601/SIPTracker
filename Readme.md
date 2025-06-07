### 📦 Tech Stack
- FastAPI
- Supabase Auth (JWT)
- PostgreSQL
- SQLAlchemy ORM

### 🚀 Getting Started
1. Clone the repo
2. Create `.env` with `DATABASE_URL` and `SUPABASE_JWT_SECRET`
3. Create and activate a virtual environment:
   - `python -m venv venv`
   - `./venv/Scripts/activate`
4. Install dependencies:
   - `pip install -r requirements.txt`
5. Start the app:
   - `python main.py`
6. Visit [http://localhost:8000/docs](http://localhost:8000/docs)


### 📘 API

## 🔐 Authentication
Get a token using the POST API gettoken by passing your email and password.
POST `/get_token`
```json
{
  "email_id": "emailid",
  "password": "password"
}
```
Pass the generated token to the Authorize Bearer in headers or in Swagger before hitting any other endpoint like get summary and create SIP. Once passed, you can test the rest with the below format.

#### Create SIP Plan
POST `/sips/`
```json
{
  "scheme_name": "Parag Parikh Flexi Cap",
  "monthly_amount": 5000,
  "start_date": "2024-01-01"
}
```

#### Get SIP Summary
GET `/sips/summary`
```json
[
  {
    "scheme_name": "Parag Parikh Flexi Cap",
    "total_invested": 25000,
    "months_invested": 5
  }
]
```