import httpx

text = """On the Electrodynamics of Moving Bodies - Albert Einstein, 1905

It is known that Maxwell's electrodynamics, as usually understood at the present time, when applied to moving bodies, leads to asymmetries which do not appear to be inherent in the phenomena. Take, for example, the reciprocal electrodynamic action of a magnet and a conductor. The observable phenomenon here depends only on the relative motion of the conductor and the magnet, whereas the customary view draws a sharp distinction between the two cases in which either the one or the other of these bodies is in motion.

The theory is based on two postulates: (1) The Principle of Relativity - the laws of physics are invariant in all inertial frames of reference. (2) The speed of light in a vacuum is the same for all observers regardless of the motion of the light source or observer.

These two postulates suffice for the attainment of a simple and consistent theory of the electrodynamics of moving bodies based on Maxwell's theory for stationary bodies. The introduction of a luminiferous ether will prove to be superfluous.

The theory leads to the following experimentally verified conclusions: Time dilation - moving clocks run slower. Length contraction - moving objects contract along the direction of motion. Mass-energy equivalence E=mc^2 - mass and energy are interconvertible. Relativity of simultaneity - events simultaneous in one frame are not necessarily simultaneous in another.

Experimental evidence: Michelson-Morley experiment (1887) showed no luminiferous ether. Time dilation confirmed by Hafele-Keating experiment (1971) using atomic clocks on aircraft. GPS satellites require relativistic corrections of 38 microseconds per day. Particle accelerators routinely observe relativistic mass increase. Gravitational lensing observations confirm spacetime curvature predictions.

The theory has been tested to extraordinary precision. No violations of special relativity have ever been observed in over a century of experiments across every domain of physics.

Kill conditions that would falsify special relativity: (1) Detection of a preferred reference frame. (2) Observation of superluminal information transfer. (3) Violation of Lorentz invariance at any energy scale. (4) Failure of E=mc^2 in nuclear reactions. None have been observed.

Limitations: Special relativity does not account for gravity. This limitation was addressed by general relativity (1915). The theory is incompatible with quantum mechanics at the Planck scale, which remains an open problem."""

print("Ingesting Einstein's Special Relativity...")
with httpx.Client(timeout=60) as client:
    resp = client.post("http://127.0.0.1:8000/papers/paste", data={
        "title": "On the Electrodynamics of Moving Bodies (Special Relativity)",
        "authors": "Albert Einstein",
        "year": "1905",
        "text": text,
    }, follow_redirects=False)
    
    papers = client.get("http://127.0.0.1:8000/papers").json()
    paper_id = papers[0]['id']
    print(f"Paper ID: {paper_id}")

print(f"Running o3 pipeline...")
with httpx.Client(timeout=600) as client:
    resp = client.post(f"http://127.0.0.1:8000/papers/{paper_id}/run-all")
    print(f"Status: {resp.status_code}")
    print(f"Result: {resp.text[:500]}")
    
print(f"\nView: http://127.0.0.1:8000/papers/{paper_id}/view")
print(f"Snapshot: http://127.0.0.1:8000/papers/{paper_id}/snapshot")