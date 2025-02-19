from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import sqlite3
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

REGISTERED_FACES_DIR = "registered_faces"
if not os.path.exists(REGISTERED_FACES_DIR):
    os.makedirs(REGISTERED_FACES_DIR)

class FaceID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configure Upload Folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database Model
class ScannedID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    extracted_text = db.Column(db.Text, nullable=False)


@app.route('/')
def home():
    about = {
        "experience": "10+",
        "title": "Why Choose Us?",
        "description": "We provide the best hospitality services with integrity and value. Stay in a home away from home and feel the your desired life with best accommodations and less costs."
    }
    collections = [
        {"image": "image/rooms.jpeg", "title": "Luxury Suites"},
        {"image": "image/luxury.jpg", "title": "Beach Resorts"},
        {"image": "image/room.jpg", "title": "Villas"},
        {"image": "image/hotel3.jpg", "title": "Family time"},
    ]
    services = [
    {
        "icon": "utensils",
        "title": "Food Service/ Food Runner",
        "description": " We ensure that hot, fresh, and delicious meals are delivered to your doorstep.Enjoy a diverse menu crafted by top chefs, featuring the finest ingredients.Savor every bite with our quick and reliable delivery service, bringing restaurant-quality meals to you."
    },
    {
        "icon": "coffee",
        "title": "Refreshment",
        "description": "From freshly brewed coffee to chilled soft drinks, we provide a range of refreshments. Quench your thirst with our carefully curated selection of beverages for every mood.Experience the perfect pairing of drinks with your favorite meals, delivered straight to you."
    },
    {
        "icon": "broom",
        "title": "HouseKeeping",
        "description": "Our housekeeping services keep your stay clean and comfortable. Our housekeeping services keep your stay clean and comfortable. Our housekeeping services keep your stay clean and comfortable.From freshly brewedhilled soft drinks, we provide a range of refreshments."
    },
    {
        "icon": "lock",
        "title": "Room Security",
        "description": "Smart keycard access, 24/7 security surveillance, and emergency support. Enjoy a safe and secure stay with advanced technology and round-the-clock protection.Your safety and peace of mind are our top priorities, ensuring a worry-free experience. Enjoy a  crafted by top chefs"
    }
]
    testimonials = [
    {
        "title": "We Loved It",
        "content": "Enjoy a delightful dining experience with our fast and efficient room service.",
        "customer": "Customer Name, Country",
        "rating": 4
    },
    {
        "title": "Comfortable Living",
        "content": "Unwind with a selection of beverages and snacks available around the clock.",
        "customer": "Customer Name, Country",
        "rating": 4
    },
    {
        "title": "Nice Place",
        "content": "Your safety is our top priority.",
        "customer": "Customer Name, Country",
        "rating": 4
    }
]
    return render_template('index.html', about=about, collections=collections, testimonials=testimonials, services=services)

# Route for Home Page
@app.route('/form')
def form():
    return render_template('form.html')

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already exists. Please login.", "error")
        return redirect(url_for('home'))

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash("Signup successful! Please login.", "success")
    return redirect(url_for('hotels'))

@app.route('/face' , methods=['GET'])
def face():
    return render_template('face.html')

@app.route('/scan-id', methods=['POST'])
def scan_id():
    if 'idImage' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['idImage']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Placeholder for OCR processing
    extracted_text = "OCR processing removed"

    # Store in Database
    new_scan = ScannedID(filename=filename, extracted_text=extracted_text)
    db.session.add(new_scan)
    db.session.commit()

    return jsonify({"extractedText": extracted_text})
    return redirect(url_for('hotels'))

# Login Route
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        flash(f"Welcome {user.name}! Login successful.", "success")
        return redirect(url_for('hotels'))
    
    flash("Invalid email or password.", "error")
    return redirect(url_for('hotels'))

# Protected Dashboard Route
@app.route('/dashboard')
@login_required
def dashboard():
    return f"Hello, {current_user.name}! Welcome to your dashboard."

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))

