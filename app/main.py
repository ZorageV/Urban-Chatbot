import time
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi import status
import psycopg2
from pydantic import BaseModel
from .ocr import ocr
app = FastAPI()

while True:
    try:
        conn = psycopg2.connect("user=postgres.lapnkmiiauzfherbglcm password=brainanalyst@123 host=aws-0-ap-south-1.pooler.supabase.com port=5432 dbname=postgres")
        cursor = conn.cursor()
        print("Connected to DB")
        break
    except Exception as error:
        print("Unable to connect to DB")

class Property(BaseModel):
    name: str
    street: str
    district: str
    state: str
    customer_id: int
class User_login(BaseModel):
    username : str
    password : str

@app.get("/")
def root():
    return "Hello This is urban chatbot"

@app.post("/login",status_code=status.HTTP_200_OK)
def login(user : User_login):
    cursor.execute("SELECT id FROM customer WHERE username = %s AND password = %s",(user.username,user.password))
    user_id = cursor.fetchone()
    if not user_id:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Wrong username and password"
        )
    return user_id

@app.get("/properties/{id}", status_code=status.HTTP_200_OK)
def get_properties(id: int):
    id = str(id)
    cursor.execute("SELECT * FROM properties WHERE customer_id = %s",(id))
    properties = cursor.fetchall()
    return properties

@app.post("/properties/")
def add_property(property: Property):
    cursor.execute("INSERT INTO properties (property_name,street,district,state,customer_id) VALUES (%s,%s,%s,%s,%s) RETURNING property_id",
                   (property.name, property.street, property.district, property.state, property.customer_id))
    property_id = cursor.fetchone()
    conn.commit()
    return {"property_id": property_id}

@app.put("/properties/{id}")
def update_property(id: int, property: Property):
    id = str(int)
    cursor.execute("UPDATE properties SET name = %s, street = %s, district = %s, state = %s WHERE id = %s returning property_id",
                   (property.name, property.street, property.district, property.state, id))
    conn.commit()
    return {"message": "Property updated successfully"}

@app.post("/application")
def application(img_path : str):
    text = ocr(img_path)
    return text