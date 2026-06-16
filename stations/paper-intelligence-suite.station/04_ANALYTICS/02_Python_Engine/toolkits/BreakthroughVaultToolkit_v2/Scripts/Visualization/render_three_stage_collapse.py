import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Semantic Colors (locked palette)
DARK_BG = '#0a0a0a'
CYAN_OBSERVER = '#00FFFF'
GOLD_LOGOS = '#FFD700'
PURPLE_FIELD = '#9933FF'
RED_CHAOS = '#FF0000'
GREEN_ACTUAL = '#00FF00'
WHITE_SOURCE = '#FFFFFF'

# Canvas: Pure black void
fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
ax = fig.add_subplot(111, projection='3d')

# Hide all axes/grids for freestanding geometry
ax.set_axis_off()
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

# Stage 1: Superposition - Infinite potential (PURPLE_FIELD wavy surface + RED_CHAOS particle cloud)
# Wavy potential surface (field substrate)
theta = np.linspace(0, 2*np.pi, 20)
phi = np.linspace(0, np.pi, 10)
theta, phi = np.meshgrid(theta, phi)
r = 1 + 0.5 * np.sin(5*phi)  # Wavy potential
x_super = r * np.sin(phi) * np.cos(theta)
y_super = r * np.sin(phi) * np.sin(theta)
z_super = r * np.cos(phi)
ax.plot_surface(x_super, y_super, z_super, color=PURPLE_FIELD, alpha=0.3)

# Quantum probability clouds (chaos/errors)
np.random.seed(42)
n_points = 200
x_cloud = np.random.uniform(-3, 3, n_points)
y_cloud = np.random.uniform(-3, 3, n_points)
z_cloud = np.random.uniform(-3, 3, n_points)
ax.scatter(x_cloud, y_cloud, z_cloud, c=RED_CHAOS, alpha=0.6, s=20)

# Stage 2: Observation - CYAN_OBSERVER beam from origin (left-to-center flow)
obs_x = np.linspace(0, 0, 50)
obs_y = np.linspace(0, 0, 50)
obs_z = np.linspace(-4, 4, 50)
ax.plot(obs_x, obs_y, obs_z, color=CYAN_OBSERVER, linewidth=4, alpha=0.8)

# Stage 3: Collapse to coherent path - GREEN_ACTUAL line to GOLD_LOGOS sphere (center-to-right)
# Coherent path: straight line from superposition edge to actualized
path_x = np.linspace(2, 0, 100)
path_y = np.linspace(0, 0, 100)
path_z = np.linspace(0, 3, 100)
ax.plot(path_x, path_y, path_z, color=GREEN_ACTUAL, linewidth=6, alpha=1.0)

# Actualized sphere: GOLD_LOGOS at end point (right side)
u = np.linspace(0, 2*np.pi, 20)
v = np.linspace(0, np.pi, 10)
sphere_x = 1 * np.outer(np.cos(u), np.sin(v))
sphere_y = 1 * np.outer(np.sin(u), np.sin(v))
sphere_z = 1 * np.outer(np.ones(np.size(u)), np.cos(v)) + 3
ax.plot_surface(sphere_x, sphere_y, sphere_z, color=GOLD_LOGOS, alpha=0.7)

# Big Text Labels (floating, spread: left/center/right)
ax.text(0, 0, 5, 'STAGE 1: SUPERPOSITION\nInfinite Potential', color=WHITE_SOURCE, fontsize=16, ha='center')
ax.text(-4, 0, 0, 'STAGE 2: OBSERVATION\nCollapse Beam', color=CYAN_OBSERVER, fontsize=16, ha='center')
ax.text(0, -4, 3, 'STAGE 3: ACTUALIZATION\nOne Coherent Path', color=GREEN_ACTUAL, fontsize=16, ha='center')

# Camera: Magical angle for intuitive flow (elev for depth, azim for spread)
ax.view_init(elev=25, azim=45)
ax.set_box_aspect([1,1,1])  # Equal scales, no distortion

# Export: Publication-grade
plt.savefig('PAPER_01_V1_THREE_STAGE_COLLAPSE.png', dpi=300, facecolor=DARK_BG, bbox_inches='tight')
print("✓ Visualization saved as PAPER_01_V1_THREE_STAGE_COLLAPSE.png")
plt.show()