@app.route('/hotels')
def hotels():
    destinations = [
    {"name": "New Delhi", "image": "image/newdelhi.jpg"},
    {"name": "Bangalore", "image": "image/bangalore.jpg"},
    {"name": "Mumbai", "image": "image/chennnai.jpg"},
    {"name": "Chennai", "image": "image/mumbai.jpg"},
    {"name": "Hyderabad", "image": "image/hyderabad.jpg"},
    {"name": "Chandigarh", "image": "image/chandigarh.jpg"},
]
    
    hostels = [
        {
            "name": "Rivoli Cinema Hostel",
            "rating": 9.4,
            "rating_text": "Superb",
            "reviews": 3656,
            "location": "Porto, Portugal",
            "discount": 15,
            "image": "https://image.unsplash.com/photo-1520277739336-7bf67edfa768"
        },
        {
            "name": "ELTARI Pine House",
            "rating": 9.4,
            "rating_text": "Superb",
            "reviews": 51,
            "location": "Malang, Indonesia",
            "discount": 25,
            "image": "https://image.unsplash.com/photo-1566073771259-6a8506099945"
        },
        {
            "name": "Sir Toby's Midtown",
            "rating": 9.2,
            "rating_text": "Superb",
            "reviews": 46,
            "location": "Prague, Czech Republic",
            "discount": 20,
            "image": "https://image.unsplash.com/photo-1555854877-bab0e564b8d5"
        },
        {
            "name": "Sloth Backpackers Hostel",
            "rating": 8.5,
            "rating_text": "Fabulous",
            "reviews": 744,
            "location": "Monteverde, Costa Rica",
            "discount": 50,
            "image": "https://image.unsplash.com/photo-1596701062351-8c2c14d1fdd0"
        },
        {
            "name": "Hoztel Jaipur",
            "rating": 9.3,
            "rating_text": "Superb",
            "reviews": 909,
            "location": "Jaipur, India",
            "discount": 25,
            "image": "https://image.unsplash.com/photo-1542314831-068cd1dbfeeb"
        },
        {
            "name": "Backpackers Paradise",
            "rating": 9.1,
            "rating_text": "Superb",
            "reviews": 427,
            "location": "Bangkok, Thailand",
            "discount": 30,
            "image": "https://image.unsplash.com/photo-1590073242678-70ee3fc28e8e"
        },
        {
            "name": "Sunset Beach Hostel",
            "rating": 8.9,
            "rating_text": "Fabulous",
            "reviews": 283,
            "location": "Bali, Indonesia",
            "discount": 35,
            "image": "https://image.unsplash.com/photo-1520250497591-112f2f40a3f4"
        },
        {
            "name": "Mountain View Lodge",
            "rating": 9.5,
            "rating_text": "Exceptional",
            "reviews": 156,
            "location": "Queenstown, New Zealand",
            "discount": 20,
            "image": "https://image.unsplash.com/photo-1571003123894-1f0594d2b5d9"
        }
    ]
    return render_template('hotels.html', destinations=destinations)



@app.route("/room")
def room():
    hotels = [
    {
        "name": "Hotel O Lal Sai Residency",
        "location": "Andheri West, Mumbai",
        "distance": "9.9 km",
        "rating": 4.1,
        "reviews": 99,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 7469,
        "discounted_price": 1928,
        "taxes_fees": 399,
        "image": "static/lalsai.jpg",
        "badge": "Mid range"
    },
    {
        "name": "Hotel Golden Galaxy",
        "location": "Santacruz East, Mumbai",
        "distance": "6.0 km",
        "rating": 4.0,
        "reviews": 97,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 7299,
        "discounted_price": 1900,
        "taxes_fees": 399,
        "image": "static/lalsai.jpg",
        "badge": "Mid range"
    },
    {
        "name": "Hotel Ajanta",
        "location": "Juhu Beach, Mumbai",
        "distance": "3.5 km",
        "rating": 4.4,
        "reviews": 99,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 8689,
        "discounted_price": 2563,
        "taxes_fees": 399,
        "image": "static/lalsai.jpg",
        "badge": "Mid range"
    },
    {
        "name": "Hotel Marine Plaza",
        "location": "29 Marine Drive, Churchgate, Mumbai",
        "distance": "9.5 km",
        "rating": 4.9,
        "reviews": 99,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 11999,
        "discounted_price": 3999,
        "taxes_fees": 399,
        "image": "static/apartment.jpeg",
        "badge": "Mid range"
    },
    {
        "name": "Hotel Sahara Star",
        "location": "Vile Parle East, Mumbai",
        "distance": "6.5 km",
        "rating": 4.5,
        "reviews": 99,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 9999,
        "discounted_price": 2999,
        "taxes_fees": 399,
        "image": "static/lalsai.jpg",
        "badge": "Mid range"
    },
    {
        "name": "Hotel Kemps Corner",
        "location": "Kemps Corner, Mumbai",
        "distance": "9.9 km",
        "rating": 4.1,
        "reviews": 99,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 7406,
        "discounted_price": 1905,
        "taxes_fees": 399,
        "image": "static/lalsai.jpg",
        "badge": "Mid range"
    },
    {
        "name": "Taj Lands End",
        "location": "Bamdra West, Mumbai",
        "distance": "8.9 km",
        "rating": 4.7,
        "reviews": 99,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 10969,
        "discounted_price": 2999,
        "taxes_fees": 399,
        "image": "static/golden.jpeg",
        "badge": "Mid range"
    },
]

    return render_template("room.html", hotels=hotels)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    message = request.form.get("message")

    print(f"Received message from {name} ({email}, {phone}): {message}")

    return "Form submitted successfully!"

@app.route('/booking')
def booking():
    return render_template('booking.html')  # Ensure you have an 'index.html' file in a 'templates' folder

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    phone = data.get("phone")
    if phone and len(phone) >= 10:
        return jsonify({"message": "OTP sent successfully!", "success": True})
    return jsonify({"message": "Invalid phone number", "success": False})

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.json
    otp = data.get("otp")
    if otp == "1234":  # Example OTP verification
        return jsonify({"message": "OTP verified successfully!", "success": True})
    return jsonify({"message": "Invalid OTP", "success": False})

user_data = {
    "name": "Nikhil Palyal",
    "email": "nikhilpalyal6@gmail.com",
    "phone": "8264131474"
}

