import hashlib
import base64
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from models import *
from auth import *

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a database engine. 
engine = create_engine('sqlite:///rocket.db', connect_args={'check_same_thread': False}, poolclass=StaticPool)
Base.metadata.bind = engine
 
# Create a new database session.
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.get("/api/alerts")
def read_alerts():
    # Get all alerts.
    rows = session.query(Alert).all()
    
    # Prepare return data.
    data = []
    for row in rows:
        data.append(row.to_json())
        
    # Return data.
    return data

@app.get("/api/contacts")
def read_contact():
    # Get all contacts.
    rows = session.query(Contact).all()
    
    # Prepare return data.
    data = []
    for row in rows:
        data.append(row.to_json())
        
    # Return data.
    return data

@app.get("/api/contacts/states/count")
def read_contact_status():
    # Generate a list of contact states with their count.
    results = []
    rows = session.query(ContactState).all()
    for row in rows:
        contacts = session.query(Contact).filter(Contact.state_id == row.id).all()
        results.append({
            "state_id": row.id,
            "state": row.state.title(),
            "count": len(contacts)
        })

    return results
    
@app.post("/api/users/register")
def register_user(new_user: UserRegistration, status_code=201):
    # Look up the user in the database.
    agent = session.query(Agent).filter(Agent.email == new_user.email).first()

    if agent is not None:
        # An account for this email has already been registered.
        raise HTTPException(status_code=409, detail="An account for this email already exists.")
    else:
        # Create new agent.
        temp = Agent()
        temp.email = new_user.email
        temp.firstname = new_user.firstname
        temp.lastname = new_user.lastname

        # Set password
        salt = create_salt(12)
        temp.passwordsalt = salt
        temp.passwordhash = get_password_hash(new_user.password + salt)
        
        # Save to database.
        session.add(temp)
        session.commit()
        token = create_token(agent)

        # Return the user and token.
        return {"result": "True",
                "email": temp.email,
                "firstname": temp.firstname,
                "lastname": temp.lastname,
                "token": token
        }

@app.post("/api/users/login")
def validate_user(user: UserLogin, status_code=200):
    # Look up the user in the database.
    agent = session.query(Agent).filter(Agent.email == user.email).first()
    if agent is not None:
        # Create new agent.
        salted_password = user.password + agent.passwordsalt
        if verify_password(salted_password, agent.passwordhash):
            token = create_token(agent.email)
            payload = {"result": "True",
                    "email": agent.email,
                    "firstname": agent.firstname,
                    "lastname": agent.lastname,
                    "token": token
            }
            return JSONResponse(content=payload)

    # If we get here, then a username/password pair wasn't matched.
    raise HTTPException(status_code=401, detail="Invalid username or password.")

@app.post("/api/token/validate")
def validate_user_token(token: UserToken, status_code=200):
    if verify_token(token.token):
        return # return default status code
    else:
        raise HTTPException(status_code=401, detail="Invalid token.")
        