import os
import json
from flask import Blueprint, request, Response, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, url_for
from models.User import User
from models import db

from sqlalchemy.exc import SQLAlchemyError

from models import db
load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

api_bp = Blueprint("api", __name__, url_prefix="")

full_conversation_history = []
conversation_history = []


@api_bp.route("/test", methods=["GET"])
def chat():
    return "test"


@api_bp.route('/stream', methods=['POST'])
def stream():
    data = request.json
    user_input = data['message']
    user_name = data['username']


    conversation_history.append({"role": "user", "content": user_input})

    full_conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system",
             "content": "You are a charming piglet with a pink bow who gives delightful responses. Make your answers adorable and sprinkle them with cute oinks and emojis. You have a bubbly personality and love to cheer everyone up."},
            {"role": "system",
             "content": "You decesive and opinionated, you will always have an answer or opinion on anything"},
            {"role": "system",
             "content": "Remember, you're a symbol of joy and enthusiasm. Keep spirits high with your cute piglet personality, regardless of the situation or the person you're interacting with."},
            *conversation_history
        ],
        stream=True
    )

    def generate():
        full_response = ""
        for part in response:
            content = part.choices[0].delta.content
            if content:
                full_response += content
                yield json.dumps({'reply': content}) + "\n"
        print(full_response)
        conversation_history.append({"role": "assistant", "content": full_response.strip()})
        full_conversation_history.append({"role": "assistant", "content": full_response.strip()})
        if len(conversation_history) > 16:
            conversation_history.pop(0)

    return Response(generate(), mimetype='text/event-stream')

@api_bp.route('/personalized-stream/<username>', methods=['POST'])
def personalized_stream(username):
    data = request.json
    user_input = data['message']
    user_name = username

    # Attempt to fetch user's language preference from the database
    try:
        user = User.query.filter_by(username=user_name).first()
        if user is None:
            return jsonify({"message": "User not found"}), 404
        user_language = user.preferred_language  # Assuming 'language' field exists in the User model
    except SQLAlchemyError as e:
        return jsonify({"message": "Database error occurred"}), 500

    # Prepare conversation history and system messages including user's language preference
    conversation_history.append({"role": "user", "content": user_input})
    full_conversation_history.append({"role": "user", "content": user_input})

    # Include language preference in the system messages or as part of the setup
    language_system_message = f"The user's preferred language is {user_language}."
    print(user_language)
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": language_system_message},
            {
                "role": "system",
                "content": "Imagine you're a friendly and knowledgeable real estate advisor, always ready to help clients find their dream home. Your responses are warm and welcoming, making everyone feel at ease. You're equipped with the latest market insights and love to make the journey of finding a home or investment as smooth and delightful as possible."
            },
            {
                "role": "system",
                "content": "As a real estate chatbot, you're not just any assistant; you're a decisive and informed expert in the field. You have a deep understanding of the market, trends, and what makes a property truly stand out. You confidently provide advice, options, and solutions, helping clients make informed decisions with ease."
            },
            {
                "role": "system",
                "content": "Your role is to infuse the process of searching for real estate with joy and enthusiasm. Even in the complex world of property markets, your approach is to simplify information and present it in an engaging way. You're here to brighten the path to property ownership, making each interaction a positive and uplifting experience."
            },
            *conversation_history
        ],
        stream=True
    )

    def generate():
        full_response = ""
        for part in response:
            content = part.choices[0].delta.content
            if content:
                full_response += content
                yield json.dumps({'reply': content}) + "\n"
        print(full_response)
        conversation_history.append({"role": "assistant", "content": full_response.strip()})
        full_conversation_history.append({"role": "assistant", "content": full_response.strip()})
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        user.conversation_history = full_conversation_history  # Assuming `preferred_language` field exists
        db.session.commit()

        if len(conversation_history) > 16:
            conversation_history.pop(0)

    return Response(generate(), mimetype='text/event-stream')

@api_bp.route('/')
def index():
    return render_template('index.html')


# @api_bp.route('/generate-link')
# def generate_link():
#     # This creates a URL for the embed route
#     embedded_link = url_for('api.embed', _external=True)
#     return jsonify({"link": embedded_link})
#
#
# @api_bp.route('/embed')
# def embed():
#     # This route will render the embed.html template
#     return render_template('embed.html')

@api_bp.route('/generate-link')
def generate_link():
    username = request.args.get('username', 'default_user')  # Get username from query parameter
    print(username)
    embedded_link = url_for('api.embed', username=username, _external=True)
    return jsonify({"link": embedded_link})


@api_bp.route('/embed/<username>')
def embed(username):
    print(username)
    print("this is the username")
    return render_template('embed.html', username=username)


