import matplotlib.pyplot as plt
import numpy as np

# --- Configuration ---
plt.rcParams['figure.facecolor'] = '#121212'
plt.rcParams['text.color'] = '#CCCCCC'

# --- Data: Cosmic Fate Curves ---
T = np.linspace(0, 10, 100)

# 1. Decay Path (Entropy/Heat Death) - Exponentially increasing disorder
S_decay = 10 * np.exp(T * 0.15) 

# 2. Restoration Path (Negentropy/New Creation) - Exponentially increasing coherence/order
S_restoration = 10 * np.exp(-T * 0.15)
S_restoration_inverted = 15 - S_restoration 

# --- The Plot ---
fig, ax = plt.subplots(figsize=(10, 6))

# 1. Decay Path (The Path of the Fallen World)
ax.plot(T, S_decay, color='#DC143C', linewidth=4, label='Path of Decay (Heat Death)')
ax.text(8, S_decay[-1] - 5, "Maximum Spiritual Entropy", color='#DC143C', fontsize=10)

# 2. Restoration Path (The Path of the Master Equation)
ax.plot(T, S_restoration_inverted, color='#00FF7F', linewidth=4, label='Path of Restoration (New Creation)')
ax.text(8, S_restoration_inverted[-1] + 2, r"Eternal Coherence ($\Delta S \to 0$)", color='#00FF7F', fontsize=10)

# Labels and Title
ax.set_title("Figure 4: The Final Blueprint (Eternal Coherence vs. Decay)", color='#CCCCCC', fontsize=14, fontweight='bold')
ax.set_xlabel('Time (t) / Progression to Eternity', color='#CCCCCC', fontsize=12)
ax.set_ylabel('Informational Order / Coherence Level', color='#CCCCCC', fontsize=12)
ax.set_ylim(0, 45)
ax.grid(color='gray', linestyle=':', linewidth=0.5)
ax.legend(facecolor='#1C1C1C', edgecolor='#CCCCCC', labelcolor='#CCCCCC', fontsize=11)
ax.tick_params(axis='both', colors='#CCCCCC')

plt.tight_layout()
plt.savefig('cosmic_fate_curves.png', dpi=300, facecolor='#121212', bbox_inches='tight')
print("Image saved as 'cosmic_fate_curves.png'")
plt.close()



