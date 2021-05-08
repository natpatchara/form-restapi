from flask import Flask
from flask_restful import Api
from resource.api import base64_api, path_api, binary_api, label

app = Flask('app')
api = Api(app)

api.add_resource(binary_api, '/binary_api')
api.add_resource(path_api, '/path_api')
api.add_resource(base64_api, '/base64_api')
api.add_resource(label, '/label')


@app.route('/')
def hello_world():
	return 'Hello, World!'


app.run(host='0.0.0.0', port=8080)
