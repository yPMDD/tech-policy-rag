from fastapi import APIRouter, Depends, HTTPException, Request
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from api.database.session import get_db
from api.models.database_models import User
from api.auth.jwt_utils import get_current_user
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
    print(f"Auth callback called for provider: {provider}")
    try:
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
        
        print(f"User info received: {user_info}")
        
        from fastapi.responses import RedirectResponse
        from api.auth.jwt_utils import create_access_token
        
        # Store or Update User in DB
        user = db.query(User).filter(User.email == user_info['email']).first()
        
        # Priority 1: GitHub Login name
        # Priority 2: Google Name (slugified)
        # Priority 3: Email prefix
        raw_username = user_info.get('login') or user_info.get('name') or user_info.get('email').split('@')[0]
        # Remove spaces and lowercase it for a clean username
        username_val = raw_username.replace(' ', '').lower()
        
        print(f"DEBUG: Processing user {user_info['email']} with intended username: {username_val}")
        
        if not user:
            print(f"DEBUG: Creating NEW user record for {user_info['email']}")
            user = User(
                email=user_info['email'],
                full_name=user_info.get('name') or user_info.get('login'),
                username=username_val,
                oauth_provider=provider,
                oauth_id=str(user_info.get('sub') or user_info.get('id'))
            )
            db.add(user)
        else:
            print(f"DEBUG: Found EXISTING user record for {user_info['email']}")
            # Update fields to keep them fresh
            user.full_name = user_info.get('name') or user_info.get('login')
            user.username = username_val
            user.oauth_provider = provider
            print(f"DEBUG: Synced username to: {user.username}")
            
        try:
            db.commit()
            db.refresh(user)
            print(f"DEBUG: Database commit successful. User ID: {user.id}")
        except Exception as db_err:
            print(f"DEBUG: Database commit FAILED: {str(db_err)}")
            db.rollback()
            # If username conflict, try to make it unique
            if "unique constraint" in str(db_err).lower() and "username" in str(db_err).lower():
                user.username = f"{username_val}_{os.urandom(2).hex()}"
                db.commit()
                db.refresh(user)
                print(f"DEBUG: Recovered with unique username: {user.username}")
            else:
                raise db_err
        
        print(f"User found/created: {user.email}")
        
        # Generate JWT
        access_token = create_access_token(data={"sub": user.email})
        print("JWT generated.")
        
        # Redirect to frontend with token
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        target_url = f"{frontend_url}/?token={access_token}"
        print("**************************************************")
        print(f"CRITICAL: REDIRECTING TO -> {target_url}")
        print("**************************************************")
        return RedirectResponse(url=target_url)
    except Exception as e:
        print(f"Error in auth_callback: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")
@router.get('/me')
async def get_me(current_user: User = Depends(get_current_user)):
    print(f"DEBUG /me: user={current_user.email}, username={current_user.username}")
    return {
        "email": current_user.email,
        "full_name": current_user.full_name,
        "username": current_user.username,
        "oauth_provider": current_user.oauth_provider
    }
