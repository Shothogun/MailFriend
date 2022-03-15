# app.py
from flask import Flask, request, jsonify
import dbClass

app = Flask(__name__)

@app.get("/calls")
def get_emails():
    db = dbClass.dbClass()
    amount = request.args.get('amount')
    
    if amount == None:
        amount = 10
    else:
        amount = int(amount)

    db.connect()
    calls = db.pullCalls(amount)
    db.close()

    if calls == None:
        calls = {}
        
    return jsonify(calls)