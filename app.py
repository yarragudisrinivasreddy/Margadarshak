from flask import Flask, render_template, request, jsonify
import openai
import requests
# Example usage with your working system
from complete_commerce_orchestrator import CompleteCommerceOrchestrator
app = Flask(__name__)
# Initialize complete system
orchestrator = CompleteCommerceOrchestrator(
    excel_file_path="synthetic_commerce_data.xlsx",
    openai_api_key="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",
    weather_api_key="c485c07fe2d89be6f9222b9878a2b782"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"reply": "⚠️ Please type a message."})

        reply = orchestrator.process_user_query(user_message)
        if not reply:
            reply = "⚠️ Sorry, I couldn't generate a response. Please try again."

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error in /chat: {e}")
        return jsonify({"reply": f"⚠️ An error occurred: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
