"""
Tax Calculator Module
Calculates federal income tax based on configurable tax brackets.
"""

import json
import os


def load_tax_config(config_path=None):
    """Load tax configuration from a JSON file.

    Args:
        config_path (str): Path to the configuration file.
            Defaults to config.json in the same directory.

    Returns:
        dict: Tax configuration containing brackets and deductions.
    """
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")

    with open(config_path, "r") as f:
        config = json.load(f)

    return config


def calculate_tax(annual_income, config=None):
    """Calculate the federal income tax for a given annual income.

    Tax is calculated using progressive tax brackets loaded from
    an external configuration file (not hard-coded).

    Args:
        annual_income (float): The gross annual income.
        config (dict, optional): Tax configuration dictionary.
            If not provided, loads from the default config file.

    Returns:
        dict: A dictionary with detailed tax breakdown:
            - gross_income
            - standard_deduction
            - taxable_income
            - tax_brackets_applied (list)
            - total_tax
            - effective_rate
    """
    if config is None:
        config = load_tax_config()

    brackets = config["tax_brackets"]
    standard_deduction = config.get("standard_deduction", 0)

    gross_income = float(annual_income)
    if gross_income < 0:
        raise ValueError("Income cannot be negative")

    taxable_income = max(0, gross_income - standard_deduction)

    total_tax = 0.0
    brackets_applied = []

    for bracket in brackets:
        b_min = bracket["min"]
        b_max = bracket["max"]
        rate = bracket["rate"]

        if taxable_income <= b_min:
            break

        upper = taxable_income if b_max is None else min(taxable_income, b_max)
        amount_in_bracket = upper - b_min
        tax_for_bracket = amount_in_bracket * rate

        brackets_applied.append({
            "range": f"${b_min:,.0f} - ${upper:,.0f}",
            "rate": f"{rate * 100:.0f}%",
            "tax": round(tax_for_bracket, 2),
        })

        total_tax += tax_for_bracket

    total_tax = round(total_tax, 2)
    effective_rate = round((total_tax / gross_income) * 100, 2) if gross_income > 0 else 0.0

    return {
        "gross_income": gross_income,
        "standard_deduction": standard_deduction,
        "taxable_income": taxable_income,
        "tax_brackets_applied": brackets_applied,
        "total_tax": total_tax,
        "effective_rate": effective_rate,
    }
