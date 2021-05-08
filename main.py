from flask import Flask
from flask_restful import Api
from resource.api import  label

app = Flask('app')
api = Api(app)

api.add_resource(label, '/label')


@app.route('/')
def hello_world():
	return 'Hello, World!'


app.run(host='0.0.0.0', port=8080)
