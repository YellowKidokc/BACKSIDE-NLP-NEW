Yeah that's trueYeah Should we populate these with the linking tables do you have the Excel people person place first ready to import What do you mean by manually provide key linkagewhgAT import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# --- 1. Setup (TVE Standard) ---
DARK_BG = '#0a0a0a'
PURPLE_FIELD = '#9933FF'  # The Potential Field
GREEN_ACTUAL = '#00FF00'  # The Stable Soul Quanta
RED_CHAOS = '#FF0000'     # Unstable State
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

# --- 2. The Geometry (Experimental: "Sombrero" Wireframe) ---

# --- The "Sombrero" Potential (φ⁴ field) ---
v = 6  # Radius of the trough (making it large)
wireframe_offset = 5  # Raise the wireframe to avoid overlap with red peak
X = np.linspace(-10, 10, 100)
Y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = (R**2 - v**2)**2 * 0.1 - 10 + wireframe_offset # Scale it down and raise it
ax.plot_wireframe(X, Y, Z, color=PURPLE_FIELD, alpha=0.3, 
                  rstride=5, cstride=5, linewidth=1)
ax.text(0, 0, 35, 'V(ΨS) (Soul Field Potential)', color=PURPLE_FIELD, 
        ha='center', fontsize=22, weight='bold')

# --- The "Unstable" Peak (Red) ---
create_sphere_with_glow(0, 0, (0-v**2)**2 * 0.1 - 10, 1.5, RED_CHAOS, RED_CHAOS, 0.8)
ax.text(0, 0, 29, '"False Vacuum" (Unstable)', color=RED_CHAOS, 
        ha='center', fontsize=20, weight='bold')

# --- The "Stable" Souls (Green, in the trough) ---
# Soul 1
soul_angle1 = np.pi / 3
soul_x1 = v * np.cos(soul_angle1)
soul_y1 = v * np.sin(soul_angle1)
soul_z1 = (np.sqrt(soul_x1**2 + soul_y1**2)**2 - v**2)**2 * 0.1 - 10 + wireframe_offset # Z position (raised with wireframe)
create_sphere_with_glow(soul_x1, soul_y1, soul_z1 + 1.5, 2.0, GREEN_ACTUAL, GREEN_ACTUAL, 0.9) # +1.5 to lift it
ax.text(soul_x1, soul_y1, soul_z1 - 3, 'Stable Soul Quanta', color=GREEN_ACTUAL, 
        ha='center', fontsize=20, weight='bold')

# Soul 2
soul_angle2 = np.pi * 1.5
soul_x2 = v * np.cos(soul_angle2)
soul_y2 = v * np.sin(soul_angle2)
soul_z2 = (np.sqrt(soul_x2**2 + soul_y2**2)**2 - v**2)**2 * 0.1 - 10 + wireframe_offset # Z position (raised with wireframe)
create_sphere_with_glow(soul_x2, soul_y2, soul_z2 + 1.5, 2.0, GREEN_ACTUAL, GREEN_ACTUAL, 0.9) # +1.5 to lift it
ax.text(soul_x2, soul_y2, soul_z2 - 3, 'Stable Soul Quanta', color=GREEN_ACTUAL, 
        ha='center', fontsize=20, weight='bold')

# --- 3. Titles and Labels (Using fig.text) ---
fig.text(0.5, 0.95, 'Paper 5: The Soul Field Potential',
         ha='center', fontsize=60, color='white', weight='bold')
fig.text(0.5, 0.90, 'Why Individual Souls are Stable, Localized Entities',
         ha='center', fontsize=24, color=WHITE_SOURCE, style='italic')

# --- BOTTOM TAGLINE ---
fig.text(0.5, 0.05, 'Souls "settle" in the lowest energy state (the trough), preventing decay and ensuring stable, individual identity.',
         ha='center', fontsize=20, color='gray', style='italic')

# --- 4. Camera and Export ---
ax.view_init(elev=45, azim=45)
ax.set_xlim([-12, 12])
ax.set_ylim([-12, 12])
ax.set_zlim([-15, 40])  # Increased upper limit to accommodate raised wireframe

plt.savefig('PAPER_05_V2_Soul_Potential.png',
            dpi=300, facecolor=DARK_BG, bbox_inches='tight')
print("✓ Soul Field Potential visualization saved as PAPER_05_V2_Soul_Potential.png")
plt.show()

