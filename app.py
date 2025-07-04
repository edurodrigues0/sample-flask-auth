import bcrypt
from models.users import User

from database import db
from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:///root:admin123@127.0.0.1:3306/sample_flask_auth'

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

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
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

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(name=name, email=email, password=hashed_password, role='user')
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201
  return jsonify({"message": "Invalid data"}), 400

@app.route('/users', methods=['GET'])
def read_users():
  page = request.args.get('page', 1, type=int)
  per_page = 10
  offset = (page - 1) * per_page
  users = User.query.offset(offset).limit(10).all()
  total_users = User.query.count()

  users_list = []
  for user in users:
    users_list.append({
      "id": user.id,
      "name": user.name,
      "email": user.email,
      "created_at": user.created_at.isoformat(),
      "updated_at": user.updated_at.isoformat()
    })
  return jsonify({"users": users_list, "total_users": total_users}), 200

@app.route('/users/<string:id>', methods=['GET'])
@login_required
def read_user(id):
  user = User.query.filter(User.id == id).first()

  if user:
    return jsonify({
      "id": user.id,
      "name": user.name,
      "email": user.email,
      "created_at": user.created_at.isoformat(),
      "updated_at": user.updated_at.isoformat()
    }), 200
  return jsonify({"message": "User not found"}), 404

@app.route('/users/<string:id>', methods=['PUT'])
@login_required
def update_user(id):
  data = request.json
  name = data.get("name")
  password = data.get("password")
  role = data.get("role")

  if id != current_user.id and current_user.role == 'user':
    return jsonify({"message": "You not can update other users"}), 403


  if name or password:
    user = User.query.filter(User.id == id).first()

    if not user:
      return jsonify({"message": "User not found"}), 404

    if name:
      user.name = name
    if password:
      hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
      user.password = hashed_password
    if role and current_user.role == 'admin':
      if role not in ['user', 'admin']:
        return jsonify({"message": "Invalid role"}), 400
      user.role = role

    db.session.commit()
    return jsonify({"message": "User updated"}), 200
  return jsonify({"message": "Invalid data"}), 400

@app.route('/users/<string:id>', methods=['DELETE'])
@login_required
def delete_user(id):
  user = User.query.filter(User.id == id).first()

  if current_user.id == id:
    return jsonify({"message": "You not can delete your own account"}), 403
  if current_user.role != 'admin':
    return jsonify({"message": "You not can delete other users"}), 403

  if user:
    user_name = user.name
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user_name} deleted"}), 200
  return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
  app.run(debug=True)