# app.py
from flask import Flask, request, jsonify
import dbClass

app = Flask(__name__)

@app.get("/calls")
def get_emails():
    db = dbClass.dbClass()
    
    db.connect()
    calls = db.pullCalls(10)
    db.close()

    if calls == None:
        calls = {}
        
    return jsonify(calls)