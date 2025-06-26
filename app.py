from models.users import User

from database import db
from flask_login import LoginManager
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)
# view login


@app.route('/authenticate', methods=['POST'])
def authenticate():
  data = request.json
  email = data.get("email")
  password = data.get("password")

  if email and password:
    user = User.query.filter(User.email == email).first()

    if user and user.password == password:
      return jsonify({"message": "Authenticated"}), 200
      
  return jsonify({"message": "Invalid credentials"}), 400

@app.route("/hello-world", methods=['GET'])
def hello_world():
  return "Hello World"

if __name__ == '__main__':
  app.run(debug=True)