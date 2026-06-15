import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch, Wedge
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.patches as mpatches

# ==============================================================================
# LAW 1: GRAVITY AND SIN - FIGURES 1-4
# ==============================================================================

# Figure 1: Gravitational Well of Sin
print("Rendering Law 1 - Figure 1: Gravitational Well of Sin...")
try:
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    r = np.linspace(0.1, 5, 100)
    theta = np.linspace(0, 2*np.pi, 100)
    R, Theta = np.meshgrid(r, theta)
    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)
    Z = -1/R - 0.5*R**2

    surf = ax.plot_surface(X, Y, Z, cmap='RdYlBu_r', alpha=0.8, edgecolor='none')
    ax.contour(X, Y, Z, levels=10, colors='black', linewidths=0.5, alpha=0.3)

    trajectory_r = np.linspace(4, 0.5, 50)
    trajectory_theta = np.linspace(0, 8*np.pi, 50)
    trajectory_x = trajectory_r * np.cos(trajectory_theta)
    trajectory_y = trajectory_r * np.sin(trajectory_theta)
    trajectory_z = -1/trajectory_r - 0.5*trajectory_r**2

    ax.plot(trajectory_x, trajectory_y, trajectory_z, 'r-', linewidth=3, label='Path into Sin')

    escape_r = np.linspace(0.5, 4, 30)
    escape_theta = np.linspace(8*np.pi, 10*np.pi, 30)
    escape_x = escape_r * np.cos(escape_theta)
    escape_y = escape_r * np.sin(escape_theta)
    escape_z = -1/escape_r - 0.5*escape_r**2 + np.linspace(0, 8, 30)

    ax.plot(escape_x, escape_y, escape_z, linewidth=3, linestyle='--', color='g', label='Redemption (Grace)')

    ax.set_xlabel('X (Moral Space)', fontsize=12, labelpad=10)
    ax.set_ylabel('Y (Moral Space)', fontsize=12, labelpad=10)
    ax.set_zlabel('Spiritual Potential V(r)', fontsize=12, labelpad=10)
    ax.set_title(r'Figure 1: The Gravitational Well of Sin' + '\n"For the wages of sin is death" (Romans 6:23)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(fontsize=11, loc='upper left')
    ax.view_init(elev=25, azim=45)

    plt.colorbar(surf, ax=ax, shrink=0.5, label='Potential Depth')
    plt.tight_layout()
    plt.savefig('law1_fig1_gravitational_well.png', dpi=300, bbox_inches='tight')
    print("Image saved as 'law1_fig1_gravitational_well.png'")
    plt.close()
except Exception as e:
    print(f"Error rendering Figure 1: {e}")

# Figure 2: Mass Curves Spacetime / Sin Curves Reality
print("Rendering Law 1 - Figure 2: Mass Curves Spacetime...")
try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z_flat = np.zeros_like(X)

    ax1.contourf(X, Y, Z_flat, levels=20, cmap='Greys', alpha=0.3)

    for i in range(-5, 6, 1):
        ax1.plot(x, [i]*len(x), 'b-', linewidth=0.5, alpha=0.5)
        ax1.plot([i]*len(y), y, 'b-', linewidth=0.5, alpha=0.5)

    mass_circle = Circle((0, 0), 0.8, color='gold', zorder=5)
    ax1.add_patch(mass_circle)
    ax1.text(0, 0, 'M', fontsize=20, ha='center', va='center', fontweight='bold')

    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-5, 5)
    ax1.set_xlabel('Space X', fontsize=12)
    ax1.set_ylabel('Space Y', fontsize=12)
    ax1.set_title('Flat Spacetime (No Mass)\nRighteous Reality', fontsize=13, fontweight='bold')
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)

    R = np.sqrt(X**2 + Y**2)
    Z_curved = -2 / (R + 0.5)

    ax2.contourf(X, Y, Z_curved, levels=20, cmap='RdYlBu_r', alpha=0.7)

    r_grid = np.linspace(0.5, 5, 10)
    theta_grid = np.linspace(0, 2*np.pi, 50)

    for r in r_grid:
        x_circle = r * np.cos(theta_grid)
        y_circle = r * np.sin(theta_grid)
        ax2.plot(x_circle, y_circle, 'k-', linewidth=0.5, alpha=0.6)

    theta_lines = np.linspace(0, 2*np.pi, 12, endpoint=False)
    for theta in theta_lines:
        x_line = np.linspace(0.5, 5, 20) * np.cos(theta)
        y_line = np.linspace(0.5, 5, 20) * np.sin(theta)
        ax2.plot(x_line, y_line, 'k-', linewidth=0.5, alpha=0.6)

    sin_circle = Circle((0, 0), 0.8, color='darkred', zorder=5)
    ax2.add_patch(sin_circle)
    ax2.text(0, 0, 'SIN', fontsize=16, ha='center', va='center', 
             fontweight='bold', color='white')

    ax2.set_xlim(-5, 5)
    ax2.set_ylim(-5, 5)
    ax2.set_xlabel('Reality X', fontsize=12)
    ax2.set_ylabel('Reality Y', fontsize=12)
    ax2.set_title('Curved Reality (Sin Present)\n"Sin distorts all creation"', 
                  fontsize=13, fontweight='bold')
    ax2.set_aspect('equal')

    plt.suptitle('Figure 2: Sin Curves Reality (Law 1 Analogy)\nMass curves spacetime → Sin curves spiritual reality', 
                 fontsize=15, fontweight='bold', y=1.00)

    plt.tight_layout()
    plt.savefig('law1_fig2_curved_reality.png', dpi=300, bbox_inches='tight')
    print("Image saved as 'law1_fig2_curved_reality.png'")
    plt.close()
