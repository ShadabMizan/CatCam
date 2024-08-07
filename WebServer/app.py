from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'

# GPS Data storage in memory
gpsData = {'latitude': None, 'longitude': None, 'satellites': None, 'hour': None, 'minute': None, 'second': None}

# PST OFFSET 


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/gps', methods=['GET', 'POST'])
def gps():
    if request.method == 'POST':        # Runs when the ESP32 POSTs gps data to the server
        try:
            content = request.get_json()
            gpsData['latitude'] = content['latitude']
            gpsData['longitude'] = content['longitude']
            gpsData['satellites'] = content['satellites']

            # Deal with Hour conversion between UTC to PST. UTC is 7 hours ahead of PST.
            pstOffset = 7
            utcTime = content['hour']
        
            # myHour = utcTime - pstOffset
            myHour = None

            # Causes a negative hour
            if utcTime < pstOffset:
                myHour = utcTime - pstOffset + 24
            else:
                myHour = utcTime - pstOffset

            gpsData['hour'] = myHour
            gpsData['minute'] = content['minute']
            gpsData['second'] = content['second']

            print(f"Received: latitude = {gpsData['latitude']}, longitude = {gpsData['longitude']}, satellites = {gpsData['satellites']}\nTime: {gpsData['hour']}:{gpsData['minute']}:{gpsData['second']}\n")
            return jsonify({'success': True})
        except Exception as e:
            print(f"Error receiving data: {str(e)}")
            return jsonify({'success': False, 'error': str(e)})
    elif request.method == 'GET':       # Runs when the JavaScript makes a GET request to the server
        return jsonify(gpsData)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
