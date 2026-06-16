"""
L3: THEOPHYSICS METRICS WRAPPER
================================
Pulls CHI, W/K, Fruits, Master Equation variables, CKG tier.
Wraps the existing Python Backend analytics. No duplication.
"""
import re
import sys
from pathlib import Path

BACKEND = Path(r"O:\999_IGNORE\Obsidian Programs\Python_Backend")
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(BACKEND / "analytics"))

WISDOM_TERMS = [
    'wisdom','discernment','eternal','transcend','revelation','mystery','grace',
    'covenant','truth','logos','spirit','divine','sacred','holy','virtue',
    'righteousness','soul','prayer','faith','love','hope','redemption',
    'atonement','resurrection','kingdom','covenant',
]
KNOWLEDGE_TERMS = [
    'data','evidence','experiment','measure','calculate','equation','formula',
    'theorem','proof','derive','quantum','physics','entropy','probability',
    'statistical','empirical','observation','hypothesis','analysis','sigma',
    'decoherence','wavefunction','superposition','photon','spacetime','information',
]
COHERENCE_TERMS = {
    'coherence':3,'coherent':3,'logos':3,'quantum':3,'decoherence':3,
    'wavefunction':3,'entropy':2,'conservation':2,'order':2,'structure':2,
    'framework':2,'principle':2,'truth':2,'divine':2,'atonement':2,
    'resurrection':2,'isomorphism':2,'axiom':2,'theorem':2,'measurement':2,
    'observer':2,'collapse':2,'information':2,'correction':2,'grace':2,
    'system':1.5,'wave':1.5,'law':1.5,'field':1.5,'fundamental':2,
}
FRUITS = {
    'love':['love','care','caring','sacrifice','sacrificial','agape','charity','compassion','communion','relational','covenantal'],
    'joy':['joy','delight','gladness','flourish','flourishing','rejoice','rejoicing','abundance','gratitude','celebration'],
    'peace':['peace','harmony','reconcile','reconciliation','noncontradiction','rest','shalom','stable','stability','wholeness','calm'],
    'patience':['patience','patient','wait','waiting','endure','endurance','persist','persistence','perseverance','long-suffering','longsuffering','delayed gratification'],
    'kindness':['kindness','kind','tender','tenderness','compassion','mercy','gentle','generosity','hospitality','benevolent','benevolence'],
    'goodness':['goodness','good','righteous','righteousness','integrity','upright','virtue','justice','honest','honorable','moral excellence'],
    'faithfulness':['faithfulness','faithful','loyal','loyalty','reliable','consistent','covenant','steadfast','fidelity','committed','promise'],
    'gentleness':['gentleness','gentle','meek','meekness','humble','humility','lowly','quiet','soft answer','restraint','tenderness'],
    'self_control':['self-control','self control','discipline','disciplined','restrain','restraint','temperance','sober','moderation','govern','mastery'],
    'grace':['grace','unmerited','freely','gift'],
    'hope':['hope','future','promise','expectation'],
    'humility':['humble','humility','servant','lowly'],
}
ANTI_FRUITS = {
    'love':['hatred','hate','contempt','cruelty','malice','resentment','bitterness','vengeance','dehumanize','exploitation','hostility','rivalry'],
    'joy':['despair','misery','nihilism','hopeless','hopelessness','cynicism','dread','emptiness','meaninglessness','anguish','despondent'],
    'peace':['chaos','panic','anxiety','anxious','violence','hostility','conflict','unrest','agitation','fear','turbulence','disorder','fragmentation'],
    'patience':['impatience','rash','reactionary','restless','hurry','rushed','impulsive','instant','frantic','short-term','volatility','escalation','reactive'],
    'kindness':['harsh','brutal','unkind','vindictive','cruel','contemptuous','scorn','mockery','callous','punitive','merciless','humiliation','derision'],
    'goodness':['corrupt','corruption','depraved','wicked','dishonest','exploitation','vice','injustice','perverse','immoral','fraud','predatory','abuse','evil'],
    'faithfulness':['fickle','treacherous','faithless','betray','betrayal','disloyal','abandonment','unfaithful','unreliable','broken promise','infidelity','apostasy'],
    'gentleness':['abrasive','dominating','coercive','coercive pressure','bullying','harshness','aggression','authoritarian','intimidation','threatening','domineering','controlling'],
    'self_control':['impulsive','undisciplined','unrestrained','reckless','addiction','addictive','indulgence','compulsive','appetite','craving','excess','binge','ungoverned','out of control'],
}
ME_VARS = {
    'G_gravity_belonging': ['gravity','belonging','community','gather','love','binding','together'],
    'M_mass_meaning': ['meaning','purpose','mass','nuclear','commit','covenant','hold'],
    'E_entropy_engagement': ['entropy','energy','work','engage','effort','action','decay'],
    'S_spacetime_structure': ['spacetime','structure','geometry','context','space','time'],
    'T_time_eternity': ['time','eternal','sequence','cause','before','after','duration'],
    'K_knowledge_logos': ['knowledge','logos','word','information','encode','transmit','meaning'],
    'R_relationship': ['relationship','connect','communicate','interact','bond','between'],
    'Q_quantum_observer': ['quantum','observer','measurement','collapse','wavefunction','consciousness'],
    'F_faith_coupling': ['faith','coupling','align','connect','trust','belief','voluntary'],
    'C_christ_coherence': ['christ','coherence','holds','together','all things','integration','complete'],
}

