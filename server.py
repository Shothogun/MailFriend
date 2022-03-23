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
    tickets_data = db.pullTicketData(amount)
    db.close()

    if tickets_data == None:
        tickets_data = {}
        
    return jsonify(tickets_data)