from fastapi import APIRouter, Depends, HTTPException, Request
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from api.database.session import get_db
from api.models.database_models import User
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
oauth = OAuth()

oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@router.get('/login/{provider}')
async def login(provider: str, request: Request):
    redirect_uri = request.url_for('auth_callback', provider=provider)
    if provider == 'google':
        return await oauth.google.authorize_redirect(request, redirect_uri)
    elif provider == 'github':
        return await oauth.github.authorize_redirect(request, redirect_uri)
    else:
        raise HTTPException(status_code=400, detail="Invalid provider")

@router.get('/callback/{provider}', name='auth_callback')
async def auth_callback(provider: str, request: Request, db: Session = Depends(get_db)):
    if provider == 'google':
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
    elif provider == 'github':
        token = await oauth.github.authorize_access_token(request)
        resp = await oauth.github.get('user', token=token)
        user_info = resp.json()
        # GitHub emails need a separate request if not public
        email_resp = await oauth.github.get('user/emails', token=token)
        emails = email_resp.json()
        user_info['email'] = next(e['email'] for e in emails if e['primary'])
    
    # Store or Update User in DB
    user = db.query(User).filter(User.email == user_info['email']).first()
    if not user:
        user = User(
            email=user_info['email'],
            full_name=user_info.get('name') or user_info.get('login'),
            oauth_provider=provider,
            oauth_id=str(user_info.get('sub') or user_info.get('id'))
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # In a real app, generate JWT here. 
    # For now, we'll return user info as a placeholder
    return {"status": "success", "user": {"email": user.email, "name": user.full_name}}
