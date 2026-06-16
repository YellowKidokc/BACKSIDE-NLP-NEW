import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# --- 1. Setup (TVE Standard) ---
DARK_BG = '#0a0a0a'
GREEN_ACTUAL = '#00FF00'  # Soul Field (ΨS)
CYAN_OBSERVER = '#00FFFF' # High Φ System
PURPLE_FIELD = '#9933FF'  # Low Φ System
GOLD_LOGOS = '#FFD700'    # The Coupling
WHITE_SOURCE = '#FFFFFF'

fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
ax = fig.add_subplot(111, projection='3d', facecolor=DARK_BG)
ax.set_axis_off()

# Helper for glowing lines
def plot_glowing_line(x_data, y_data, z_data, core_color, glow_color, core_linewidth, glow_linewidth, alpha):
    ax.plot(x_data, y_data, z_data, color=glow_color, linewidth=glow_linewidth, alpha=alpha/2)
    ax.plot(x_data, y_data, z_data, color=core_color, linewidth=core_linewidth, alpha=alpha)

# --- 2. The Geometry (Experimental: Side-by-Side Comparison) ---

# --- The "Soul Field" (The Source Wave) ---
x_soul = np.linspace(-10, 10, 80)
y_soul = np.linspace(-10, 10, 80)
X_soul, Y_soul = np.meshgrid(x_soul, y_soul)
Z_soul = 2 * np.sin(X_soul/2) * np.cos(Y_soul/2) + 10 # Positioned high up
ax.plot_surface(X_soul, Y_soul, Z_soul, color=GREEN_ACTUAL, alpha=0.3, 
                rstride=2, cstride=2, linewidth=0, antialiased=True)
ax.text(0, 0, 14, 'Soul Field (ΨS)', color=GREEN_ACTUAL, 
        ha='center', fontsize=24, weight='bold')

# --- Left Side: "Low Φ System" (Weak Coupling) ---
ax.text(-7, 0, 5, 'Low Φ System (e.g., Simple Brain)', color=PURPLE_FIELD, 
        ha='center', fontsize=22, weight='bold')
# Dim, chaotic particle cloud
np.random.seed(1)
x_low = np.random.normal(-7, 1, 300)
y_low = np.random.normal(0, 1, 300)
z_low = np.random.normal(0, 1, 300)
ax.scatter(x_low, y_low, z_low, c=PURPLE_FIELD, s=50, alpha=0.2)
# Weak Coupling Line
plot_glowing_line([-7, -7], [0, 0], [1, 9], 
                  GOLD_LOGOS, GOLD_LOGOS, 1, 4, 0.4)
ax.text(-7, 0, -3, 'Weak Coupling (g)', color=GOLD_LOGOS, 
        ha='center', fontsize=18, style='italic')

# --- Right Side: "High Φ System" (Strong Coupling) ---
ax.text(7, 0, 5, 'High Φ System (e.g., Human Brain)', color=CYAN_OBSERVER, 
        ha='center', fontsize=22, weight='bold')
# Bright, ordered lattice
x_hi = np.linspace(6, 8, 3)
y_hi = np.linspace(-1, 1, 3)
z_hi = np.linspace(-1, 1, 3)
# Create 3D grid points
for x in x_hi:
    for y in y_hi:
        for z in z_hi:
            ax.scatter([x], [y], [z], c=CYAN_OBSERVER, s=400, alpha=1.0, marker='D')
# Draw connecting lines to show structure
for x in x_hi:
    for y in y_hi:
        ax.plot([x, x], [y, y], [z_hi[0], z_hi[-1]], color=CYAN_OBSERVER, alpha=0.7, linewidth=1)
for x in x_hi:
    for z in z_hi:
        ax.plot([x, x], [y_hi[0], y_hi[-1]], [z, z], color=CYAN_OBSERVER, alpha=0.7, linewidth=1)
for y in y_hi:
    for z in z_hi:
        ax.plot([x_hi[0], x_hi[-1]], [y, y], [z, z], color=CYAN_OBSERVER, alpha=0.7, linewidth=1)
# Strong Coupling Beam
plot_glowing_line([7, 7], [0, 0], [2, 9], 
                  GOLD_LOGOS, GOLD_LOGOS, 8, 20, 0.9)
ax.text(7, 0, -3, 'Strong Coupling (g)', color=GOLD_LOGOS, 
        ha='center', fontsize=18, weight='bold')

# --- 3. Titles and Labels (Using fig.text) ---
fig.text(0.5, 0.95, 'Paper 5: H3 - Integrated Information (Φ)',
         ha='center', fontsize=60, color='white', weight='bold')
fig.text(0.5, 0.90, 'Higher Φ Creates a Stronger "Antenna" for the Soul Field',
         ha='center', fontsize=24, color=WHITE_SOURCE, style='italic')

# --- BOTTOM TAGLINE ---
fig.text(0.5, 0.05, 'A system\'s complexity (Φ) determines its coupling strength (g) to the Soul Field (ΨS).',
         ha='center', fontsize=20, color='gray', style='italic')

# --- 4. Camera and Export ---
ax.view_init(elev=20, azim=0)
ax.set_xlim([-12, 12])
ax.set_ylim([-10, 10])
ax.set_zlim([-5, 15])

plt.savefig('PAPER_05_V4_Integrated_Information.png',
            dpi=300, facecolor=DARK_BG, bbox_inches='tight')
print("✓ Integrated Information (Φ) visualization saved as PAPER_05_V4_Integrated_Information.png")
plt.show()

