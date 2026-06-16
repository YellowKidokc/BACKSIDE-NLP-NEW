import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Semantic Colors (locked)
DARK_BG = '#0a0a0a'
CYAN_OBSERVER = '#00FFFF'
GOLD_LOGOS = '#FFD700'
PURPLE_FIELD = '#9933FF'
RED_CHAOS = '#FF0000'
GREEN_ACTUAL = '#00FF00'
WHITE_SOURCE = '#FFFFFF'

# Canvas: Void
fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
ax = fig.add_subplot(111, projection='3d')
ax.set_axis_off()
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

# Stage 1: Superposition - Wavy purple surface + variable-size red chaos cloud
theta = np.linspace(0, 2*np.pi, 20)
phi = np.linspace(0, np.pi, 10)
theta, phi = np.meshgrid(theta, phi)
r = 1 + 0.5 * np.sin(5*phi)
x_super = r * np.sin(phi) * np.cos(theta)
y_super = r * np.sin(phi) * np.sin(theta)
z_super = r * np.cos(phi)
ax.plot_surface(x_super, y_super, z_super, color=PURPLE_FIELD, alpha=0.3)

# Red chaos: Variable sizes (larger near surface)
np.random.seed(42)
n_points = 300  # Upped for density
x_cloud = np.random.uniform(-3, 3, n_points)
y_cloud = np.random.uniform(-3, 3, n_points)
z_cloud = np.random.uniform(-3, 3, n_points)

# Calculate distance to surface center for size variation
dist_to_surface = np.sqrt(x_cloud**2 + y_cloud**2 + z_cloud**2)  # Approx distance
sizes = 50 * (1 / (1 + dist_to_surface))  # Bigger near purple
ax.scatter(x_cloud, y_cloud, z_cloud, c=RED_CHAOS, alpha=0.6, s=sizes)

# Stage 2: Observation - Thicker cyan beam + glow (overlapping faded lines)
obs_z = np.linspace(-4, 4, 50)
for alpha in [0.8, 0.5, 0.3]:  # Glow layers
    ax.plot([0]*50, [0]*50, obs_z, color=CYAN_OBSERVER, linewidth=6-alpha*2, alpha=alpha)

# Stage 3: Actualization - Tapered green funnel tube to gold sphere
# Funnel: Simple cone via Poly3DCollection
verts_funnel = [  # Trapezoid slices along path
    [[2,0,0], [0,0,0], [0,0,3], [2,0,3]],  # Base to tip
    # Add more for 3D tube if needed, but keep light
]
ax.add_collection3d(Poly3DCollection(verts_funnel, alpha=0.4, color=GREEN_ACTUAL))

# Gold sphere with core highlight
u = np.linspace(0, 2*np.pi, 20)
v = np.linspace(0, np.pi, 10)
sphere_x = 1 * np.outer(np.cos(u), np.sin(v))
sphere_y = 1 * np.outer(np.sin(u), np.sin(v))
sphere_z = 1 * np.outer(np.ones(np.size(u)), np.cos(v)) + 3
ax.plot_surface(sphere_x, sphere_y, sphere_z, color=GOLD_LOGOS, alpha=0.7)

# Core glow: Inner scatter ring
core_r = 0.3
core_theta = np.linspace(0, 2*np.pi, 50)
core_x = core_r * np.cos(core_theta) + 0
core_y = core_r * np.sin(core_theta) + 0
core_z = np.full(50, 3.5)
ax.scatter(core_x, core_y, core_z, c=GOLD_LOGOS, s=100, alpha=0.9)

# Big floating text (spread layout)
ax.text(0, 0, 5, 'STAGE 1:\nSUPERPOSITION\nInfinite Potential', color=WHITE_SOURCE, fontsize=18, ha='center')
ax.text(-4, 0, 0, 'STAGE 2:\nOBSERVATION\nCollapse Beam', color=CYAN_OBSERVER, fontsize=18, ha='center')
ax.text(0, -4, 3, 'STAGE 3:\nACTUALIZATION\nOne Coherent Path', color=GREEN_ACTUAL, fontsize=18, ha='center')

# Camera & aspect
ax.view_init(elev=25, azim=45)
ax.set_box_aspect([1,1,1])

# Export
plt.savefig('PAPER_01_V2_THREE_STAGE_COLLAPSE.png', dpi=300, facecolor=DARK_BG, bbox_inches='tight')
print("✓ Enhanced visualization saved as PAPER_01_V2_THREE_STAGE_COLLAPSE.png")
plt.show()

