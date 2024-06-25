from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'

# GPS Data storage in memory
gpsData = {'latitude': None, 'longitude': None, 'satellites': None}

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

    return render_template('index.html', pos_data=session['pos_data'], satellites=gpsData['satellites'], lat=gpsData['latitude'], lng=gpsData['longitude'])

@app.route('/gps', methods=['GET', 'POST'])
def gps():
    try:
        content = request.get_json()

        gpsData['latitude'] = content['latitude']
        gpsData['longitude'] = content['longitude']
        gpsData['satellites'] = content['satellites']

        print(f"Received: latitude = {gpsData['latitude']}, longitude = {gpsData['longitude']}, satellites = {gpsData['satellites']}\n")
        return jsonify({'success' : True})
    except Exception as e:
        print(f"Error receiving data: {str(e)}")
        return jsonify({'success' : False, 'error': str(e)})




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

