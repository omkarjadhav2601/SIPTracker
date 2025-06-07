from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt 
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from schemas import TokenCreate

load_dotenv()

security = HTTPBearer()
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
print("Loaded JWT Secret:", SUPABASE_JWT_SECRET)

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    print("[DEBUG] JWT Secret Loaded:", SUPABASE_JWT_SECRET)
    print("[DEBUG] Token Received:", token)
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"],audience="authenticated")
        print("[DEBUG] Decoded Payload:", payload)
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        print("[DEBUG] Token expired")
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception as e:
        print("[DEBUG] JWT Decode Error:", e)
        raise HTTPException(status_code=401, detail="Invalid JWT Token")


def get_token(token_data:TokenCreate):
    try:
        url = os.getenv("PROJECT_URL")
        key = os.getenv("API_KEY")

        supabase: Client = create_client(url, key)
        print("token_data ::", token_data)
        print("token_data ::", token_data.email_id)
        # Sign in with email and password
        response = supabase.auth.sign_in_with_password({
            "email": token_data.email_id,
            "password": token_data.password
        })
        print("response :: ", response)
        # Get the JWT access token
        jwt_token = response.session.access_token
        print("JWT Token:", jwt_token)
        return jwt_token
    except Exception as error:
        return error.message