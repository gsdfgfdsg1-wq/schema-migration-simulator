import unittest
from simulate import analyze


class SimulatorTests(unittest.TestCase):
    def test_flags_drop_as_irreversible(self):
        report = analyze("ALTER TABLE users DROP COLUMN legacy")
        self.assertEqual(report["risks"][0]["kind"], "irreversible-ddl")

    def test_estimates_large_backfill(self):
        report = analyze("UPDATE events SET state='x'", {"events": 2_000_000})
        self.assertEqual(report["estimates"][0]["estimated_seconds"], 40.0)
        self.assertIn("large-backfill", [risk["kind"] for risk in report["risks"]])

    def test_small_addition_has_no_high_risk(self):
        report = analyze("ALTER TABLE users ADD COLUMN name text", {"users": 10})
        self.assertTrue(report["safe"])
        self.assertIn("table-lock-risk", [risk["kind"] for risk in report["risks"]])


if __name__ == "__main__":
    unittest.main()
