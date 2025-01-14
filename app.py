from flask import Flask, render_template, jsonify,request, make_response, redirect, url_for
import qrcode
from io import BytesIO
import base64
app = Flask(__name__)

# Routes for rendering pages
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/instructions')
def instructions():
    return render_template('instructions.html')
@app.route('/secret_cameras')
def secret_cameras():
    return render_template('security_cameras.html')

@app.route('/flag_part2')
def flag_part2():
    return render_template('flag_part2.html')

@app.route('/secret_cameras/TheProfessorsCommunications')
def next_challenge():
    return render_template('TheProfessorsCommunications.html')

# API route to check answers
@app.route('/check-answer', methods=['POST'])
def check_answer():
    data = request.json
    question = data.get("question")
    user_answer = data.get("answer")

    # Define correct answers and logic
    correct_answers = {
        "camera_equation": "2333336",
        "binary_puzzle": "10101101",
    }

    if question == "binary_puzzle":
        if user_answer == correct_answers["binary_puzzle"]:
            return jsonify({
                "success": True,
                "message": "Success! Flag Part 2: _R1Tu4l_ \n\n..... Secret Quest: Solve the equation in Camera 2 feed to get the route to the next challenge! Check Comments near cam 2",
                "next_challenge_url": "/ProfessorsCommunication"
            })
        else:
            return jsonify({
                "success": False,
                "message": (
                    "Incorrect! Try again. Find the Binary equivalent of X.\n\n"
                    "Clues to find X are:\n\n"
                    "Clue 1: The number must be the highest prime less than 200 satisfying the other clues.\n"
                    "Clue 2: The number leaves a remainder of 3 when divided by 5.\n"
                    "Clue 3: The number minus 30 is divisible by 11."
                )
            })

    elif question == "camera_equation":
        if user_answer == correct_answers["camera_equation"]:
            return jsonify({
                "success": True,
                "message": "Correct! URL to the next challenge: /ProfessorsCommunication",
                "next_challenge_url": "/ProfessorsCommunication"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Incorrect! Try solving the equation again."
            })

    # If question not recognized
    return jsonify({
        "success": False,
        "message": "Invalid question or answer."
    })


@app.route('/ProfessorsCommunication')
def ProfessorsCommunication():
    return render_template('ProfessorsCommunicatoin.html')

# Route for checking MD5 hash of "hello"
@app.route('/md5_check', methods=['POST'])
def md5_check():
    user_input = request.form.get('hash')
    if user_input == '5d41402abc4b2a76b9719d911017c592':  # MD5 of "hello"
        return "Correct! Check the robots.txt for the next clue.", 200
    return "Incorrect hash. Try again!", 400

# robots.txt route
@app.route('/robots.txt')
def robots():
    response = make_response("User-agent: *\nDisallow: /bella-ciao\nHint: HESIT is the key!")
    response.headers["Content-Type"] = "text/plain"
    return response


@app.route('/set-cookie', methods=['POST'])
def set_cookie():
    # Check if the user sets the cookie to admin=true
    admin_cookie = request.cookies.get('admin')
    if admin_cookie == 'true':
        return redirect(url_for('admin_panel'))
    resp = make_response("Set the 'admin' cookie to 'true' and reload the page.")
    resp.set_cookie('admin', 'false')  # Set default cookie value
    return resp

@app.route('/bella-ciao')
def bella_ciao():
    admin_cookie = request.cookies.get('admin')
    if admin_cookie == 'true':
        return redirect('/admin-panel')  # Redirect to the Admin Panel if the cookie is set
    return render_template('bella_ciao.html')  # Show the "Bella Ciao" page otherwise


# Add this route to app.py
@app.route('/admin-panel')
def admin_panel():
    admin_cookie = request.cookies.get('admin')
    if admin_cookie == 'true':
        return render_template('admin_panel.html')
    return redirect(url_for('bella_ciao'))

@app.route('/book-cipher', methods=['POST'])
def book_cipher():
    user_input = request.form.get('cipher_words')
    # Correct answer is based on words from the book
    correct_words = "quick hobbit times ishmael question"
    if user_input.strip().lower() == correct_words:
        return {"message": "Correct! You've solved the Book Cipher.where does JavaScript print stuff 🤔", "next_part": "Flag Part 1/3: secuRIT{M@n1pulate_"}
    return {"message": "Incorrect! Try again."}


@app.route('/vigenere-cipher', methods=['POST'])
def vigenere_cipher():
    user_input = request.form.get('cipher_text')
    key = 'HEIST'
    encrypted_message = 'KIKJRWXQGG'
    decrypted_message = decrypt_vigenere(encrypted_message, key)

    if user_input.strip().lower() == decrypted_message.lower():
        return "route: /admin-panel/final-challenge'"
    return "Incorrect! Keep trying."

def decrypt_vigenere(cipher_text, key):
    """
    Decrypts a Vigenère cipher text with the given key.
    """
    key = key.upper()
    key_length = len(key)
    decrypted_text = []

    for i, char in enumerate(cipher_text):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)

@app.route('/qr-code')
def qr_code():
    # Example QR code data
    qr_data = "flag part 3/3: S3cur1ty}"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Generate the QR code image in memory
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Return the base64-encoded image
    base64_qr = base64.b64encode(buffer.read()).decode()
    return {"qr_code_base64": base64_qr}


@app.route('/admin-panel/final-challenge', methods=['GET', 'POST'])
def final_challenge():
    if request.method == 'POST':
        puzzle = request.form.get('puzzle')
        answer = request.form.get('answer')

        # Puzzle 1: Unique riddle challenge
        if puzzle == 'puzzle1':
            correct_answer = "time"  # Example riddle: "What has no body, but can cast a shadow?"
            if answer.strip().lower() == correct_answer:
                return {"message": "Awesome! password for the Hard Challenge: HEIST_COMPLETED_TIME_TOESCAPE"}
            else:
                return {"message": "Incorrect! Try again."}

        # Puzzle 2: Fun binary decoding challenge
        elif puzzle == 'puzzle2':
            correct_answer = "binary"  # Binary: 01100010 01101001 01101110 01100001 01110010 01111001
            if answer.strip().lower() == correct_answer:
                return {"message": "\n flag part 2/3: Th3_H31st_"}
            else:
                return {"message": "Incorrect! Try again."}

    return render_template('final_challenge.html')



BOOK_TEXT = """
1. The quick brown fox jumps over the lazy dog.
2. In a hole in the ground, there lived a hobbit.
3. It was the best of times, it was the worst of times.
4. Call me Ishmael.
5. To be or not to be, that is the question.
"""

@app.route('/book/<int:page>')
def book(page):
    lines = BOOK_TEXT.strip().split("\n")
    if 1 <= page <= len(lines):
        return {"page": page, "text": lines[page - 1]}
    return {"error": "Page not found"}, 404



if __name__ == '__main__':
    app.run(debug=True)
