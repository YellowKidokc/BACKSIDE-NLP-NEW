import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# --- 1. Setup (TVE Standard) ---
DARK_BG = '#0a0a0a'
GREEN_ACTUAL = '#00FF00'  # Soul Field (ΨS)
CYAN_OBSERVER = '#00FFFF' # Matter Field (ψe - electron)
GOLD_LOGOS = '#FFD700'    # Yukawa Coupling (g)
WHITE_SOURCE = '#FFFFFF'

fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
ax = fig.add_subplot(111, projection='3d', facecolor=DARK_BG)
ax.set_axis_off()

# Helper function to create a 3D sphere surface with glow
def create_sphere_with_glow(x_center, y_center, z_center, radius, core_color, glow_color, core_alpha):
    theta = np.linspace(0, 2 * np.pi, 60)
    phi = np.linspace(0, np.pi, 60)
    THETA, PHI = np.meshgrid(theta, phi)
    x_core = radius * np.sin(PHI) * np.cos(THETA) + x_center
    y_core = radius * np.sin(PHI) * np.sin(THETA) + y_center
    z_core = radius * np.cos(PHI) + z_center
    ax.plot_surface(x_core, y_core, z_core, color=core_color, alpha=core_alpha, 
                    rstride=1, cstride=1, linewidth=0, antialiased=True)
    for r_glow_mult in [1.2, 1.5, 1.8]:
        r_glow = radius * r_glow_mult
        x_glow = r_glow * np.sin(PHI) * np.cos(THETA) + x_center
        y_glow = r_glow * np.sin(PHI) * np.sin(THETA) + y_center
        z_glow = r_glow * np.cos(PHI) + z_center
        ax.plot_surface(x_glow, y_glow, z_glow, color=glow_color, alpha=0.08 / r_glow_mult, 
                        rstride=1, cstride=1, linewidth=0, antialiased=True)

# --- 2. The Geometry (Experimental: Interacting Fields) ---

# --- Left Side: The "Soul Field (ΨS)" (Coherent Wave) ---
x_soul = np.linspace(-10, 0, 80)
y_soul = np.linspace(-8, 8, 80)
X_soul, Y_soul = np.meshgrid(x_soul, y_soul)
Z_soul = 2 * np.sin(X_soul/1.5 + Y_soul/1.5) # A steady, coherent wave
ax.plot_surface(X_soul, Y_soul, Z_soul, color=GREEN_ACTUAL, alpha=0.5, 
                rstride=2, cstride=2, linewidth=0, antialiased=True)
ax.text(-7, 0, 5, 'Soul Field (ΨS)', color=GREEN_ACTUAL, 
        ha='center', fontsize=24, weight='bold')

# --- Right Side: The "Matter Field (ψe)" (Particle Cloud) ---
np.random.seed(1)
x_matter = np.random.normal(7, 1, 800)
y_matter = np.random.normal(0, 1, 800)
z_matter = np.random.normal(0, 1, 800)
ax.scatter(x_matter, y_matter, z_matter, c=CYAN_OBSERVER, s=70, alpha=0.1)
create_sphere_with_glow(7, 0, 0, 0.8, CYAN_OBSERVER, CYAN_OBSERVER, 0.8) # Core particle
ax.text(7, 0, 5, 'Matter Field (ψe)', color=CYAN_OBSERVER, 
        ha='center', fontsize=24, weight='bold')

# --- The "Yukawa Coupling (g)" (Gold beam) ---
# The interaction particle/beam
ax.plot([0, 7], [0, 0], [0, 0], color=GOLD_LOGOS, 
        linewidth=8, alpha=0.9, linestyle='--')
create_sphere_with_glow(3.5, 0, 0, 0.5, GOLD_LOGOS, GOLD_LOGOS, 1.0) # The "particle"
ax.text(3.5, 0, -3, 'Yukawa Coupling (g)', color=GOLD_LOGOS, 
        ha='center', fontsize=22, weight='bold')

# --- 3. Titles and Labels (Using fig.text) ---
fig.text(0.5, 0.95, 'Paper 5: Yukawa Coupling',
         ha='center', fontsize=60, color='white', weight='bold')
fig.text(0.5, 0.90, 'The Physical Mechanism of Soul-Matter Interaction',
         ha='center', fontsize=24, color=WHITE_SOURCE, style='italic')

# --- BOTTOM TAGLINE ---
fig.text(0.5, 0.05, 'The Soul Field (ΨS) "couples" to the Matter Field (ψe) via the Yukawa interaction (g), allowing mind to influence matter.',
         ha='center', fontsize=20, color='gray', style='italic')

# --- 4. Camera and Export ---
ax.view_init(elev=20, azim=25)
ax.set_xlim([-12, 12])
ax.set_ylim([-10, 10])
ax.set_zlim([-8, 8])

plt.savefig('PAPER_05_V3_Yukawa_Coupling.png',
            dpi=300, facecolor=DARK_BG, bbox_inches='tight')
print("✓ Yukawa Coupling visualization saved as PAPER_05_V3_Yukawa_Coupling.png")
plt.show()