except Exception as e:
    print(f"Error rendering Figure 2: {e}")

# Figure 3: Escape Velocity from Sin
print("Rendering Law 1 - Figure 3: Escape Velocity from Sin...")
try:
    fig, ax = plt.subplots(figsize=(12, 9))

    v_attempt = np.linspace(0, 15, 8)
    colors_grad = plt.cm.RdYlGn(np.linspace(0.2, 0.9, len(v_attempt)))

    for i, v in enumerate(v_attempt):
        t = np.linspace(0, 3, 100)
        y = v*t - 5*t**2
        y = np.maximum(y, 0)
        
        if v < 10:
            label = f'Human Effort: v={v:.1f}m/s (Falls Back)'
            linestyle = '-'
            linewidth = 2
        elif v < 11:
            label = f'Threshold: v={v:.1f}m/s'
            linestyle = '--'
            linewidth = 3
        else:
            label = f'Divine Grace: v={v:.1f}m/s (Escapes!)'
            linestyle = '-'
            linewidth = 2.5
        
        ax.plot(t, y, color=colors_grad[i], linewidth=linewidth, 
                linestyle=linestyle, label=label, alpha=0.8)

    ax.axhline(y=10, color='gold', linewidth=3, linestyle=':', 
               label='Escape Threshold (Salvation)', alpha=0.7)

    ax.fill_between([0, 3], 0, 10, color='red', alpha=0.1, label='Gravitational Bound (Sin)')
    ax.fill_between([0, 3], 10, 15, color='green', alpha=0.1, label='Freedom Region (Grace)')

    ax.set_xlabel('Time t (Journey of Faith)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Height y (Spiritual Position)', fontsize=13, fontweight='bold')
    ax.set_title(r'Figure 3: Escape Velocity from Sin' + '\n"Not by works... but by grace through faith" (Ephesians 2:8-9)', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.legend(fontsize=10, loc='upper right', framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 15)

    textstr = 'Human effort alone (v < v_escape):\nCannot overcome sin\'s gravity\n\nDivine grace (v ≥ v_escape):\nProvides escape velocity'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.97, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.savefig('law1_fig3_escape_velocity.png', dpi=300, bbox_inches='tight')
    print("Image saved as 'law1_fig3_escape_velocity.png'")
    plt.close()
except Exception as e:
    print(f"Error rendering Figure 3: {e}")

# Figure 4: Orbital Decay vs. Grace Boost
print("Rendering Law 1 - Figure 4: Orbital Mechanics of Faith...")
try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), subplot_kw={'projection': 'polar'})

    n_orbits = 5
    theta_decay = np.array([])
    r_decay = np.array([])

    for i in range(n_orbits):
        theta_orbit = np.linspace(0, 2*np.pi, 100) + i*2*np.pi
        r_orbit = 5 - i*0.8 - 0.1*theta_orbit
        r_orbit = np.maximum(r_orbit, 0.5)
        theta_decay = np.concatenate([theta_decay, theta_orbit])
        r_decay = np.concatenate([r_decay, r_orbit])

    ax1.plot(theta_decay, r_decay, 'r-', linewidth=2.5, label='Orbital Decay (Sin\'s Pull)')
    ax1.plot([theta_decay[-1]], [r_decay[-1]], 'ro', markersize=15, label='Crash Point')
    ax1.fill_between(np.linspace(0, theta_decay[-1], 100), 0, 0.5, 
                      color='darkred', alpha=0.3, label='Event Horizon (Death)')

    ax1.set_ylim(0, 6)
    ax1.set_title('WITHOUT GRACE: Orbital Decay into Sin\n"The soul who sins shall die" (Ezekiel 18:20)', 
                  fontsize=12, fontweight='bold', pad=20)
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)

    theta_stable = np.linspace(0, 6*np.pi, 500)
    r_base = 4.0
    r_stable = r_base + 0.3*np.sin(theta_stable) - 0.05*theta_stable

    grace_boosts = [2*np.pi, 4*np.pi, 6*np.pi]
    for boost_angle in grace_boosts:
        idx = np.argmin(np.abs(theta_stable - boost_angle))
        boost_magnitude = 1.2
        r_stable[idx:] += boost_magnitude

    r_stable = np.maximum(r_stable, 0.5)

    ax2.plot(theta_stable, r_stable, 'g-', linewidth=2.5, label='Sustained Orbit (Grace)')

    for boost_angle in grace_boosts:
        ax2.plot([boost_angle], [r_base + 1.2], 'go', markersize=12)
        ax2.annotate('Grace\nBoost', xy=(boost_angle, r_base + 1.2), 
                     xytext=(boost_angle + 0.5, r_base + 2),
                     fontsize=9, ha='center', fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color='green', lw=2))

    ax2.fill_between(theta_stable, r_base - 0.5, r_base + 0.5, 
                      color='green', alpha=0.2, label='Stable Orbit Zone')

    ax2.set_ylim(0, 6)
    ax2.set_title('WITH GRACE: Sustained Orbit\n"My grace is sufficient" (2 Corinthians 12:9)', 
                  fontsize=12, fontweight='bold', pad=20)
    ax2.legend(loc='upper right', fontsize=10)
    ax2.grid(True, alpha=0.3)

    plt.suptitle('Figure 4: Orbital Mechanics of Faith\nSin pulls us down → Grace lifts us up', 
                 fontsize=15, fontweight='bold', y=0.98)

    plt.tight_layout()
    plt.savefig('law1_fig4_orbital_mechanics.png', dpi=300, bbox_inches='tight')
    print("Image saved as 'law1_fig4_orbital_mechanics.png'")
    plt.close()
except Exception as e:
    print(f"Error rendering Figure 4: {e}")

print("\n--- Law 1 visualization suite complete. ---")

