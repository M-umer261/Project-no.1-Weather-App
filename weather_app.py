import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

# OpenWeatherMap API key (replace with your key)
API_KEY = "96310405244f43a0a2ca19ea4ca31ffe"

# Function to fetch real-time weather data
def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return

    # API URL for current weather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        # Check if the city was found
        if data.get("cod") != 200:
            messagebox.showerror("Error", "City not found! Please enter a valid city name.")
            return

        # Extract weather data
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]
        weather_info = f"Temperature: {temp}°C\nHumidity: {humidity}%\nCondition: {weather.capitalize()}"
        weather_label.config(text=weather_info)

        # Fetch and display 7-day forecast
        get_forecast(city)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to fetch 7-day forecast
def get_forecast(city):
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(forecast_url)
        data = response.json()

        # Check if the forecast data was fetched successfully
        if data.get("cod") != "200":
            messagebox.showerror("Error", "Unable to fetch forecast data.")
            return

        # Organize forecast data by day
        daily_temps = {}
        for entry in data["list"]:
            date = entry["dt_txt"].split(" ")[0]  # Extract date
            temp = entry["main"]["temp"]
            condition = entry["weather"][0]["description"]
            if date not in daily_temps:
                daily_temps[date] = (temp, condition)

        # Format forecast for display
        forecast_data = ""
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for i, (date, (temp, condition)) in enumerate(daily_temps.items()):
            forecast_data += f"{days[i % 7]}: {temp}°C, {condition.capitalize()}\n"

        # Update forecast label
        forecast_label.config(text=forecast_data)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI Setup
# Initialize the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("450x600")
root.configure(bg="#F0F0F0")  # Light gray background

# Load and display the app icon
try:
    icon = Image.open("weather_icon.png")  # Ensure you have this file in the same directory
    icon = icon.resize((120, 120), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon)
    icon_label = tk.Label(root, image=icon_photo, bg="#F0F0F0")
    icon_label.pack(pady=10)
except Exception as e:
    print(f"Error loading icon: {e}")

# Title Label
tk.Label(
    root,
    text="Weather Forecast",
    font=("Helvetica", 24, "bold"),
    bg="#F0F0F0",
    fg="#333333"  # Dark gray text
).pack(pady=10)

# City Input Frame
input_frame = tk.Frame(root, bg="#F0F0F0")
input_frame.pack(pady=10)

# City Input Field
city_entry = tk.Entry(
    input_frame,
    font=("Arial", 14),
    bg="white",
    fg="#333333",
    relief="flat",
    bd=2,
    width=25
)
city_entry.pack(side=tk.LEFT, padx=5)

# Search Button
search_button = tk.Button(
    input_frame,
    text="Get Weather",
    font=("Arial", 10, "bold"),
    bg="#4CAF50",  # Green color
    fg="white",
    relief="flat",
    padx=10,
    pady=5,
    command=get_weather
)
search_button.pack(side=tk.LEFT)

# Weather Details Frame
weather_frame = tk.Frame(root, bg="#F0F0F0")
weather_frame.pack(pady=10)

# Weather Details Label
weather_label = tk.Label(
    weather_frame,
    text="",
    font=("Arial", 14),
    bg="#F0F0F0",
    fg="#333333",
    justify="left",
    padx=10,
    pady=5
)
weather_label.pack()

# Forecast Title
tk.Label(
    root,
    text="7-Day Forecast",
    font=("Helvetica", 18, "bold"),
    bg="#F0F0F0",
    fg="#333333"
).pack(pady=12)

# Forecast Data Frame
forecast_frame = tk.Frame(root, bg="#F0F0F0")
forecast_frame.pack(pady=5)

# Forecast Data Label
forecast_label = tk.Label(
    forecast_frame,
    text="",
    font=("Arial", 12),
    bg="#F0F0F0",
    fg="#333333",
    justify="left",
    padx=10,
    pady=5
)
forecast_label.pack()

# Run the application
root.mainloop()