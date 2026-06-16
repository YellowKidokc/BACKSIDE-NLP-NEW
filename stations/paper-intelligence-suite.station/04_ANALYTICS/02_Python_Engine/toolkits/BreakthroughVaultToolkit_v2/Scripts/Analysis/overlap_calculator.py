# overlap_calculator.py
"""
Calculate semantic overlap between traditional and Theophysics definitions.
"""

def calculate_overlap(traditional_props, theophysics_props):
    """
    Compare two sets of defining properties.
    
    Args:
        traditional_props: List of properties from traditional definition
        theophysics_props: List of properties from Theophysics definition
    
    Returns:
        Dictionary with overlap analysis
    """
    traditional_set = set(prop.lower().strip() for prop in traditional_props)
    theophysics_set = set(prop.lower().strip() for prop in theophysics_props)
    
    shared = traditional_set & theophysics_set
    unique_traditional = traditional_set - theophysics_set
    unique_theophysics = theophysics_set - traditional_set
    total = traditional_set | theophysics_set
    
    if len(total) == 0:
        return {
            'overlap_percent': 0,
            'shared_properties': [],
            'unique_traditional': [],
            'unique_theophysics': []
        }
    
    overlap_percent = (len(shared) / len(total)) * 100
    
    return {
        'overlap_percent': round(overlap_percent, 1),
        'shared_properties': sorted(list(shared)),
        'unique_traditional': sorted(list(unique_traditional)),
        'unique_theophysics': sorted(list(unique_theophysics)),
        'total_properties': len(total),
        'shared_count': len(shared)
    }


if __name__ == "__main__":
    # Example: Coherence
    print("="*60)
    print("SEMANTIC OVERLAP ANALYSIS: COHERENCE")
    print("="*60)
    print()
    
    physics_coherence = [
        'phase relationship', 'wave interference', 'quantum correlation',
        'temporal stability', 'spatial correlation', 'predictability',
        'order', 'synchronization', 'resonance', 'entanglement'
    ]
    
    theophysics_coherence = [
        'phase relationship', 'order', 'resonance',  # Shared with physics
        'logos alignment', 'spiritual unity', 'divine intention',
        'moral consistency', 'redemptive pattern', 'grace flow',
        'consciousness integration'
    ]
    
    result = calculate_overlap(physics_coherence, theophysics_coherence)
    
    print(f"Overlap: {result['overlap_percent']}%")
    print(f"Total Properties Analyzed: {result['total_properties']}")
    print(f"Shared Properties ({result['shared_count']}):")
    for prop in result['shared_properties']:
        print(f"  ✓ {prop}")
    print()
    print(f"Unique to Physics ({len(result['unique_traditional'])}):")
    for prop in result['unique_traditional']:
        print(f"  • {prop}")
    print()
    print(f"Unique to Theophysics ({len(result['unique_theophysics'])}):")
    for prop in result['unique_theophysics']:
        print(f"  • {prop}")
    print()
    
    # Verdict
    if result['overlap_percent'] < 30:
        tier = "TIER 1: COLLISION (Critical - New Definition Required)"
    elif result['overlap_percent'] < 60:
        tier = "TIER 2: BRIDGE (Clarification Needed)"
    else:
        tier = "TIER 3: LOW COLLISION (Traditional Def May Work)"
    
    print(f"Classification: {tier}")
    print()
