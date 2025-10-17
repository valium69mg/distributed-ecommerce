import httpx
import os
from dotenv import load_dotenv
from fastapi import Request, HTTPException, Depends
from dtos import UserRoles

load_dotenv()  

AUTH_ADDRESS = os.getenv('AUTH_ADDRESS')

async def verify_token(request : Request):
    token = request.headers.get('Authorization')
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    url = f"http://{AUTH_ADDRESS}/auth"  
    headers = {"Authorization": f"{token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        
    if response.status_code == 200:
        data = response.json()
        user = UserRoles(**data)
        return user
    elif response.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        raise HTTPException(status_code=500, detail="Auth service error")

