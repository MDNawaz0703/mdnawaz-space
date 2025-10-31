import socket
import ssl
import json
from datetime import datetime
import requests

# SSL setup
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 12000))
s.listen(3)
print(" Server listening on port 12000...")

def fetch_weather_summary(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    forecast = {}

    for entry in data['list']:
        date = entry['dt_txt'].split()[0]
        temp = entry['main']['temp']
        desc = entry['weather'][0]['description']
        wind = entry['wind']['speed']
        humidity = entry['main']['humidity']

        # Take only one forecast per day (first occurrence)
        if date not in forecast:
            forecast[date] = {
                'date': date,
                'temp': temp,
                'description': desc,
                'wind': wind,
                'humidity': humidity
            }

        if len(forecast) == 5:
            break

    return list(forecast.values())

while True:
    client_socket, addr = s.accept()
    print(f" Connected with {addr}")
    try:
        conn = ssl_context.wrap_socket(client_socket, server_side=True)
        city = conn.recv(1024).decode().strip()
        print(f" Received city: {city}")

        api_key = '9c0deab4d5441d2ec7275c1472c3ee9d'
        forecast_data = fetch_weather_summary(api_key, city)

        if forecast_data:
            conn.send(json.dumps(forecast_data).encode())
        else:
            conn.send(b"[]")
        conn.close()
    except Exception as e:
        print(" Error:", e)
        client_socket.close()
