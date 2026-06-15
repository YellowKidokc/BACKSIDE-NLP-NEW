"""One-shot o3 call: Analogy → Isomorphism → Maxwell boundary question."""
import os, json
from pathlib import Path
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

PROMPT = """I'm building a framework called Theophysics that maps theology to physics — not as metaphor, but claiming shared mathematical structure.

I need you to give me an extremely precise, rigorous answer to this question:

What is the EXACT boundary between:

1. ANALOGY — 'these two things are similar'
2. STRUCTURAL ANALOGY — 'these two things share a pattern'
3. ISOMORPHISM — 'these two things have the same mathematical structure'
4. PHYSICAL LAW — 'this IS the physics' (Maxwell level)

For each transition (1→2, 2→3, 3→4), tell me:

(a) What SPECIFIC thing must be true that wasn't true at the previous level?
(b) Give me a concrete historical example of something that crossed that boundary (e.g., something that started as analogy and became law)
(c) What is the MINIMUM evidence required to claim you've crossed?
(d) What is the common mistake people make — claiming they've crossed when they haven't?

Then answer the critical question for MY work:

If I have a 12-stage mapping between BEC phase transitions and Christian soteriology where the ordering matches — what SPECIFICALLY would I need to show to cross from 'structural analogy' (level 2) to 'isomorphism' (level 3)?

Be precise. I don't want philosophy — I want the mathematician's answer. What operations must be preserved? What must the morphism look like? What would a category theorist demand?

And then: what would it take to get from isomorphism (level 3) to 'this is actual physics' (level 4)? Is that even possible for theology? If not, what is the ceiling and why?

Finally: are there examples in the history of physics where a mapping between two seemingly unrelated domains turned out to be MORE than analogy? (I'm thinking of things like the AdS/CFT correspondence, gauge/gravity duality, the Langlands program, etc.) What made those crossings work, and what can I learn from them?"""

response = client.chat.completions.create(
    model='o3',
    messages=[
        {'role': 'developer', 'content': 'You are a mathematical physicist and philosopher of science with deep expertise in category theory, mathematical physics, and formal epistemology. Give precise, technical answers. Use real mathematics. Name real theorems and real historical examples.'},
        {'role': 'user', 'content': PROMPT}
    ],
    max_completion_tokens=16000,
)

text = response.choices[0].message.content
usage = response.usage
input_t = usage.prompt_tokens if usage else 0
output_t = usage.completion_tokens if usage else 0
total_t = usage.total_tokens if usage else 0
cost = (input_t * 10.0 + output_t * 40.0) / 1_000_000

print(f"Tokens: {total_t:,} (in={input_t:,}, out={output_t:,})")
print(f"Cost: ${cost:.4f}")
print("=" * 60)
# Print safely (avoid encoding errors on Windows console)
try:
    print(text)
except UnicodeEncodeError:
    print(text.encode('ascii', 'replace').decode('ascii'))

# Save
out_dir = Path("T:/THEOPHYSICS_PAPER_INTELLIGENCE/OUTPUT/SALVATION_INTEL")
out_dir.mkdir(parents=True, exist_ok=True)

result = {
    'text': text,
    'tokens': total_t,
    'cost': cost,
    'model': 'o3',
    'timestamp': datetime.now().isoformat()
}
(out_dir / 'ANALOGY_TO_MAXWELL_o3.json').write_text(
    json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')

header = f"# Analogy to Isomorphism to Maxwell: Where Are the Lines?\n"
header += f"*Model: o3 | {total_t:,} tokens | ${cost:.4f} | {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n---\n\n"
(out_dir / 'ANALOGY_TO_MAXWELL_o3.md').write_text(header + text, encoding='utf-8')
print(f"\nSaved to: {out_dir / 'ANALOGY_TO_MAXWELL_o3.md'}")
