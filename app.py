from flask import Flask, jsonify, request
import math
import requests

app = Flask(__name__)

# Helper function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Helper function to check if a number is perfect
def is_perfect(n):
    if n < 1:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

# Helper function to check if a number is an Armstrong number
def is_armstrong(n):
    digits = [int(d) for d in str(abs(n))]  # Ignore negative sign for Armstrong check
    length = len(digits)
    return sum([d ** length for d in digits]) == abs(n)

# Helper function to calculate the sum of digits
def sum_of_digits(n):
    return sum(int(d) for d in str(abs(n)) if d.isdigit())  # Works for both integers and floats

# Helper function to get a fun fact from Numbers API
def get_fun_fact(n):
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        if response.status_code == 200:
            return response.text
        else:
            return f"{n} is an interesting number!"
    except Exception:
        return f"Could not fetch a fun fact for {n}."

# API endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    # Check if the input is a valid number (integer or floating-point)
    try:
        number = float(number)  # Convert the string input to a float
    except (ValueError, TypeError):
        return jsonify({
            "number": number,
            "error": True,
            "message": "Invalid input. Please provide a valid number."
        }), 400

    # Determine properties
    properties = []

    # Handle integers separately from floating-point numbers
    if number.is_integer():  # Check if it's an integer value
        integer_value = int(number)
        
        # Check properties specific to integers
        if is_prime(integer_value):
            properties.append("prime")
        if is_perfect(integer_value):
            properties.append("perfect")
        if is_armstrong(integer_value):
            properties.append("armstrong")
        
        # Determine even or odd
        if integer_value % 2 == 0:
            properties.append("even")
        else:
            properties.append("odd")

        # Prepare response for integers
        response = {
            "number": integer_value,
            "is_prime": is_prime(integer_value),
            "is_perfect": is_perfect(integer_value),
            "properties": properties,
            "digit_sum": sum_of_digits(integer_value),
            "fun_fact": get_fun_fact(integer_value)
        }
    
    else:  # Handle floating-point numbers
        digit_sum = sum_of_digits(number)  # Sum of digits for float
        
        response = {
            "number": number,
            "is_prime": False,
            "is_perfect": False,
            "properties": ["floating-point"],  # Explicitly include 'floating-point'
            "digit_sum": digit_sum,
            "fun_fact": get_fun_fact(number)
        }

    return jsonify(response), 200


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
