/**
 * Tax Calculator Module
 * Calculates federal income tax based on configurable tax brackets.
 */

const fs = require("fs");
const path = require("path");

/**
 * Load tax configuration from a JSON file.
 * @param {string} [configPath] - Path to config file. Defaults to config.json.
 * @returns {object} Tax configuration with brackets and deductions.
 */
function loadTaxConfig(configPath) {
  if (!configPath) {
    configPath = path.join(__dirname, "config.json");
  }
  const raw = fs.readFileSync(configPath, "utf-8");
  return JSON.parse(raw);
}

/**
 * Calculate federal income tax for a given annual income.
 * @param {number} annualIncome - Gross annual income.
 * @param {object} [config] - Tax configuration object. Loaded from file if omitted.
 * @returns {object} Tax breakdown with gross_income, standard_deduction,
 *   taxable_income, tax_brackets_applied, total_tax, effective_rate.
 */
function calculateTax(annualIncome, config) {
  if (!config) {
    config = loadTaxConfig();
  }

  const grossIncome = parseFloat(annualIncome);
  if (isNaN(grossIncome) || grossIncome < 0) {
    throw new Error("Income cannot be negative");
  }

  const standardDeduction = config.standard_deduction || 0;
  const taxableIncome = Math.max(0, grossIncome - standardDeduction);
  const brackets = config.tax_brackets;

  let totalTax = 0;
  const bracketsApplied = [];

  for (const bracket of brackets) {
    const bMin = bracket.min;
    const bMax = bracket.max;
    const rate = bracket.rate;

    if (taxableIncome <= bMin) break;

    const upper = bMax === null ? taxableIncome : Math.min(taxableIncome, bMax);
    const amountInBracket = upper - bMin;
    const taxForBracket = parseFloat((amountInBracket * rate).toFixed(2));

    bracketsApplied.push({
      range: `$${bMin.toLocaleString()} - $${upper.toLocaleString()}`,
      rate: `${(rate * 100).toFixed(0)}%`,
      tax: taxForBracket,
    });

    totalTax += taxForBracket;
  }

  totalTax = parseFloat(totalTax.toFixed(2));
  const effectiveRate =
    grossIncome > 0
      ? parseFloat(((totalTax / grossIncome) * 100).toFixed(2))
      : 0;

  return {
    gross_income: grossIncome,
    standard_deduction: standardDeduction,
    taxable_income: taxableIncome,
    tax_brackets_applied: bracketsApplied,
    total_tax: totalTax,
    effective_rate: effectiveRate,
  };
}

module.exports = { calculateTax, loadTaxConfig };
