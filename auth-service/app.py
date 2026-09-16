import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app) # Add this line to allow browser requests

# Database configuration (These will be passed dynamically by Kubernetes later)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost:5432/librarydb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET', 'super-secret-key')

db = SQLAlchemy(app)
jwt = JWTManager(app)

# --- Database Model (Replacing the old JSON structure) ---
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
# --- REST Endpoints (Replacing the old command-line inputs) ---
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Missing username or password"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "User already exists"}), 409
        
    # Hash the password for security
    hashed_pw = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password_hash=hashed_pw)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201
    
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
        
    if not user or not check_password_hash(user.password_hash, data.get('password')):
        return jsonify({"msg": "Bad username or password"}), 401
        
    # Issue the stateless JWT string
    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200
    
if __name__ == '__main__':
    # Initialize DB tables for testing purposes
    with app.app_context():
        db.create_all()
    # Bind to 0.0.0.0 so Docker and Kubernetes can route external traffic to it
    app.run(host='0.0.0.0', port=5000)