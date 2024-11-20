import requests
from flask import Flask, request, jsonify

app= Flask(__name__)
@app.route("/", methods=["POST"])

def index():
    data = request.get_json()
    try:
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        source_amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name']

        # Log the received values for debugging
        print(f"Source: {source_currency}, Amount: {source_amount}, Target: {target_currency}")

        # Fetch conversion rate
        conversion_rate = fetch_conversion_factor(source_currency, target_currency)
        if conversion_rate:
            converted_amount = source_amount * conversion_rate
            # Respond back to Dialogflow with the result
            return jsonify({
                "fulfillmentText": f"{source_amount} {source_currency} equals {converted_amount:.2f} {target_currency}."
            })
        else:
            # If conversion rate is not available
            return jsonify({
                "fulfillmentText": "Sorry, I couldn't fetch the conversion rate at the moment. Please try again later."
            })
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({
            "fulfillmentText": "There was an error processing your request. Please check your input."
        })


def fetch_conversion_factor(source, target):
    # Use the ExchangeRate-API endpoint for currency conversion
    url = f"https://v6.exchangerate-api.com/v6/c1ce609f54c3081a6aae2d8e/pair/{source}/{target}"
    response = requests.get(url)
    if response.status_code == 200:
        response_data = response.json()
        # Extract the conversion rate
        return response_data.get("conversion_rate")
    else:
        print(f"API Error: {response.status_code}, {response.text}")
        return None


if __name__== "__main__":
    app.run(debug=True)