import os
import json
from flask import Blueprint, request, Response, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, url_for
from models.User import User
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


