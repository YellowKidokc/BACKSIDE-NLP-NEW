import os
import shutil
import re

source_dir = 'DMP_Unsorted'
target_base = '.'

# Mapping of keywords/patterns to folders
mapping = {
    'GTQ': ['genesis.to.quantum', 'gtq', 'measurement.collapsed', 'quantum.state', r'^q\d-', 'judging.layer', 'convergence.0', '7q'],
    'TP': ['theophysics.overview', 'what.is.theophysics', 'theophysics.intro', 'unavoidable.conclusion', 'traceability.matrix', 'nonlinear.dynamics', 'control.theory', 'network.theory', 'computational.complexity'],
    'MDA': ['moral.decline', 'cliodynamic', 'church.decline', r'^19\d{2}', r'^20\d{2}', 'social.pathology', 'amish', 'rothschild', '911', 'polarization', 'disunion'],
    'AOD': ['architecture.of.debt', 'finance.deep.mapping', 'debt.1', 'monetary'],
    'MEQ': ['master.equation', 'unified.blueprint', 'e2.1', 'e19.1', 'chi.field', 'translation.layer', 'unifiers.and.standard', 'master.assembly'],
    'AXM': ['axiom', r'^[ad]\d+\.\d+', 'existence.4', 'court.room', 'biaxiosum', 'first.principles', r'^a-\d{3}.role'],
    'LAW': ['ten.laws', 'law.1', 'law.2', 'law.3', 'law.4', 'law-5', 'law.6', 'law.7', 'law.8', 'law.9', 'law.10', 'lw-', 'pm_'],
    'LGS': ['logos.field', 'logos.principle', 'lgs-', r'^p\d{2}-', r'^paper-', 'logos.lab'],
    'SAL': ['salvation', 'grace.function', 'redemption', 'grace.operator'],
    'JAS': ['jesus.as.light', 'trinity.physics', 'i.am.statement', 'christ'],
    'MAT': ['materialism.rebuttals', 'materialism', 'eliminative'],
    'WVW': ['worldview', 'aristotelianism', 'calvinism', 'absurdism', 'nihilism', 'humanism', 'panentheism', 'pantheism', 'stoicism', 'kantian', 'thomism'],
    'PHY': ['quantum.mechanics', 'wave.particle', 'entanglement', 'bell.theorem', 'copenhagen', 'relativity', 'einstein', 'maxwell', 'feynman', 'schrodinger', 'lagrangian', 'newton'],
    'COH': ['coherence.entropy', 'entropy.dynamics', 'phase.transition', 'coherence.gauge'],
    'THO': ['theology.general', 'prayer', 'faith', 'sin', 'holy.spirit', 'eternal.security', 'resurrection', 'eternal_security', 'david.effect'],
    'CON': ['consciousness', 'qualia', 'soul.observer', 'integrated.information', 'panpsychism', 'hard.problem', 'chalmers', 'active.inference'],
    'FPR': ['formal.papers', 'academic.papers', r'^fp-', r'^\d{4}\.\d{4}'],
    'BIB': ['biblical.studies', 'scripture.analysis', 'prophecy', 'tanakh', 'quran', 'gita', 'kjv', 'dhammapada', 'upanishads'],
    'HIS': ['historical.timeline', 'civilization.analysis', 'american.history', 'us.constitution', 'bill.of.rights', 'declaration.of.independence', 'articles.of.confederation'],
    'DUA': ['duality.project', 'alpha.prime', 'omega.null'],
    'CHT': ['charts.dashboards', 'analytics', 'visualizations', 'dashboard', r'^ft-\d+'],
    'TPL': ['templates', 'system.prompts', 'workflow.pages', 'prompt', 'opus.page.builder', '404.html', 'wordmark'],
    'APO': ['apologetics', 'arguments.for.god', 'rebuttals', r'^_CF\d+'],
    'WAR': ['spiritual.warfare', 'adversary.physics', 'attack-surface', 'mkultra', 'conspiracy'],
    'GLO': ['glossary', 'term.definitions', 'merged.glossary'],
    'ISO': ['isomorphism', r'^iso-\d+'],
    'IMG': [r'\.webp$', r'\.png$', r'\.jpg$', r'\.jpeg$']
}

# Reverse mapping for folder lookup
folder_map = {
    'GTQ': 'GTQ_Genesis-to-Quantum',
    'TP': 'TP_Theophysics-Overview',
    'MDA': 'MDA_Moral-Decline-of-America',
    'AOD': 'AOD_Architecture-of-Debt',
    'MEQ': 'MEQ_Master-Equation',
    'AXM': 'AXM_Axioms-Framework',
    'LAW': 'LAW_Ten-Laws',
    'LGS': 'LGS_Logos',
    'SAL': 'SAL_Salvation-Grace',
    'JAS': 'JAS_Jesus-Light-Trinity',
    'MAT': 'MAT_Materialism-Rebuttals',
    'WVW': 'WVW_Worldview-Comparisons',
    'PHY': 'PHY_Physics-Quantum',
    'COH': 'COH_Coherence-Entropy',
    'THO': 'THO_Theology-General',
    'CON': 'CON_Consciousness-Mind',
    'FPR': 'FPR_Formal-Papers',
    'BIB': 'BIB_Biblical-Studies',
    'HIS': 'HIS_Historical-Timeline',
    'DUA': 'DUA_Duality-Project',
    'CHT': 'CHT_Charts-Dashboards',
    'TPL': 'TPL_Templates-System',
    'APO': 'APO_Apologetics-Debate',
    'WAR': 'WAR_Spiritual-Warfare',
    'GLO': 'GLO_Glossary-Gallery',
    'ISO': 'ISO_Isomorphism-Registry',
    'IMG': 'IMG_Images'
}

moved_count = 0
for filename in os.listdir(source_dir):
    filepath = os.path.join(source_dir, filename)
    if os.path.isdir(filepath):
        continue
    
    for code, patterns in mapping.items():
        found = False
        for pattern in patterns:
            # Replacing dot with a regex that matches dash or underscore or space
            p = pattern.replace('.', '[_ \-]')
            if re.search(p, filename, re.IGNORECASE):
                target_dir = os.path.join(folder_map[code], '_drafts')
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                try:
                    shutil.move(filepath, os.path.join(target_dir, filename))
                    moved_count += 1
                except Exception as e:
                    pass
                found = True
                break
        if found:
            break

print(f"Successfully moved {moved_count} files in the flexible separator pass.")
