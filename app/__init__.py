from flask import Flask

app = Flask(__name__)

from app.views import api
app.register_blueprint(api) 