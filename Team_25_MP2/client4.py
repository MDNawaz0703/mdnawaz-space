import tkinter as tk
from tkinter import *
from tkinter import ttk
import socket
import json
import ssl

def fetch_weather_data(city):
    context = ssl._create_unverified_context()
    conn = socket.create_connection(('192.168.1.26', 12000))
    ssl_client = context.wrap_socket(conn, server_hostname='192.168.1.1')
    ssl_client.send(bytes(city, 'utf-8'))
    rec_data = ssl_client.recv(20480).decode()
    ssl_client.close()
    return json.loads(rec_data)

def display_weather_info():
    city = city_entry.get()
    forecast_data = fetch_weather_data(city)

    current_row = 1
    forecast_weather_label.config(text="5-Day Forecast:")

    for entry in forecast_data:
        date = entry['date']
        desc = entry['description'].capitalize()
        temp = entry['temp']
        wind = entry['wind']
        humidity = entry['humidity']

        if temp > 34:
            alert = "🔥 High Temp (Careful!)"
        elif temp < 30:
            alert = "✅ Safe"
        else:
            alert = "⚠️ Moderate"

        summary = f"{date} | {desc} | Temp: {temp}°C | Wind: {wind} km/h | Humidity: {humidity}% | Alert: {alert}"
        label = tk.Label(second_frame, text=summary, bg="white", fg="black")
        label.grid(row=current_row, column=0, columnspan=3, sticky="w", pady=2)
        current_row += 1

root = tk.Tk()
root.title("5-Day Weather Forecast")
root.configure(bg="white")
root.geometry("800x600")

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

second_frame = Frame(my_canvas, bg="white")
my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

city_label = tk.Label(second_frame, text="Enter city:", bg="white", fg="black")
city_label.grid(row=0, column=0, padx=10, pady=10)

city_entry = tk.Entry(second_frame)
city_entry.grid(row=0, column=1, padx=10)

submit_button = tk.Button(second_frame, text="Fetch Weather", command=display_weather_info, bg="black", fg="white")
submit_button.grid(row=0, column=2, padx=10)

forecast_weather_label = tk.Label(second_frame, text="", bg="white", fg="black")
forecast_weather_label.grid(row=1, column=0, columnspan=3, pady=10)

root.mainloop()
