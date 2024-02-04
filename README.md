# Jasmine-Flask

# Flask Real Estate API

This Flask application receives POST requests from the frontend and fetches real estate data using the Repliers API.

## Prerequisites

- Python 3.x
- Flask
- PyCharm (recommended IDE for this project)

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/jasmine-artificial-intelligence/Jasmine-Flask.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Jasmine-Flask
   ```

3. (Optional) It's recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Using PyCharm:

1. Open the project in PyCharm.
2. Set up the interpreter using the virtual environment you created.
3. Right-click on `app.py` and choose `Run`.

### Using Command Line:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

This will start the Flask development server, and the application will be accessible at `http://127.0.0.1:5000/`.

## Contributing

For any suggestions or contributions, please create an issue or submit a pull request.

## Acknowledgments

- Repliers API for real estate data.
- Flask community for the web framework.
