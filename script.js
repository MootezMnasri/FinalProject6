document.getElementById("taxForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const income = document.getElementById("income").value;
  const errorMsg = document.getElementById("errorMsg");
  const resultSection = document.getElementById("resultSection");
  const resultContent = document.getElementById("resultContent");
  errorMsg.style.display = "none";
  resultSection.style.display = "none";
  try {
    const result = calculateTax(income);
    resultContent.innerHTML =
      "<p><strong>Gross Income:</strong> $" + result.gross_income.toLocaleString() + "</p>" +
      "<p><strong>Standard Deduction:</strong> -$" + result.standard_deduction.toLocaleString() + "</p>" +
      "<p><strong>Taxable Income:</strong> $" + result.taxable_income.toLocaleString() + "</p>" +
      "<p><strong>Total Tax:</strong> $" + result.total_tax.toLocaleString() + "</p>" +
      "<p><strong>Effective Rate:</strong> " + result.effective_rate + "%</p>";
    resultSection.style.display = "block";
  } catch (err) {
    errorMsg.textContent = err.message;
    errorMsg.style.display = "block";
  }
});
