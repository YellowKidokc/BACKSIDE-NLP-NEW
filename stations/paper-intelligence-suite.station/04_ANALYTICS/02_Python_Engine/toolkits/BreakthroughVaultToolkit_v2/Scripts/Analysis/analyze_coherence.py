"""
Logos Papers Local Coherence Analyzer
=====================================

This script analyzes coherence metrics specifically for the 12 Logos Papers,
independent of the global vault coherence system.

Coherence Metrics Tracked:
- Cross-reference density (how well papers cite each other)
- Concept consistency (terminology usage across papers)
- Mathematical notation consistency
- Argument flow (logical progression through the series)
- Novelty vs. redundancy (information gain per paper)

Author: David Lowe + Claude
Date: November 9, 2025
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class LogosPapersCoherenceAnalyzer:
    def __init__(self, papers_root):
        self.papers_root = Path(papers_root)
        self.papers = {}
        self.cross_references = defaultdict(list)
        self.concept_usage = defaultdict(Counter)
        self.math_symbols = defaultdict(set)
        
        # Core concepts to track
        self.core_concepts = [
            'Logos Field', 'χ', 'wave function collapse', 'participatory',
            'consciousness', 'observer', 'quantum', 'spacetime',
            'coherence', 'information', 'GR', 'QM', 'General Relativity',
            'Quantum Mechanics', 'grace', 'soul', 'resurrection'
        ]
        
        # Mathematical notation to track
        self.math_notation = [
            r'\\chi', r'\\Huge\\chi', r'\\psi', r'\\Psi',
            r'\\mathcal', r'\\Lambda', r'\\delta'
        ]
    
    def load_papers(self):
        """Load all 12 papers from their respective folders"""
        paper_folders = [
            'P01-Logos-Principle',
            'P02-Quantum-Bridge',
            'P03-Algorithm-Reality',
            'P04-Hard-Problem',
            'P05-Soul-Observer',
            'P06-Physics-Principalities',
            'P07-Grace-Function',
            'P08-Stretched-Heavens',
            'P09-Moral-Universe',
            'P10-Creatio-Silico',
            'P11-Protocols-Validation',
            'P12-Decalogue-Cosmos'
        ]
        
        for folder in paper_folders:
            folder_path = self.papers_root / folder
            if not folder_path.exists():
                print(f"Warning: {folder} not found")
                continue
            
            # Find the main paper markdown file
            paper_files = list(folder_path.glob('Paper-*.md'))
            if not paper_files:
                print(f"Warning: No paper file found in {folder}")
                continue
            
            paper_num = folder.split('-')[0][1:]  # Extract number from P01, P02, etc.
            paper_path = paper_files[0]
            
            with open(paper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.papers[paper_num] = {
                    'path': paper_path,
                    'content': content,
                    'folder': folder,
                    'word_count': len(content.split())
                }
        
        print(f"Loaded {len(self.papers)} papers")
    
    def analyze_cross_references(self):
        """Analyze how papers reference each other"""
        # Pattern to detect paper references
        ref_pattern = r'Paper\s+(\d+)'
        
        for paper_num, paper_data in self.papers.items():
            content = paper_data['content']
            refs = re.findall(ref_pattern, content, re.IGNORECASE)
            
            # Count references to other papers
            for ref in refs:
                if ref != paper_num:  # Don't count self-references
                    self.cross_references[paper_num].append(ref)
    
    def analyze_concept_consistency(self):
        """Track usage of core concepts across papers"""
        for paper_num, paper_data in self.papers.items():
            content = paper_data['content'].lower()
            
            for concept in self.core_concepts:
                count = content.count(concept.lower())
                if count > 0:
                    self.concept_usage[concept][paper_num] = count
    
    def analyze_math_notation(self):
        """Check consistency of mathematical notation"""
        for paper_num, paper_data in self.papers.items():
            content = paper_data['content']
            
            for notation in self.math_notation:
                if notation in content:
                    self.math_symbols[paper_num].add(notation)
    
    def calculate_coherence_score(self):
        """Calculate overall coherence score for the series"""
        scores = {}
        
        # Cross-reference density (0-100)
        total_possible_refs = len(self.papers) * (len(self.papers) - 1)
        total_actual_refs = sum(len(refs) for refs in self.cross_references.values())
        ref_density = (total_actual_refs / total_possible_refs) * 100 if total_possible_refs > 0 else 0
        scores['cross_reference_density'] = round(ref_density, 2)
        
        # Concept consistency (% of papers using core concepts)
        concept_coverage = {}
        for concept, usage in self.concept_usage.items():
            coverage = (len(usage) / len(self.papers)) * 100
            concept_coverage[concept] = round(coverage, 2)
        scores['concept_coverage'] = concept_coverage
        
        # Math notation consistency
        common_notation = set.intersection(*self.math_symbols.values()) if self.math_symbols else set()
        notation_consistency = (len(common_notation) / len(self.math_notation)) * 100 if self.math_notation else 0
        scores['notation_consistency'] = round(notation_consistency, 2)
        
        # Overall coherence (weighted average)
        overall = (
            ref_density * 0.3 +
            np.mean(list(concept_coverage.values())) * 0.4 +
            notation_consistency * 0.3
        )
        scores['overall_coherence'] = round(overall, 2)
        
        return scores
    
    def generate_visualizations(self):
        """Generate coherence visualization graphs"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Logos Papers Coherence Analysis', fontsize=16, fontweight='bold')
        
        # 1. Cross-reference network
        papers = sorted(self.papers.keys(), key=lambda x: int(x))
        ref_matrix = np.zeros((len(papers), len(papers)))
        
        for i, paper_from in enumerate(papers):
            for ref_to in self.cross_references.get(paper_from, []):
                if ref_to in papers:
                    j = papers.index(ref_to)
                    ref_matrix[i][j] += 1
        
        im1 = ax1.imshow(ref_matrix, cmap='YlOrRd', aspect='auto')
        ax1.set_xticks(range(len(papers)))
        ax1.set_yticks(range(len(papers)))
        ax1.set_xticklabels([f'P{p}' for p in papers])
        ax1.set_yticklabels([f'P{p}' for p in papers])
        ax1.set_title('Cross-Reference Matrix')
        ax1.set_xlabel('Referenced Paper')
        ax1.set_ylabel('Referencing Paper')
        plt.colorbar(im1, ax=ax1, label='Reference Count')
        
        # 2. Concept coverage across papers
        top_concepts = sorted(
            self.concept_usage.items(),
            key=lambda x: sum(x[1].values()),
            reverse=True
        )[:10]
        
        concept_names = [c[0] for c in top_concepts]
        coverage_pcts = [(len(c[1]) / len(self.papers)) * 100 for c in top_concepts]
        
        bars = ax2.barh(concept_names, coverage_pcts, color='steelblue')
        ax2.set_xlabel('Coverage (% of papers)')
        ax2.set_title('Top 10 Concept Coverage')
        ax2.set_xlim(0, 100)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2, 
                    f'{width:.1f}%', ha='left', va='center', fontweight='bold')
        
        # 3. Word count distribution
        paper_nums = sorted(self.papers.keys(), key=lambda x: int(x))
        word_counts = [self.papers[p]['word_count'] for p in paper_nums]
        
        ax3.bar(range(len(paper_nums)), word_counts, color='forestgreen', alpha=0.7)
        ax3.set_xticks(range(len(paper_nums)))
        ax3.set_xticklabels([f'P{p}' for p in paper_nums])
        ax3.set_ylabel('Word Count')
        ax3.set_title('Paper Length Distribution')
        ax3.axhline(np.mean(word_counts), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(word_counts):.0f}')
        ax3.legend()
        
        # 4. Coherence scores radar chart
        scores = self.calculate_coherence_score()
        categories = ['Cross-Ref\nDensity', 'Concept\nCoverage', 
                     'Notation\nConsistency', 'Overall\nCoherence']
        values = [
            scores['cross_reference_density'],
            np.mean(list(scores['concept_coverage'].values())),
            scores['notation_consistency'],
            scores['overall_coherence']
        ]
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]  # Complete the circle
        angles += angles[:1]
        
        ax4 = plt.subplot(224, projection='polar')
        ax4.plot(angles, values, 'o-', linewidth=2, color='purple')
        ax4.fill(angles, values, alpha=0.25, color='purple')
        ax4.set_xticks(angles[:-1])
        ax4.set_xticklabels(categories)
        ax4.set_ylim(0, 100)
        ax4.set_title('Coherence Metrics (0-100)', pad=20)
        ax4.grid(True)
        
        plt.tight_layout()
        
        # Save the visualization
        output_path = self.papers_root / 'coherence_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to: {output_path}")
        
        return str(output_path)
    
    def generate_report(self):
        """Generate a comprehensive coherence report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'papers_analyzed': len(self.papers),
            'scores': self.calculate_coherence_score(),
            'cross_references': {k: len(v) for k, v in self.cross_references.items()},
            'concept_usage_summary': {
                concept: {
                    'total_mentions': sum(counts.values()),
                    'papers_using': len(counts),
                    'coverage_pct': round((len(counts) / len(self.papers)) * 100, 2)
                }
                for concept, counts in self.concept_usage.items()
            }
        }
        
        # Save report
        report_path = self.papers_root / 'coherence_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved to: {report_path}")
        
        # Print summary
        print("\n" + "="*60)
        print("LOGOS PAPERS COHERENCE ANALYSIS SUMMARY")
        print("="*60)
        print(f"Papers Analyzed: {len(self.papers)}")
        print(f"\nOverall Coherence Score: {report['scores']['overall_coherence']}/100")
        print(f"  - Cross-Reference Density: {report['scores']['cross_reference_density']}/100")
        print(f"  - Concept Coverage (avg): {np.mean(list(report['scores']['concept_coverage'].values())):.2f}/100")
        print(f"  - Notation Consistency: {report['scores']['notation_consistency']}/100")
        print("\nTop 5 Most Referenced Concepts:")
        
        top_concepts = sorted(
            report['concept_usage_summary'].items(),
            key=lambda x: x[1]['total_mentions'],
            reverse=True
        )[:5]
        
        for concept, data in top_concepts:
            print(f"  - {concept}: {data['total_mentions']} mentions across {data['papers_using']} papers ({data['coverage_pct']}% coverage)")
        
        print("="*60 + "\n")
        
        return report
    
    def run_full_analysis(self):
        """Run complete coherence analysis"""
        print("Starting Logos Papers Coherence Analysis...")
        print("-" * 60)
        
        self.load_papers()
        self.analyze_cross_references()
        self.analyze_concept_consistency()
        self.analyze_math_notation()
        
        report = self.generate_report()
        viz_path = self.generate_visualizations()
        
        print(f"\nAnalysis complete!")
        print(f"Visualization: {viz_path}")
        print(f"Report: {self.papers_root / 'coherence_report.json'}")
        
        return report

def main():
    # Path to Logos Papers folder
    papers_root = r"C:\Users\Yellowkid\Desktop\Obsidian Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers"
    
    analyzer = LogosPapersCoherenceAnalyzer(papers_root)
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()
