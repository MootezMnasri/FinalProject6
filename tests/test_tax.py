"""
Unit tests for the Tax Calculator module.
"""

import json
import os
import pytest
from tax_calculator.tax import calculate_tax, load_tax_config


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def sample_config():
    """Return a known tax configuration for deterministic tests."""
    return {
        "tax_brackets": [
            {"min": 0, "max": 10000, "rate": 0.10},
            {"min": 10000, "max": 40000, "rate": 0.20},
            {"min": 40000, "max": 85000, "rate": 0.30},
            {"min": 85000, "max": None, "rate": 0.35},
        ],
        "standard_deduction": 12000,
    }


# ──────────────────────────────────────────────
# Configuration loading tests
# ──────────────────────────────────────────────

class TestLoadConfig:
    def test_load_default_config(self):
        """Default config.json should load without errors."""
        config = load_tax_config()
        assert "tax_brackets" in config
        assert "standard_deduction" in config

    def test_config_has_brackets(self):
        config = load_tax_config()
        assert len(config["tax_brackets"]) > 0

    def test_config_brackets_have_required_keys(self):
        config = load_tax_config()
        for bracket in config["tax_brackets"]:
            assert "min" in bracket
            assert "max" in bracket
            assert "rate" in bracket


# ──────────────────────────────────────────────
# Tax calculation tests
# ──────────────────────────────────────────────

class TestCalculateTax:

    def test_zero_income(self, sample_config):
        result = calculate_tax(0, config=sample_config)
        assert result["total_tax"] == 0.0
        assert result["taxable_income"] == 0.0
        assert result["effective_rate"] == 0.0

    def test_income_below_deduction(self, sample_config):
        """Income less than standard deduction → zero tax."""
        result = calculate_tax(10000, config=sample_config)
        assert result["taxable_income"] == 0.0
        assert result["total_tax"] == 0.0

    def test_income_equal_to_deduction(self, sample_config):
        result = calculate_tax(12000, config=sample_config)
        assert result["taxable_income"] == 0.0
        assert result["total_tax"] == 0.0

    def test_first_bracket_only(self, sample_config):
        """Income 20000 → taxable 8000, all in 10% bracket → tax 800."""
        result = calculate_tax(20000, config=sample_config)
        assert result["taxable_income"] == 8000.0
        assert result["total_tax"] == 800.0

    def test_two_brackets(self, sample_config):
        """Income 30000 → taxable 18000.
        First 10k @ 10% = 1000, next 8k @ 20% = 1600 → total 2600.
        """
        result = calculate_tax(30000, config=sample_config)
        assert result["taxable_income"] == 18000.0
        assert result["total_tax"] == 2600.0

    def test_three_brackets(self, sample_config):
        """Income 62000 → taxable 50000.
        10k @ 10% = 1000, 30k @ 20% = 6000, 10k @ 30% = 3000 → 10000.
        """
        result = calculate_tax(62000, config=sample_config)
        assert result["taxable_income"] == 50000.0
        assert result["total_tax"] == 10000.0

    def test_all_four_brackets(self, sample_config):
        """Income 112000 → taxable 100000.
        10k@10%=1000, 30k@20%=6000, 45k@30%=13500, 15k@35%=5250 → 25750.
        """
        result = calculate_tax(112000, config=sample_config)
        assert result["taxable_income"] == 100000.0
        assert result["total_tax"] == 25750.0

    def test_effective_rate(self, sample_config):
        result = calculate_tax(112000, config=sample_config)
        expected_rate = round((25750.0 / 112000.0) * 100, 2)
        assert result["effective_rate"] == expected_rate

    def test_result_keys(self, sample_config):
        result = calculate_tax(50000, config=sample_config)
        expected_keys = {
            "gross_income",
            "standard_deduction",
            "taxable_income",
            "tax_brackets_applied",
            "total_tax",
            "effective_rate",
        }
        assert set(result.keys()) == expected_keys

    def test_negative_income_raises(self, sample_config):
        with pytest.raises(ValueError, match="negative"):
            calculate_tax(-5000, config=sample_config)

    def test_large_income(self, sample_config):
        """Smoke test with a very large income."""
        result = calculate_tax(1_000_000, config=sample_config)
        assert result["total_tax"] > 0
        assert result["effective_rate"] > 0


# ──────────────────────────────────────────────
# Flask app endpoint tests
# ──────────────────────────────────────────────

class TestFlaskApp:

    @pytest.fixture
    def client(self):
        from app import app
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_index_get(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_health_endpoint(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "healthy"

    def test_calculate_valid(self, client):
        resp = client.post("/calculate", data={"income": "75000"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert "total_tax" in data
        assert data["total_tax"] > 0

    def test_calculate_zero(self, client):
        resp = client.post("/calculate", data={"income": "0"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total_tax"] == 0.0

    def test_calculate_missing_income(self, client):
        resp = client.post("/calculate", data={})
        assert resp.status_code == 400

    def test_calculate_negative(self, client):
        resp = client.post("/calculate", data={"income": "-100"})
        assert resp.status_code == 400
