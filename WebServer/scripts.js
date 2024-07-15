// Initialize the map and set its view to a default location
let map = null;
let marker = null;

function initMap() 
{
    map = L.map('map').setView([0, 0], 19);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}

function fetchGPSData() 
{
    fetch('/gps')
        .then(response => response.json())
        .then(data => {
            // Satellite Data
            document.getElementById('satellites').textContent = data.satellites;
            document.getElementById('latitude').textContent = data.latitude;
            document.getElementById('longitude').textContent = data.longitude;
            
            // Convert to AM or PM
            let myHour = data.hour;
            let myMinute = data.minute;
            let mySecond = data.second;
            if (myHour > 12) {
                myHour -= 12;
                document.getElementById('pm').textContent = "PM";
            } else {
                document.getElementById('pm').textContent = "AM";
            }

            if (myHour < 10) {
                document.getElementById('hour').textContent = "0" + myHour;
            } else {
                document.getElementById('hour').textContent = myHour;
            }

            if (myMinute < 10) {
                document.getElementById('minute').textContent = "0" + myMinute;
            } else {
                document.getElementById('minute').textContent = myMinute;
            }

            if (mySecond < 10) {
                document.getElementById('second').textContent = "0" + mySecond;
            } else {
                document.getElementById('second').textContent = mySecond;
            }

            // Update the map location
            const latLng = [data.latitude, data.longitude];
            if (marker) {
                marker.setLatLng(latLng);
            } else {
                marker = L.marker(latLng).addTo(map);
            }
            map.setView(latLng, 19);
        })
        .catch(error => console.error('Error fetching GPS data:', error));
}

// Fetch GPS data every 5 seconds
setInterval(fetchGPSData, 5000);

// Fetch GPS data immediately on page load
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    fetchGPSData();
});