def _term_pattern(term):
    escaped = re.escape(term.lower().strip())
    escaped = escaped.replace(r'\ ', r'[\s\-_]+').replace(r'\-', r'[\s\-_]+')
    return re.compile(rf'(?<![a-z0-9]){escaped}(?![a-z0-9])')

def _count_terms(text, terms):
    return sum(len(_term_pattern(term).findall(text)) for term in terms)

def analyze(path_or_text, is_path=True):
    if is_path:
        text = Path(path_or_text).read_text(encoding='utf-8', errors='ignore')
        fname = Path(path_or_text).name
    else:
        text = path_or_text
        fname = 'inline'

    tl = text.lower()
    words = tl.split()
    wc = len(words)
    if wc == 0:
        return {'file': fname}
    norm = 1000 / wc

    # CHI Score
    cs = sum(tl.count(t) * w * norm for t, w in COHERENCE_TERMS.items())
    chi = round(min(10, max(0, cs / 10)), 2)
    chi_status = "HIGH" if chi>=8 else "STRONG" if chi>=6 else "MODERATE" if chi>=4 else "WEAK"

    # W/K Ratio
    ws_cnt = sum(tl.count(t) for t in WISDOM_TERMS)
    ks_cnt = sum(tl.count(t) for t in KNOWLEDGE_TERMS)
    wk_ratio = round(ws_cnt / max(ks_cnt, 1), 3)
    wk_status = "WISDOM-LED" if wk_ratio >= 1.5 else "BALANCED" if wk_ratio >= 1.0 else "KNOWLEDGE-DOMINANT"

    # Fruits of the Spirit (12 positive dimensions + 9 canonical anti-fruits)
    fruits = {f: _count_terms(tl, kws) for f, kws in FRUITS.items()}
    fruits_total = sum(fruits.values())
    fruits_norm = round(min(10, fruits_total * norm / 5), 2)
    dominant_fruit = max(fruits, key=fruits.get) if fruits else ''
    anti_fruits = {f: _count_terms(tl, kws) for f, kws in ANTI_FRUITS.items()}
    anti_total = sum(anti_fruits.values())
    anti_norm = round(min(10, anti_total * norm / 5), 2)
    fruit_net = round(max(0, fruits_norm - 0.65 * anti_norm), 2)
    dominant_anti_fruit = max(anti_fruits, key=anti_fruits.get) if anti_fruits else ''

    # Master Equation Variables (G,M,E,S,T,K,R,Q,F,C)
    me_scores = {}
    for var, terms in ME_VARS.items():
        score = sum(tl.count(t) for t in terms)
        me_scores[var] = round(min(10, score * norm / 3), 2)
    me_avg = round(sum(me_scores.values()) / len(me_scores), 2)
    dominant_me = max(me_scores, key=me_scores.get)

    # Cross-domain bridges
    cross_domain = len(re.findall(
        r'\b(isomorphism|maps to|maps onto|analogous|parallel|mirror|dual|correspond|bridges|connects)\b', tl
    ))

    # Scripture references
    scripture = len(re.findall(
        r'\b\d:\d+|\b(genesis|john|romans|colossians|hebrews|corinthians|matthew|revelation|psalms|isaiah|acts)\b', tl
    ))

    # CKG tier estimate (based on structure)
    axioms = len(re.findall(r'\b(axiom|law \d|principle \d|theorem|postulate)\b', tl))
    citations = len(re.findall(r'\([A-Z][a-z]+,\s*\d{4}\)|\[\d+\]|et al\.', text))
    evidence = len(re.findall(r'\b(evidence|experiment|sigma|p-value|data|measure|statistic)\b', tl))
    ckg_raw = min(100, axioms*5 + citations*3 + evidence*2 + cross_domain*4 + (chi*5))
    if ckg_raw >= 80:   ckg_tier = 'A — Publication Grade'
    elif ckg_raw >= 60: ckg_tier = 'B — Strong'
    elif ckg_raw >= 40: ckg_tier = 'C — Moderate'
    elif ckg_raw >= 20: ckg_tier = 'D — Developing'
    else:               ckg_tier = 'F — Needs Work'

    result = {
        'file': fname,
        'chi_score': chi,
        'chi_status': chi_status,
        'wisdom_score': round(ws_cnt * norm / 10, 2),
        'knowledge_score': round(ks_cnt * norm / 10, 2),
        'wk_ratio': wk_ratio,
        'wk_status': wk_status,
        'fruits_composite': fruits_norm,
        'anti_fruits_composite': anti_norm,
        'fruits_net_score': fruit_net,
        'dominant_fruit': dominant_fruit,
        'dominant_anti_fruit': dominant_anti_fruit,
        'fruits_detail': ', '.join(f"{k}:{v}" for k,v in sorted(fruits.items(), key=lambda x: -x[1])[:5]),
        'anti_fruits_detail': ', '.join(f"{k}:{v}" for k,v in sorted(anti_fruits.items(), key=lambda x: -x[1])[:5]),
        'me_avg_score': me_avg,
        'me_dominant_variable': dominant_me,
        'cross_domain_bridges': cross_domain,
        'scripture_refs': scripture,
        'ckg_raw': round(ckg_raw, 1),
        'ckg_tier': ckg_tier,
    }
    result.update({f"me_{k}": v for k, v in me_scores.items()})
    return result


if __name__ == '__main__':
    import sys, json
    if len(sys.argv) > 1:
        r = analyze(sys.argv[1])
        print(json.dumps(r, indent=2))
