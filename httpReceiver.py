import os
from flask import Flask, request, Response, jsonify
from slackclient import SlackClient
import remote
import sensors


app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')

@app.route('/slack', methods=['POST'])
def inbound():
	text = ''
	#if request.form.get('token') == SLACK_WEBHOOK_SECRET:
	if True:
		channel = request.form.get('channel_name')
		username = request.form.get('user_name')
		text = request.form.get('text')
		inbound_message = username + " in " + channel + " says: " + text
		print(inbound_message)
		remote.parseRemoteCommand(text)
	return Response("Got it: " + text), 200

@app.route('/', methods=['GET'])
def test():
	return Response('It works!')

@app.route('/storage', methods=['GET'])
def returnStorage():
	return jsonify(sensors.storage)

@app.route('/shutdown', methods=['GET'])
def shutdown():
	remote.parseOffCommand()
	return Response('Shutdown')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def runFlaskServer():
	app.run(debug=True, use_reloader = False, host='0.0.0.0')

#if __name__ == "__main__":
#app.run(debug=True, use_reloader = False, host='0.0.0.0')
