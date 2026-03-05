"""
Flask web application for the Tax Calculator.
"""

from flask import Flask, render_template, request, jsonify
from tax_calculator.tax import calculate_tax, load_tax_config

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Render the main Tax Calculator page."""
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    """API endpoint to calculate tax from submitted income."""
    try:
        income = request.form.get("income", type=float)
        if income is None:
            return jsonify({"error": "Please provide a valid income"}), 400

        result = calculate_tax(income)
        return jsonify(result)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An internal error occurred"}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for the deployment pipeline."""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
