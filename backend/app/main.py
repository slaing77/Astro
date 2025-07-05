from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # ✅ create app FIRST!

# ✅ then add CORS middleware AFTER app exists:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import Depends
from app import models, database
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import SessionLocal
from fastapi import Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import shutil
import os
from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")  # Replace in production
DATABASE_URL = os.getenv("DATABASE_URL")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")
    return user

models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
async def root():
    return {"message": "Astro Bot API is up and running 🚀"}

@app.post("/login")
async def login(
    db: Session = Depends(get_db),
    payload: dict = Body(...)
):
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required.")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register")
async def register(
    email: str = Form(...),
    password: str = Form(...),
    username: str = Form(...),
    profile_picture: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    user_by_email = db.query(models.User).filter(models.User.email == email).first()
    user_by_username = db.query(models.User).filter(models.User.username == username).first()
    if user_by_email or user_by_username:
        raise HTTPException(status_code=400, detail="Email or username already taken.")

    hashed_password = pwd_context.hash(password)

    profile_picture_url = None
    if profile_picture:
        file_location = f"app/uploads/{profile_picture.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(profile_picture.file, buffer)
        profile_picture_url = file_location

    new_user = models.User(
        email=email,
        username=username,
        password_hash=hashed_password,
        profile_picture_url=profile_picture_url,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Registration successful!", "username": new_user.username}

@app.get("/profile")
async def read_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "username": current_user.username,
        "profile_picture_url": current_user.profile_picture_url,
        "created_at": current_user.created_at,
    }