booking_data = {
    "hotel_name": "Super Townhouse Khar The Unicontinental",
    "address": "9A Rajkutir, 3rd Road, next to Doolally Taproom, next to Khar railway station, Khar West",
    "rating": "4.7 ★ (276 Ratings) • Excellent",
    "stay_details": "Sun, 16 Feb – Mon, 17 Feb | 1 Room, 1 Guest",
    "price_breakdown": {
        "room_price": 10375,
        "instant_discount": -3112,
        "coupon_discount": -3849,
        "wizard_discount": -171,
        "wizard_membership": 171,
        "oyo_money": -682,
        "payable_amount": 2732
    }
}

@app.route('/activity')
def activity():
    return render_template('activity.html', user=user_data, booking=booking_data)

@app.route('/update_user', methods=['POST'])
def update_user():
    global user_data
    user_data["name"] = request.form.get("name")
    user_data["email"] = request.form.get("email")
    user_data["phone"] = request.form.get("phone")
    return jsonify({"message": "User details updated successfully!"})


# Payment model for database
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    expiry_date = db.Column(db.String(10), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Payment {self.email}>'

# Create the database and tables
def init_db():
    with app.app_context():
        # Drop existing tables and create new ones
        db.drop_all()
        db.create_all()

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            # If not JSON, try form data
            data = request.form

        # Extract payment details
        email = data.get('email')
        card_number = data.get('card_number')
        expiry_date = data.get('expiry_date')
        cvv = data.get('cvv')
        payment_method = data.get('payment_method')

        # Validate required fields
        if not all([email, card_number, expiry_date, cvv, payment_method]):
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400

        # Basic validation
        if not 13 <= len(str(card_number)) <= 16:
            return jsonify({
                'success': False,
                'message': 'Invalid card number'
            }), 400

        if len(str(cvv)) not in [3, 4]:
            return jsonify({
                'success': False,
                'message': 'Invalid CVV'
            }), 400

        # Create new payment record
        new_payment = Payment(
            email=email,
            card_number=card_number,
            expiry_date=expiry_date,
            cvv=cvv,
            payment_method=payment_method
        )

        # Save to database
        db.session.add(new_payment)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Payment processed successfully',
            'payment_id': new_payment.id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error processing payment: {str(e)}'
        }), 500

@app.route('/payment', methods=['GET'])
def get_payments():
    try:
        payments = Payment.query.order_by(Payment.created_at.desc()).all()
        return jsonify({
            'success': True,
            'payments': [{
                'id': p.id,
                'email': p.email,
                'payment_method': p.payment_method,
                'created_at': p.created_at.strftime('%Y-%m-%d %H:%M:%S')
            } for p in payments]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving payments: {str(e)}'
        }), 500

def init_db():
    with sqlite3.connect('transactions.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     upi_id TEXT NOT NULL,
                     amount REAL NOT NULL,
                     description TEXT,
                     timestamp TEXT NOT NULL)''')
        conn.commit()

with app.app_context():
    init_db()

@app.route('/upi')
def upi():
    return render_template('upi.html')

@app.route('/get_transactions')
def get_transactions():
    with sqlite3.connect('transactions.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM transactions ORDER BY timestamp DESC')
        transactions = c.fetchall()

    formatted_transactions = [
        {
            'id': t[0],
            'upi_id': t[1],
            'amount': t[2],
            'description': t[3],
            'timestamp': t[4]
        } for t in transactions
    ]
    return jsonify(formatted_transactions)

@app.route('/make_payment', methods=['POST'])
def make_payment():
    try:
        data = request.get_json()
        upi_id = data.get('upi_id')
        amount = float(data.get('amount'))
        description = data.get('description', '')

        if not upi_id or not amount:
            return jsonify({'error': 'Missing required fields'}), 400

        if '@' not in upi_id:
            return jsonify({'error': 'Invalid UPI ID format'}), 400

        if amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400

        with sqlite3.connect('transactions.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO transactions (upi_id, amount, description, timestamp) VALUES (?, ?, ?, ?)',
                      (upi_id, amount, description, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()

        return jsonify({'message': 'Payment successful and data stored in database'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/registerface")
def registerface():
    return render_template("registerface.html")

@app.route("/register-face", methods=["POST"])
def register_face():
    try:
        data = request.json  # Get JSON data from request
        if not data or "name" not in data or "image" not in data:
            return jsonify({"success": False, "message": "Missing name or image data!"}), 400

        name = data["name"]
        image_data = data["image"].split(",")[1]  # Remove base64 header
        image_bytes = base64.b64decode(image_data)

        # Save the image with a unique filename
        image_filename = f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        image_path = os.path.join(REGISTERED_FACES_DIR, image_filename)

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        # Save details in the database
        new_face = FaceID(name=name, image_path=image_path)
        db.session.add(new_face)
        db.session.commit()
        
        return jsonify({"success": True, "message": "Face registered successfully!", "image_path": image_path})
    except Exception as e:
        print("Error:", str(e))  # Print error in terminal
        return jsonify({"success": False, "message": "An error occurred while registering face."}), 500



# Run Server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)