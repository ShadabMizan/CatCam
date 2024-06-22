from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'

@app.route('/', methods=['GET', 'POST'])
def home():
    # session is a Flask object that works similarly to a dictionary. Data from a session is available across different requests made by the same user.

    # Initializes show_data as true in the session object dictionary
    if 'pos_data' not in session:
        session['pos_data'] = True     

    if request.method == 'POST':
        action = request.form['action']
        if action == 'toggle_pos_data':     
            # Toggle pos_data
            session['pos_data'] = not session['pos_data']
            print("Show Position: ", session['pos_data'])

        # Implement a Post/Redirect/Get pattern, which helps prevent form resubmission and a clean url
        return redirect(url_for('home'))


    return render_template('index.html', pos_data=session['pos_data'])

if __name__ == '__main__':
    app.run(debug=True)

