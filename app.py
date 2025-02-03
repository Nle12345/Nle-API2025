from flask import Flask, jsonify, request
import math

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
    if n < 2:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

# Helper function to check if a number is an Armstrong number
def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    length = len(digits)
    return sum([d ** length for d in digits]) == n

# Helper function to calculate the sum of digits
def sum_of_digits(n):
    return sum(int(d) for d in str(n))

# Helper function to get a fun fact (placeholder for now)
def get_fun_fact(n):
    return f"{n} is an interesting number!"

# API endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')
    
    # Check if the input is a valid number
    if not number or not number.lstrip('-').isdigit():
        return jsonify({
            "number": number,
            "error": True
        }), 400
    
    number = int(number)
    
    # Determine properties
    properties = []
    if is_prime(number):
        properties.append("prime")
    if is_perfect(number):
        properties.append("perfect")
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    # Prepare response
    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "class_sum": sum_of_digits(number),
        "fun_fact": get_fun_fact(number)
    }
    
    return jsonify(response), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)