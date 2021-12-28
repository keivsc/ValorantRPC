from flask import Flask, jsonify
import os
import logging    
logging.getLogger('werkzeug').disabled = True

Valclient = None

app = Flask(__name__)

@app.route('/game')
def gamer():
    return Valclient.api()

@app.route('/game/<index>')
def game(index):
    api = Valclient.api()
    try:
        return api[index]
    except:
        return api

@app.route('/presence')
def presence():
    return Valclient.get_presence()

@app.route('/shutdown')
def shutdown():
    os._exit(1)

# @app.route('/search/<riotid>')
# def search(riotid):
#     pass
# WIP

def webrun(port, valclient):
    global Valclient
    Valclient = valclient
    app.run("localhost", port, debug=False)
    
    