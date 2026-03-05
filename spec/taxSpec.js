/**
 * Jasmine unit tests for the Tax Calculator module.
 * 7 specs covering configuration loading, bracket calculations, and edge cases.
 */

const { calculateTax, loadTaxConfig } = require("../tax_calculator/tax");

const sampleConfig = {
  tax_brackets: [
    { min: 0, max: 10000, rate: 0.10 },
    { min: 10000, max: 40000, rate: 0.20 },
    { min: 40000, max: 85000, rate: 0.30 },
    { min: 85000, max: null, rate: 0.35 },
  ],
  standard_deduction: 12000,
};

describe("Tax Calculator", function () {

  // Spec 1
  it("should load the default tax configuration", function () {
    const config = loadTaxConfig();
    expect(config.tax_brackets).toBeDefined();
    expect(config.standard_deduction).toBeDefined();
    expect(config.tax_brackets.length).toBeGreaterThan(0);
  });

  // Spec 2
  it("should return zero tax for income below the standard deduction", function () {
    const result = calculateTax(10000, sampleConfig);
    expect(result.taxable_income).toBe(0);
    expect(result.total_tax).toBe(0);
  });

  // Spec 3
  it("should calculate tax correctly for income in the first bracket only", function () {
    // Income 20000 → taxable 8000, all in 10% bracket → 800
    const result = calculateTax(20000, sampleConfig);
    expect(result.taxable_income).toBe(8000);
    expect(result.total_tax).toBe(800);
  });

  // Spec 4
  it("should calculate tax correctly across two brackets", function () {
    // Income 30000 → taxable 18000
    // First 10k @ 10% = 1000, next 8k @ 20% = 1600 → 2600
    const result = calculateTax(30000, sampleConfig);
    expect(result.taxable_income).toBe(18000);
    expect(result.total_tax).toBe(2600);
  });

  // Spec 5
  it("should calculate tax correctly across all four brackets", function () {
    // Income 112000 → taxable 100000
    // 10k@10%=1000, 30k@20%=6000, 45k@30%=13500, 15k@35%=5250 → 25750
    const result = calculateTax(112000, sampleConfig);
    expect(result.taxable_income).toBe(100000);
    expect(result.total_tax).toBe(25750);
  });

  // Spec 6
  it("should compute the correct effective tax rate", function () {
    const result = calculateTax(112000, sampleConfig);
    const expectedRate = parseFloat(((25750 / 112000) * 100).toFixed(2));
    expect(result.effective_rate).toBe(expectedRate);
  });

  // Spec 7
  it("should throw an error for negative income", function () {
    expect(function () {
      calculateTax(-5000, sampleConfig);
    }).toThrowError("Income cannot be negative");
  });

});
