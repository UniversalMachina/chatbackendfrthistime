from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, Blueprint, request, current_app as app
from models.User import User
from models import db
user_bp = Blueprint("user_bp", __name__, url_prefix="")

@user_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        print("Login successful")
        return jsonify({"message": "Login successful"}), 200
    else:
        print("Invalid credentials")
        return jsonify({"message": "Invalid credentials"}), 401


@user_bp.route('/register', methods=['POST'])
def register():
    try:
        print("Register endpoint hit")
        data = request.json

        if not data:
            print("No data received in request")
            return jsonify({"message": "No data received"}), 400

        print("Request Data:", data)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            print("Username or password not provided")
            return jsonify({"message": "Username and password are required"}), 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        print(f"User '{username}' registered successfully")
        return jsonify({"message": "User registered successfully"}), 200

    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {e}")
        return jsonify({"message": "Database error occurred"}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({"message": "An error occurred during registration"}), 500


@user_bp.route('/update-profile', methods=['POST'])
def update_profile():
    try:
        data = request.json
        print("Received profile data:", data)

        # Assuming the username is provided for identifying the user
        # In a real app, you would typically use the logged-in user's ID or username
        username = data.get('username')
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        user.name = data.get('name', user.name)  # Update name, if provided
        user.email = data.get('email', user.email)  # Update email, if provided
        user.age = data.get('age', user.age)  # Update age, if provided

        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200

    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {e}")
        return jsonify({"message": "Database error occurred"}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({"message": "An error occurred during profile update"}), 500


@user_bp.route('/customization', methods=['POST'])
def update_user_color():
    try:
        data = request.json
        username = data.get('username')

        # Check if the username is provided
        if not username:
            return jsonify({"message": "Username is required"}), 400

        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        # Update the color attribute
        user.color = data.get('color')
        print(user.color)
        if not user.color:
            return jsonify({"message": "Color is required"}), 400

        db.session.commit()
        return jsonify({"message": "Color updated successfully"}), 200

    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {e}")
        return jsonify({"message": "Database error occurred"}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({"message": "An error occurred during color update"}), 500

@user_bp.route('/get-color/<username>', methods=['GET'])
def get_user_color(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"color": user.color}), 200


@user_bp.route('/set-language', methods=['POST'])
def set_language():
    try:
        data = request.json
        username = data.get('username')
        language = data.get('language')

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        user.preferred_language = language  # Assuming `preferred_language` field exists
        db.session.commit()

        return jsonify({"message": "Language updated successfully"}), 200

    except SQLAlchemyError as e:
        return jsonify({"message": "Database error occurred"}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500


@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_data = [
            {
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "age": user.age,
                "subscription_plan": user.subscription_plan  # Include subscription plan
            }
            for user in users
        ]
        return jsonify(users_data), 200
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {e}")
        return jsonify({"message": "Error fetching users"}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({"message": "An error occurred"}), 500


@user_bp.route('/update-subscription', methods=['POST'])
def update_subscription():
    try:
        data = request.json
        username = data.get('username')
        plan = data.get('plan')

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        user.subscription_plan = plan
        db.session.commit()
        return jsonify({"message": f"Subscription updated to {plan} plan"}), 200

    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {e}")
        return jsonify({"message": "Database error occurred"}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({"message": "An error occurred during subscription update"}), 500


import stripe

stripe.api_key = 'sk_test_51OUNa5G9oNaqIQuvQLhXlYR4UoykkeHxvIq3lWvcoNkZVgfg9o0Wp0WryBF5yDlkSkgEtgIjQ7iD7u30ZvVqHOhq00cqceFUVj'  # Replace with your Stripe secret key
import traceback


@user_bp.route('/confirm-payment', methods=['POST'])
def confirm_payment():
    try:
        data = request.json
        payment_method_id = data.get('paymentMethodId')
        subscription_info = data.get('subscriptionInfo')

        # Log received data for debugging
        print(f"Received payment method ID: {payment_method_id}")
        print(f"Received subscription info: {subscription_info}")

        # Create the PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=100,  # Amount in cents
            currency='usd',
            payment_method=payment_method_id,
            confirmation_method='manual',
            confirm=True,
            return_url='http://youtube.com'  # Replace with your actual return URL

        )
        username = data.get('username')

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        user.subscription_plan = subscription_info
        db.session.commit()
        # Update user's subscription in your database here
        # ...

        return jsonify({'success': True, 'status': intent['status']}), 200

    except stripe.error.CardError as e:
        # Handle the card error
        err = e.error
        print(f"Stripe CardError: {err.message}")
        return jsonify({'success': False, 'error': err.message}), 403

    except stripe.error.StripeError as e:
        # Handle general Stripe API errors
        print(f"Stripe API Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

    except Exception as e:
        # Handle other exceptions
        print(f"Internal Server Error: {str(e)}")
        traceback.print_exc()  # Print stack trace for debugging
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500
