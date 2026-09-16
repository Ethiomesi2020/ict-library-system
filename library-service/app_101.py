import os
import csv
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

appp = Flask(__name__)
CORS(app) # Add this line to allow browser requests

# Connect to the same PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost:5432/librarydb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CRITICAL: Must be the exact same secret key used in the Auth Service
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET', 'super-secret-key')

db = SQLAlchemy(app)
jwt = JWTManager(app)

# --- Database Model (Replacing the user JSON storage for borrowed books) ---
class BorrowedBook(db.Model):
    __tablename__ = 'borrowed_books'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    
# --- REST Endpoints ---

@app.route('/books', methods=['GET'])
def get_books():
    """Fetches and parses book data from an external CSV URL."""
    # In a real scenario, this URL might be hardcoded or passed via environment variable
    csv_url = request.args.get('url', 'https://example-domain.com/books.csv')
    
    try:
        response = requests.get(csv_url)
        response.raise_for_status()
        
        # Parse CSV text data into a list of dictionaries
        lines = response.text.splitlines()
        reader = csv.DictReader(lines)
        books = [row for row in reader]
        
        return jsonify({"available_books": books}), 200
    except Exception as e:
        return jsonify({"msg": f"Failed to fetch books: {str(e)}"}), 500
        
@app.route('/borrow', methods=['POST'])
@jwt_required()
def borrow_book():
    """Records a borrowed book. Requires a valid JWT."""
    # get_jwt_identity() securely extracts the user_id from the token
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('book_title'):
        return jsonify({"msg": "Missing book_title in request body"}), 400
        
    # Save the borrow record to PostgreSQL instead of a local JSON file
    new_borrow = BorrowedBook(
        user_id=current_user_id, 
        book_title=data['book_title'],
        author=data.get('author', 'Unknown')
    )
    db.session.add(new_borrow)
    db.session.commit()
    
    return jsonify({"msg": f"Book '{data['book_title']}' borrowed successfully by user {current_user_id}"}), 201
    
@app.route('/return', methods=['POST'])
@jwt_required()
def return_book():
    """Removes a borrowed book record. Requires a valid JWT."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('book_title'):
        return jsonify({"msg": "Missing book_title"}), 400
        
    # Find the specific record for this user and this book
    record = BorrowedBook.query.filter_by(user_id=current_user_id, book_title=data['book_title']).first()
    
    if not record:
        return jsonify({"msg": "Record not found or book not borrowed by you"}), 404
        
    # Delete the record to simulate returning the book
    db.session.delete(record)
    db.session.commit()
        
    return jsonify({"msg": f"Book '{data['book_title']}' returned successfully"}), 200    
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Run on port 5001 so it doesn't conflict with the Auth Service on port 5000
    app.run(host='0.0.0.0', port=5001)