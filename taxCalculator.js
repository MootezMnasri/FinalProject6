/**
 * Tax Calculator - browser module
 * Progressive tax bracket calculation
 */

const taxConfig = {
  tax_brackets: [
    { min: 0, max: 10000, rate: 0.10 },
    { min: 10000, max: 40000, rate: 0.20 },
    { min: 40000, max: 85000, rate: 0.30 },
    { min: 85000, max: null, rate: 0.35 }
  ],
  standard_deduction: 12000
};

function calculateTax(annualIncome) {
  const grossIncome = parseFloat(annualIncome);
  if (isNaN(grossIncome) || grossIncome < 0) {
    throw new Error("Income cannot be negative");
  }
  const standardDeduction = taxConfig.standard_deduction;
  const taxableIncome = Math.max(0, grossIncome - standardDeduction);
  let totalTax = 0;
  for (const bracket of taxConfig.tax_brackets) {
    if (taxableIncome <= bracket.min) break;
    const upper = bracket.max === null ? taxableIncome : Math.min(taxableIncome, bracket.max);
    totalTax += (upper - bracket.min) * bracket.rate;
  }
  totalTax = parseFloat(totalTax.toFixed(2));
  const effectiveRate = grossIncome > 0 ? parseFloat(((totalTax / grossIncome) * 100).toFixed(2)) : 0;
  return { gross_income: grossIncome, standard_deduction: standardDeduction, taxable_income: taxableIncome, total_tax: totalTax, effective_rate: effectiveRate };
}
