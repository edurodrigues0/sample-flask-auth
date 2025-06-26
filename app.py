from flask import Flask
from models.users import User
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route("/hello-world", methods=['GET'])
def hello_world():
  return "Hello World"

if __name__ == '__main__':
  app.run(debug=True)