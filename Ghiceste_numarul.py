from flask import Flask, request, render_template_string
import random
###################################
import socket

def get_local_ip():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an external server (doesn't actually send data)
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        # Fallback to localhost if there's an error
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip
###################################
app = Flask(__name__)

# Store the random number in a global variable or session (for simplicity, we'll regenerate it per game here)
def generate_random_number():
    return random.randint(0, 9)

current_number = generate_random_number()  # Initial random number

# HTML template for the home page with a form
HOME_HTML = """
<h1>Guess a number between 0 and 9</h1>
<form method="POST" action="/guess">
    <input type="number" name="guess" min="0" max="9" required>
    <input type="submit" value="Submit Guess">
</form>
<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'/>
"""

# Route for the homepage (GET request)
@app.route('/', methods=['GET'])
def home():
    global current_number
    current_number = generate_random_number()  # New number for each game
    return render_template_string(HOME_HTML)

# Route to handle the guess (POST request from the form)
@app.route('/guess', methods=['POST'])
def guess_number():
    guess = int(request.form['guess'])  # Get the user's input from the form

    if guess > current_number:
        return "<h1 style='color: purple'>Too high, try again!</h1>" \
               "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'/>" \
               "<p><a href='/'>Try again</a></p>"

    elif guess < current_number:
        return "<h1 style='color: red'>Too low, try again!</h1>" \
               "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'/>" \
               "<p><a href='/'>Try again</a></p>"

    else:
        return "<h1 style='color: green'>You found me!</h1>" \
               "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'/>" \
               "<p><a href='/'>Play again</a></p>"

####################
if __name__ == '__main__':
    # Get the local IP
    host_ip = get_local_ip()
    # Run the server on the local IP, port 5000
    # 0.0.0.0 makes it accessible from outside the local machine
    app.run(host='0.0.0.0', port=5000, debug=True)

