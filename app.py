from models.users import User

from database import db
from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'authenticate'

@login_manager.user_loader
def load_user(user_id):
  return User.query.filter(User.id == user_id).first()

@app.route('/authenticate', methods=['POST'])
def authenticate():
  data = request.json
  email = data.get("email")
  password = data.get("password")

  if email and password:
    user = User.query.filter(User.email == email).first()

    if user and user.password == password:
      login_user(user)
      return jsonify({"message": "Authenticated"}), 200
      
  return jsonify({"message": "Invalid credentials"}), 400

@app.route("/logout", methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logged out"}), 200
    
@app.route("/users", methods=['POST'])
def create_user():
  data = request.json
  name = data.get("name")
  email = data.get("email")
  password = data.get("password")

  if name and email and password:
    user_exists = User.query.filter(User.email == email).first()

    if user_exists:
      return jsonify({"message": "User already exists"}), 400

    user = User(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201
  return jsonify({"message": "Invalid data"}), 400

@app.route("/hello-world", methods=['GET'])
def hello_world():
  return "Hello World"

if __name__ == '__main__':
  app.run(debug=True, port=3333)