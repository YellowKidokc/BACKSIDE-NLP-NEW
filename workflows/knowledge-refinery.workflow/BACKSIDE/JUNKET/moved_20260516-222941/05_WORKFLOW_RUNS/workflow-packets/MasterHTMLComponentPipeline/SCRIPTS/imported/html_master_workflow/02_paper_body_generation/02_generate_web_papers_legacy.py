import os
import re

# Paths
template_path = r'C:\Users\lowes\Desktop\Kimi Web Design\theophysics-paper-template.html'
papers_dir = r'C:\Users\lowes\Desktop\Theophysics_Papers_April_2026'
output_dir = r'C:\Users\lowes\Desktop\Theophysics_Web_Pages_April_2026'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read template
with open(template_path, 'r', encoding='utf-8') as f:
    template_content = f.read()

def parse_markdown(content):
    # Extract Title
    title_match = re.search(r'# (.*)\n## (.*)', content)
    main_title = title_match.group(1) if title_match else "Theophysics Paper"
    sub_title = title_match.group(2) if title_match else ""
    
    # Extract Abstract
    abstract_match = re.search(r'\*\*Abstract:\*\* (.*?)\n\n', content, re.DOTALL)
    abstract = abstract_match.group(1) if abstract_match else ""
    
    # Extract Sections
    sections = re.findall(r'### (\d+\..*?)\n(.*?)(?=\n### |\n---|\Z)', content, re.DOTALL)
    
    return main_title, sub_title, abstract, sections

def markdown_to_html(text):
    # Basic conversion for bold, italic, and lists
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # Convert lists
    text = re.sub(r'^\* (.*)', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*</li>)', r'<ul class="list-disc ml-6 space-y-2 text-[#a0a0a0] mb-4">\1</ul>', text, flags=re.DOTALL)
    # Fix nested lists if any (very basic)
    # Paragraphs
    paragraphs = text.split('\n\n')
    text = ''.join([f'<p class="text-[#a0a0a0] mb-4 leading-relaxed">{p.strip()}</p>' for p in paragraphs if p.strip()])
    return text

# Get all papers
paper_files = [f for f in os.listdir(papers_dir) if f.endswith('.md')]
paper_files.sort()

for filename in paper_files:
    with open(os.path.join(papers_dir, filename), 'r', encoding='utf-8') as f:
        content = f.read()
    
    main_title, sub_title, abstract, sections = parse_markdown(content)
    
    full_title = f"{main_title}: {sub_title}"
    
    # Process sections
    html_sections = ""
    for sec_title, sec_body in sections:
        html_sections += f'<h2 class="serif text-3xl font-bold text-white mb-6 mt-12">{sec_title}</h2>\n'
        html_sections += markdown_to_html(sec_body)
    
    # Update template
    page = template_content
    page = page.replace('[PAPER TITLE]', full_title)
    page = page.replace('[One-sentence summary of the paper\'s core claim or finding.]', abstract[:150] + "...")
    page = page.replace('[Full abstract goes here. 150-250 words describing the problem, method, and key findings.]', abstract)
    
    # Replace the Full Paper section
    paper_placeholder = re.search(r'<article class="max-w-4xl">.*?</article>', page, re.DOTALL)
    if paper_placeholder:
        new_article = f'''<article class="max-w-4xl">
                <h2 class="serif text-3xl font-bold text-white mb-6">Abstract</h2>
                <p class="text-[#e0e0e0] mb-8 leading-relaxed text-lg">
                    {abstract}
                </p>
                {html_sections}
            </article>'''
        page = page.replace(paper_placeholder.group(0), new_article)
    
    # Update Executive Summary Tab
    summary_placeholder = page.find('<section id="summary" class="tab-content">')
    if summary_placeholder != -1:
        # Very simple summary for now
        summary_text = abstract
        page = page.replace('[One paragraph maximum. The absolute core claim. If they read nothing else, they get this.]', summary_text)
    
    # Set date
    page = page.replace('YYYY-MM-DD', '2026-04-11')
    
    # Set Thesis Unit
    paper_num = filename.split('_')[1]
    page = page.replace('DT-XXX', f'DT-{paper_num}')
    
    output_filename = filename.replace('.md', '.html')
    with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as f:
        f.write(page)
    print(f"Generated {output_filename}")

print("Done.")
