// Check if the browser supports speech recognition
if ('webkitSpeechRecognition' in window) {
    var speechRecognizer = new webkitSpeechRecognition();
    var isListening = false;
    var finalTranscript = ''; // To store the final recognized speech

    speechRecognizer.continuous = true; // Keep the recognition active
    speechRecognizer.interimResults = true; // Show interim results
    speechRecognizer.lang = 'en-US'; // Set language to English

    // Handle the results of speech recognition
    speechRecognizer.onresult = function(event) {
        var interimTranscript = '';
        for (var i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }
        document.getElementById('user-input').value = interimTranscript;
    };

    // Handle end of speech recognition
    speechRecognizer.onend = function() {
        if (finalTranscript.trim().length > 0) {
            appendMessage(finalTranscript, 'user'); // Display recognized speech as user message
            streamMessage(finalTranscript);
            finalTranscript = ''; // Reset the final transcript for the next recognition
        }
        isListening = false; // Reset listening state
    };

    // Handle the start and stop of speech recognition
    document.getElementById('microphone-button').addEventListener('click', function() {
        if (!isListening) {
            speechRecognizer.start();
            isListening = true;
        } else {
            speechRecognizer.stop();
            isListening = false;
        }
    });

    // Handle errors (optional)
    speechRecognizer.onerror = function(event) {
        console.error('Speech recognition error', event.error);
    };
} else {
    console.log('Your browser does not support speech recognition.');
    // Hide the microphone button if not supported
    document.getElementById('microphone-button').style.display = 'none';
}


function appendMessage(messageText, sender) {
    var chatBox = document.getElementById('chat-box');
    var messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);

    var textNode = document.createTextNode(messageText);
    messageDiv.appendChild(textNode);

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the new message
}


function streamMessage(userInput) {
    fetch('http://localhost:5000/stream', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => {
        const reader = response.body.getReader();
        let accumulatedText = '';
        let messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'bot');
        document.getElementById('chat-box').appendChild(messageDiv);

        function push() {
            reader.read().then(({ done, value }) => {
                if (done) {
                    console.log('Stream complete');
                    return;
                }
                accumulatedText += new TextDecoder().decode(value);

                try {
                    const lines = accumulatedText.split("\n");
                    for (let i = 0; i < lines.length - 1; i++) {
                        const data = JSON.parse(lines[i]);
                        if (data && data.reply) {
                            messageDiv.textContent += data.reply;
                        }
                    }
                    accumulatedText = lines[lines.length - 1]; // Keep the incomplete chunk for the next iteration
                } catch (error) {
                    console.error('Error parsing JSON:', error);
                }

                document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight; // Scroll to the new message
                push();
            });
        }
        push();
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        appendMessage(this.value, 'user'); // Display user message
        streamMessage(this.value);
        this.value = '';  // Clear the input field
    }
});

document.querySelector('button').addEventListener('click', function () {
    const userInputField = document.getElementById('user-input');
    appendMessage(userInputField.value, 'user'); // Display user message
    streamMessage(userInputField.value);
    userInputField.value = '';  // Clear the input field
});
