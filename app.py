from flask import Flask, request, jsonify
import math 

app = Flask(__name__)

# Helper functions

# Function to check if the number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if the number is perfect
def is_perfect(n):
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

# Function to check if the number is an Armstrong number
def is_armstrong(n):
    if n < 0:
        return False  # Armstrong numbers are typically defined for positive integers
    digits = [int(digit) for digit in str(n)]
    return n == sum([digit ** len(digits) for digit in digits])

# Function to calculate the sum of the digits
def digit_sum(n):
    return sum([int(digit) for digit in str(abs(n))])  # Use abs to handle negative numbers

# Function to get the fun fact about the number (Math type from Numbers API)
def get_fun_fact(n):
    if n < 0:
        return "No fun fact available for negative numbers."
    return f"{n} is an Armstrong number because " + " + ".join([f"{d}^3" for d in str(n)]) + f" = {n}"

# API route for classifying numbers
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        # Get the number from the query parameters
        number = request.args.get('number', type=int)
        
        # If the number is invalid (not a valid integer)
        if number is None:
            return jsonify({
                "number": "alphabet", 
                "error": True
            }), 400
        
        # Check properties of the number
        prime = is_prime(abs(number))  # Use abs to handle negative numbers
        perfect = is_perfect(abs(number))  # Use abs to handle negative numbers
        armstrong = is_armstrong(number)
        properties = []
        
        # Assign properties based on number classification
        if armstrong:
            properties.append("armstrong")
        if number % 2 == 0:
            properties.append("even")
        else:
            properties.append("odd")
        
        # Fun fact about the number
        fun_fact = get_fun_fact(number) if armstrong else "No fun fact available."
        
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)