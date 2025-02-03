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
    digits = [int(d) for d in str(abs(n))]  # Ignore negative sign for Armstrong check
    length = len(digits)
    return sum([d ** length for d in digits]) == abs(n)

# Helper function to calculate the sum of digits
def sum_of_digits(n):
    return sum(int(d) for d in str(abs(n)))  # Ignore negative sign for sum of digits

# Helper function to get a fun fact (armstrong number specific)
def get_fun_fact(n):
    if is_armstrong(n):
        digits = [int(d) for d in str(n)]
        length = len(digits)
        # Armstrong fact
        return f"{n} is an Armstrong number because " + " + ".join([f"{d}^{length}" for d in digits]) + f" = {n}"
    return f"{n} is an interesting number!"

# API endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    # Check if the input is a valid integer
    try:
        number = int(number)  # Convert the string input to an integer
    except (ValueError, TypeError):
        return jsonify({
            "number": number,
            "error": True
        }), 400

    # Determine properties
    properties = []

    # Check properties specific to integers
    if is_armstrong(number):
        properties.append("armstrong")
    if is_prime(number):
        properties.append("prime")
    if is_perfect(number):
        properties.append("perfect")
    
    # Determine even or odd
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    # Prepare response for integers
    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum_of_digits(number),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response), 200


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
