import unittest

from packet_bridge import build_packet_bundle


class PacketBridgeTests(unittest.TestCase):
    def test_build_packet_bundle_from_partial_station_outputs(self):
        source = {
            "slug": "consciousness-chi-field-action",
            "series_slug": "consciousness",
            "source_path": "consciousness/consciousness-chi-field-action.html",
            "content_type": "paper",
            "title": "Chi Field Action",
            "description": "A formal page about coherence, grace, and field behavior.",
            "url": "https://faiththruphysics.com/consciousness/consciousness-chi-field-action.html",
        }
        station_outputs = {
            "02": {
                "thesis": {
                    "one_sentence": "Grace acts as an external source term for coherence recovery.",
                    "thesis_type": "mathematical",
                    "thesis_strength": 8,
                },
                "claims": [
                    {
                        "id": "C1",
                        "claim": "Grace is modeled as an external source term.",
                        "type": "mathematical",
                        "proof": "Derived from the field equation discussion.",
                        "proof_type": "argument",
                        "proof_strength": 8,
                        "depends_on": ["A3"],
                    },
                    {
                        "id": "C2",
                        "claim": "Self-repair is insufficient under decoherence.",
                        "type": "causal",
                        "proof_type": "none",
                        "proof_strength": 2,
                    },
                ],
            },
            "05": {
                "questions": [
                    {
                        "id": "Q1",
                        "question": "What prevents self-repair from restoring coherence?",
                        "value_score": 9,
                    }
                ],
                "overclaim_flags": ["C2"],
            },
            "06": {
                "primary_domain": "consciousness",
                "secondary_domains": ["physics", "theology"],
                "topic_tags": ["coherence", "grace", "field-theory"],
                "method_tags": ["formal", "deductive"],
            },
            "08": {
                "scores": {"weighted_total": 86, "pass": True},
                "variants": {
                    "title": {"canonical": "Chi Field Action"},
                    "description": {"canonical": "Formal coherence-field analysis."},
                },
                "fixes": ["Split long intro paragraph", "Tighten meta description"],
            },
            "14": {
                "master_equation_presence": "explicit",
                "axiom_ids_present": ["A3", "A8"],
                "lean_refs_present": ["theorem_21"],
                "claim_alignment": [
                    {
                        "claim_id": "C1",
                        "formal_support_type": "equation",
                        "support_ref": "EQ-014",
                        "alignment_strength": 9,
                    }
                ],
            },
            "16": {
                "background_ok": True,
                "white_page_risk": "green",
                "player_present": True,
            },
        }

        bundle = build_packet_bundle(source, station_outputs)

        self.assertEqual(bundle["bridge_packet"]["slug"], "consciousness-chi-field-action")
        self.assertEqual(bundle["bridge_packet"]["thesis"]["one_sentence"], "Grace acts as an external source term for coherence recovery.")
        self.assertEqual(bundle["bridge_packet"]["formal_surfaces"]["master_equation"], "explicit")
        self.assertEqual(bundle["bridge_packet"]["claims"][0]["formal_support_ref"], "EQ-014")
        self.assertEqual(bundle["integrity_packet"]["structural_verdict"]["publish_recommendation"], "fix_first")
        self.assertEqual(bundle["schema_packet"]["@type"], "ScholarlyArticle")
        self.assertIn("pof:formalSurfaces", bundle["schema_packet"])


if __name__ == "__main__":
    unittest.main()
