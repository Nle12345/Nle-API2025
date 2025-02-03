from flask import Flask, request, jsonify
import math
import requests

app = Flask(__name__)

# Helper functions

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def is_perfect(n):
    """Check if a number is perfect."""
    if n <= 1:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    if n < 0:
        return False
    digits = [int(digit) for digit in str(n)]
    return n == sum([digit ** len(digits) for digit in digits])

def digit_sum(n):
    """Calculate the sum of the digits of a number."""
    return sum(int(digit) for digit in str(abs(n)))

def get_fun_fact(n):
    """Fetch a fun fact about the number using the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        if response.status_code == 200:
            return response.text
        return "No fun fact available."
    except requests.RequestException:
        return "No fun fact available."

# API route for classifying numbers
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        # Get the number from the query parameters
        number = request.args.get('number', type=int)
        
        # Validate the input
        if number is None:
            return jsonify({
                "number": "alphabet",
                "error": True
            }), 400
        
        # Handle negative numbers
        if number < 0:
            return jsonify({
                "number": number,
                "is_prime": False,
                "is_perfect": False,
                "properties": ["negative"],
                "digit_sum": digit_sum(number),
                "fun_fact": "No fun fact available for negative numbers."
            }), 200
        
        # Check properties of the number
        prime = is_prime(number)
        perfect = is_perfect(number)
        armstrong = is_armstrong(number)
        properties = []
        
        # Assign properties based on number classification
        if armstrong:
            properties.append("armstrong")
        if number % 2 == 0:
            properties.append("even")
        else:
            properties.append("odd")
        
        # Fetch fun fact
        fun_fact = get_fun_fact(number)
        
        # Create the response JSON
        response = {
            "number": number,
            "is_prime": prime,
            "is_perfect": perfect,
            "properties": properties,
            "digit_sum": digit_sum(number),
            "fun_fact": fun_fact
        }
        
        # Return the JSON response with 200 OK status
        return jsonify(response), 200

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({
            "error": str(e)
        }), 500

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)