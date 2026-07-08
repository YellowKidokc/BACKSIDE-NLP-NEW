import unittest

from disk_packet_loader import load_article_fixture


class DiskPacketLoaderTest(unittest.TestCase):
    def test_real_consciousness_fixture_loads(self):
        data = load_article_fixture("consciousness", "consciousness-chi-field-action")

        self.assertEqual(data["source"]["title"], "The Minimal χ-Field Action")
        self.assertIn("02", data["station_outputs"])
        self.assertIn("14", data["station_outputs"])
        self.assertEqual(data["bundle"]["bridge_packet"]["classification"]["primary_domain"], "physics")
        self.assertTrue(data["bundle"]["bridge_packet"]["media"]["has_minimum_media"])
        self.assertEqual(data["bundle"]["schema_packet"]["@type"], "ScholarlyArticle")
        self.assertIn("A1.1", data["bundle"]["schema_packet"]["pof:formalSurfaces"]["axioms"])


if __name__ == "__main__":
    unittest.main()
