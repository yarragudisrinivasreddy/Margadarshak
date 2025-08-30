from flask import Flask, render_template, request, jsonify
import openai
import requests

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "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"

# Optional: OpenWeather API
OPENWEATHER_KEY = "c485c07fe2d89be6f9222b9878a2b782"

def get_weather(location):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_KEY}&units=metric"
        res = requests.get(url).json()
        if "main" in res:
            return f"{res['weather'][0]['description']}, {res['main']['temp']}°C"
        return "Weather data not available"
    except Exception as e:
        print(f"Weather API error: {e}")
        return "Weather data not available"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"reply": "⚠️ Please type a message."})

        # Extract keywords (simple rules)
        budget = "unknown"
        location = "unknown"
        if "budget" in user_message.lower():
            budget = ''.join([c for c in user_message if c.isdigit()]) or "unknown"
        if "college" in user_message.lower():
            location = "college"
        elif "metro" in user_message.lower():
            location = "metro station"

        # Get weather info
        weather_info = get_weather("Hyderabad") if location != "unknown" else "N/A"

        # Prompt for AI
        prompt = f"""
        You are an AI assistant for Indian street vendors.
        Vendor input: {user_message}
        Budget: {budget}
        Location: {location}
        Weather: {weather_info}

        👉 Format your response like this (Markdown-style, WhatsApp friendly):

        ✅ Suggested Stock:
        - Item 1 (qty)
        - Item 2 (qty)

        💰 Expected Profit: INR xxx – yyy
        🌤 Weather Advice: ...
        📍 Location Advice: ...

        Keep it short and clear, use emojis where useful.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for vendors."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )

        # Safe access to reply
        reply = response["choices"][0]["message"].get("content", "").strip()
        if not reply:
            reply = "⚠️ Sorry, I couldn't generate a response. Please try again."

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error in /chat: {e}")
        return jsonify({"reply": f"⚠️ An error occurred: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
