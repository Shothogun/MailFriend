# app.py
from flask import Flask, request, jsonify
import dbClass
import os 

app = Flask(__name__)

@app.get("/calls")
def get_emails():
    db = dbClass.dbClass()
    amount = request.args.get('amount')
    
    if amount == None:
        amount = 100
    else:
        amount = int(amount)

    db.connect()
    tickets_data = db.pullTicketData(amount)
    db.close()

    if tickets_data == None:
        tickets_data = {}
        
    return jsonify(tickets_data)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)