import json
import unittest
from pathlib import Path

from main import calculate_cost_savings, calculate_operating_costs


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CostCalculationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(PROJECT_ROOT / "config.json", encoding="utf-8") as file:
            cls.config = json.load(file)

    def test_total_cost_is_sum_of_components(self):
        costs = calculate_operating_costs(29.7173, 4040, "diesel", self.config)
        expected_total = (
            costs["energy_cost_gbp"]
            + costs["labour_cost_gbp"]
            + costs["fixed_vehicle_cost_gbp"]
            + costs["waste_treatment_cost_gbp"]
        )
        self.assertAlmostEqual(costs["total_cost_gbp"], expected_total)

    def test_shorter_route_reduces_variable_costs(self):
        baseline = {
            vehicle: calculate_operating_costs(29.7173, 4040, vehicle, self.config)
            for vehicle in ("diesel", "electric")
        }
        optimal = {
            vehicle: calculate_operating_costs(27.3315, 4040, vehicle, self.config)
            for vehicle in ("diesel", "electric")
        }
        savings = calculate_cost_savings(baseline, optimal)

        self.assertGreater(savings["diesel"]["amount_gbp"], 0)
        self.assertGreater(savings["electric"]["amount_gbp"], 0)
        self.assertAlmostEqual(
            baseline["diesel"]["waste_treatment_cost_gbp"],
            optimal["diesel"]["waste_treatment_cost_gbp"]
        )

    def test_zero_baseline_cost_has_safe_percentage(self):
        baseline = {"diesel": {"total_cost_gbp": 0.0}}
        optimal = {"diesel": {"total_cost_gbp": 0.0}}
        savings = calculate_cost_savings(baseline, optimal)
        self.assertEqual(savings["diesel"]["percentage"], 0.0)


if __name__ == "__main__":
    unittest.main()
