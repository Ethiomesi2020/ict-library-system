import os
import csv
import requests
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
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

    # Register the due date and Check the return status
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))
    is_returned = db.Column(db.Boolean, default=False)

# --- REST Endpoints ---

@app.route('/books', methods=['GET'])
def get_books():
    """Fetches and parses book data from an external CSV URL."""
    # In a real scenario, this URL might be hardcoded or passed via environment variable
    csv_url = request.args.get('url', 'https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv')

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

    # Some Business Logics:
    # Rule-01, get_jwt_identity() securely extracts the user_id from the token
    current_user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('Title')

    if not title:
        return jsonify({"msg": "Missing book_title in request body"}), 400

    # Rule-02, Check if a user already has 10 unreturned books
    active_count = BorrowedBook.query.filter_by(user_id=current_user_id, is_returned=False).count()

    if active_count >= 10:
        return jsonify({"msg": "Limit reached. You cannot borrow more than 10 books at a time."}), 403

    # Rule-03, Check if they already borrowed THIS specific book and haven't returned it
    already_borrowed = BorrowedBook.query.filter_by(user_id=current_user_id, book_title=title, is_returned=False).first()

    if already_borrowed:
        return jsonify({"msg": f"You already have an active borrowed copy of '{title}'."}), 409

    # Rule-04, Save the borrow record to PostgreSQL
    new_borrow = BorrowedBook(
        user_id = current_user_id, 
        book_title = data['Title'],
        author = data.get('author', 'Unknown')
    )
    db.session.add(new_borrow)
    db.session.commit()

    return jsonify({"msg": f"Book '{data['Title']}' borrowed successfully by user {current_user_id}"}), 201

@app.route('/return', methods=['POST'])
@jwt_required()
def return_book():
    """Removes a borrowed book record. Requires a valid JWT."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('Title')

    if not title:
        return jsonify({"msg": "Missing book_title in request body"}), 400

    # Rule-05, Find the specific record for this user and this book
    record = BorrowedBook.query.filter_by(user_id=current_user_id, book_title=title, is_returned=False).first()

    if not record:
        return jsonify({"msg": "Record not found or book not borrowed by you"}), 404

    # Mark as returned
    record.is_returned = True
    return_date = datetime.utcnow()
    fee = 0
    days_late = 0

    # Rule-06, Calculate $1 per day late fee if returned after 30 days
    if return_date > record.due_date:
        days_late = (return_date - record.due_date).days
        if days_late > 0:
            fee = days_late * 1  # $1 per day

    # Commit the record
    db.session.commit()

    msg = f"Book '{title}' returned successfully."

    if fee > 0:
        msg += f" WARNING: You were {days_late} days late. Late fee owed: ${fee}."

    return jsonify({"msg": msg, "fee_charged": fee}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Run on port 5001 so it doesn't conflict with the Auth Service on port 5000
    app.run(host='0.0.0.0', port=5001)
