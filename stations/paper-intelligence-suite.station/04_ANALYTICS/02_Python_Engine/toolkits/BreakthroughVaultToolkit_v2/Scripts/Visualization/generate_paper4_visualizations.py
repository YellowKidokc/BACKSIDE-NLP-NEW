#!/usr/bin/env python3
"""
Generate all 5 visualizations for Paper 4: The Syzygy Principle
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os

# Create output directory
output_dir = "COMPLETE_LOGOS_PAPERS_FINAL/assets/P4"
os.makedirs(output_dir, exist_ok=True)

# TVE Standard Colors
DARK_BG = '#0a0a0a'
GOLD_LOGOS = '#FFD700'
RED_CHAOS = '#FF0000'
WHITE_SOURCE = '#FFFFFF'
GREEN_ACTUAL = '#00FF00'
CYAN_OBSERVER = '#00FFFF'
PURPLE_FIELD = '#9933FF'

# ============================================================================
# Visualization 1: Binary States
# ============================================================================

def create_v1_binary_states():
    fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
    ax = fig.add_subplot(111, projection='3d', facecolor=DARK_BG)
    ax.set_axis_off()

    def create_glowing_plane(x_grid, y_grid, z_val, core_color, glow_color, alpha):
        X, Y = np.meshgrid(x_grid, y_grid)
        Z = np.full_like(X, z_val)
        ax.plot_surface(X, Y, Z, color=core_color, alpha=alpha, 
                        rstride=1, cstride=1, linewidth=0, antialiased=True)
        for i in range(1, 4):
            ax.plot_surface(X, Y, Z + i*0.1, color=glow_color, alpha=alpha * 0.1 / i, 
                            rstride=1, cstride=1, linewidth=0, antialiased=True)
            ax.plot_surface(X, Y, Z - i*0.1, color=glow_color, alpha=alpha * 0.1 / i, 
                            rstride=1, cstride=1, linewidth=0, antialiased=True)

    x_grid = np.linspace(-10, 10, 30)
    y_grid = np.linspace(-10, 10, 30)

    create_glowing_plane(x_grid, y_grid, 5, GOLD_LOGOS, GOLD_LOGOS, 0.5)
    ax.text(0, 0, 6.5, 'State +1 (Aligned)', color=GOLD_LOGOS, 
            ha='center', fontsize=28, weight='bold')

    create_glowing_plane(x_grid, y_grid, -5, RED_CHAOS, RED_CHAOS, 0.5)
    ax.text(0, 0, -3.5, 'State -1 (Opposed)', color=RED_CHAOS, 
            ha='center', fontsize=28, weight='bold')

    ax.scatter([5], [5], [5.1], c=WHITE_SOURCE, s=300, alpha=1.0, 
               edgecolor=GOLD_LOGOS, linewidth=2, marker='o')
    ax.text(5, 5, 3.5, 'Aligned Soul', color=WHITE_SOURCE, ha='center', fontsize=18)

    ax.scatter([-5], [-5], [-4.9], c=WHITE_SOURCE, s=300, alpha=1.0, 
               edgecolor=RED_CHAOS, linewidth=2, marker='o')
    ax.text(-5, -5, -6.5, 'Opposed Soul', color=WHITE_SOURCE, ha='center', fontsize=18)

    fig.text(0.5, 0.95, 'Paper 4: The Syzygy Principle',
             ha='center', fontsize=60, color='white', weight='bold')
    fig.text(0.5, 0.90, 'Consciousness Exists in Binary Sign States (+1 or -1)',
             ha='center', fontsize=24, color=WHITE_SOURCE, style='italic')
    fig.text(0.5, 0.05, 'The two states are parallel but fundamentally separate dimensions of moral reality.',
             ha='center', fontsize=20, color='gray', style='italic')

    ax.view_init(elev=20, azim=25)
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])
    
    plt.savefig(f'{output_dir}/P4-01-binary-states-O-1-of-5.png',
                dpi=300, facecolor=DARK_BG, bbox_inches='tight')
    plt.close()
    print("✓ Created V1: Binary States")

# ============================================================================
# Visualization 2: Impossibility of Works
# ============================================================================

def create_v2_impossibility_of_works():
    fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
    ax = fig.add_subplot(111, projection='3d', facecolor=DARK_BG)
    ax.set_axis_off()

    def plot_glowing_line(x_data, y_data, z_data, core_color, glow_color, core_linewidth, glow_linewidth, alpha):
        ax.plot(x_data, y_data, z_data, color=glow_color, linewidth=glow_linewidth, alpha=alpha/2)
        ax.plot(x_data, y_data, z_data, color=core_color, linewidth=core_linewidth, alpha=alpha)

    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x, y)
    Z = (X**2 + Y**2) * 0.1 - 10

    ax.plot_surface(X, Y, Z, color=RED_CHAOS, alpha=0.2, 
                    rstride=2, cstride=2, linewidth=0, antialiased=True)
    ax.plot_wireframe(X, Y, Z, color=RED_CHAOS, alpha=0.3, linewidth=1)
    ax.text(0, 0, -12, 'State -1 (Opposed)', color=RED_CHAOS, 
            ha='center', fontsize=24, weight='bold')

    t_works = np.linspace(0, 8 * np.pi, 200)
    x_works = (t_works/3) * np.cos(t_works)
    y_works = (t_works/3) * np.sin(t_works)
    z_works = (x_works**2 + y_works**2) * 0.1 - 10

    plot_glowing_line(x_works, y_works, z_works, CYAN_OBSERVER, CYAN_OBSERVER, 4, 12, 1.0)
    ax.text(x_works[0], y_works[0], z_works[0]+2, 'Start', color=WHITE_SOURCE, ha='center', fontsize=18)
    ax.text(x_works[-1], y_works[-1], z_works[-1]+2, 'End (Still Trapped)', color=CYAN_OBSERVER, ha='center', fontsize=20, weight='bold')

    fig.text(0.5, 0.95, 'Paper 4: Theorem 1 - Sign Preservation',
             ha='center', fontsize=60, color='white', weight='bold')
    fig.text(0.5, 0.90, 'Self-Operations ("Works") Cannot Change the State',
             ha='center', fontsize=24, color=CYAN_OBSERVER, style='italic')
    fig.text(0.5, 0.05, 'All self-effort is "unitary"—it moves *within* the current state but can never escape it.',
             ha='center', fontsize=20, color='gray', style='italic')

    ax.view_init(elev=40, azim=30)
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-15, 10])
    
    plt.savefig(f'{output_dir}/P4-02-impossibility-of-works-O-2-of-5.png',
                dpi=300, facecolor=DARK_BG, bbox_inches='tight')
    plt.close()
    print("✓ Created V2: Impossibility of Works")

# ============================================================================
# Visualization 3: Grace Operator
# ============================================================================

def create_v3_grace_operator():
    fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
    ax = fig.add_subplot(111, projection='3d', facecolor=DARK_BG)
    ax.set_axis_off()

    def create_sphere(x_center, y_center, z_center, radius, color, alpha):
        theta = np.linspace(0, 2 * np.pi, 60)
        phi = np.linspace(0, np.pi, 60)
        THETA, PHI = np.meshgrid(theta, phi)
        x = radius * np.sin(PHI) * np.cos(THETA) + x_center
        y = radius * np.sin(PHI) * np.sin(THETA) + y_center
        z = radius * np.cos(PHI) + z_center
        ax.plot_surface(x, y, z, color=color, alpha=alpha, 
                        rstride=1, cstride=1, linewidth=0, antialiased=True)

    x_l = np.linspace(-10, -1, 50)
    y_l = np.linspace(-5, 5, 50)
    X_l, Y_l = np.meshgrid(x_l, y_l)
    Z_l = ((X_l+5.5)**2 + Y_l**2) * 0.1 - 10

    ax.plot_surface(X_l, Y_l, Z_l, color=RED_CHAOS, alpha=0.2, 
                    rstride=1, cstride=1, linewidth=0, antialiased=True)
    ax.text(-5.5, 0, -12, 'State -1 (Opposed)', color=RED_CHAOS, ha='center', fontsize=22, weight='bold')

    x_r = np.linspace(1, 10, 50)
    y_r = np.linspace(-5, 5, 50)
    X_r, Y_r = np.meshgrid(x_r, y_r)
    Z_r = ((X_r-5.5)**2 + Y_r**2) * 0.1 - 10

    ax.plot_surface(X_r, Y_r, Z_r, color=GOLD_LOGOS, alpha=0.3, 
                    rstride=1, cstride=1, linewidth=0, antialiased=True)
    ax.text(5.5, 0, -12, 'State +1 (Aligned)', color=GOLD_LOGOS, ha='center', fontsize=22, weight='bold')

    create_sphere(-5.5, 0, -9.5, 0.8, WHITE_SOURCE, 0.9)
    ax.text(-5.5, 0, -8, '1. Soul in -1 State', color=WHITE_SOURCE, ha='center', fontsize=18)

    ax.plot([-5.5, -5.5], [0, 0], [10, -9.5], color=GOLD_LOGOS, 
            linewidth=10, alpha=0.7, label='Grace Operator (Ĝ)')
    ax.text(0, 0, 12, '2. The Grace Operator (Ĝ) Intervenes', color=GOLD_LOGOS, ha='center', fontsize=24, weight='bold')

    create_sphere(5.5, 0, -9.5, 0.8, GREEN_ACTUAL, 0.9)
    ax.text(5.5, 0, -8, '3. Soul "Flipped" to +1', color=GREEN_ACTUAL, ha='center', fontsize=18)

    ax.plot([-5.5, 5.5], [0, 0], [5, 5], color=GREEN_ACTUAL, 
            linestyle=':', linewidth=5, alpha=0.8)

    fig.text(0.5, 0.95, 'Paper 4: The Grace Operator (Ĝ)',
             ha='center', fontsize=60, color='white', weight='bold')
    fig.text(0.5, 0.90, 'The External, Non-Unitary Sign-Flip Mechanism',
             ha='center', fontsize=24, color=GOLD_LOGOS, style='italic')
    fig.text(0.5, 0.05, 'The soul cannot escape its own state. Grace is an external operation that "re-writes" the state.',
             ha='center', fontsize=20, color='gray', style='italic')

    ax.view_init(elev=30, azim=0)
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-15, 15])
    
    plt.savefig(f'{output_dir}/P4-03-grace-operator-O-3-of-5.png',
                dpi=300, facecolor=DARK_BG, bbox_inches='tight')
    plt.close()
    print("✓ Created V3: Grace Operator")

# ============================================================================
# Visualization 4: Magnitude vs Sign
# ============================================================================

def create_v4_magnitude_vs_sign():
    fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
    ax = fig.add_subplot(111, projection='3d', facecolor=DARK_BG)
    ax.set_axis_off()

    def plot_glowing_line(x_data, y_data, z_data, core_color, glow_color, core_linewidth, glow_linewidth, alpha):
        ax.plot(x_data, y_data, z_data, color=glow_color, linewidth=glow_linewidth, alpha=alpha/2)
        ax.plot(x_data, y_data, z_data, color=core_color, linewidth=core_linewidth, alpha=alpha)

    y_wall, z_wall = np.meshgrid(np.linspace(-10, 10, 20), np.linspace(-10, 10, 20))
    x_wall = np.zeros_like(y_wall)
    ax.plot_surface(x_wall, y_wall, z_wall, color=WHITE_SOURCE, alpha=0.1)
    ax.text(0, 0, 11, 'The Great Divide (Sign σ)', color=WHITE_SOURCE, ha='center', fontsize=24)

    ax.text(-7, 0, 8, 'Realm: σ = -1 (Opposed)', color=RED_CHAOS, ha='center', fontsize=22, weight='bold')

    t = np.linspace(0, 15, 200)
    x = -5 - 2*np.cos(t)
    y = np.sin(t*2) * 4
    z = -t/2
    plot_glowing_line(x, y, z, RED_CHAOS, RED_CHAOS, 8, 20, 0.8)
    ax.text(x[0], y[0], z[0]+2, 'Start (High Magnitude "A")', color=RED_CHAOS, ha='center', fontsize=18)

    ax.scatter([-7], [0], [-10], c=CYAN_OBSERVER, s=5000, alpha=0.3, marker='x')
    ax.text(-7, 0, -12, 'Destination: Decoherence', color=CYAN_OBSERVER, ha='center', fontsize=20)

    ax.text(7, 0, 8, 'Realm: σ = +1 (Aligned)', color=GOLD_LOGOS, ha='center', fontsize=22, weight='bold')

    ax.scatter([7], [0], [-10], c=WHITE_SOURCE, s=8000, alpha=1.0, 
               edgecolor=GOLD_LOGOS, linewidth=3, marker='*')
    ax.text(7, 0, -12, 'Destination: Coherence (Heaven)', color=WHITE_SOURCE, ha='center', fontsize=20)

    t = np.linspace(0, 15, 200)
    x_s = 5 + 2*np.cos(t)
    y_s = np.sin(t*2) * 4
    z_s = -t/2
    plot_glowing_line(x_s, y_s, z_s, GOLD_LOGOS, GOLD_LOGOS, 8, 20, 0.8)
    ax.text(x_s[0], y_s[0], z_s[0]+2, 'Start (High "A")', color=GOLD_LOGOS, ha='center', fontsize=18)
    ax.plot([x_s[-1], 7], [y_s[-1], 0], [z_s[-1], -10], 'w:', alpha=0.5)

    x_t = [5, 7]
    y_t = [8, 0]
    z_t = [0, -10]
    plot_glowing_line(x_t, y_t, z_t, GREEN_ACTUAL, GREEN_ACTUAL, 3, 10, 1.0)
    ax.text(x_t[0], y_t[0], z_t[0]+2, 'Start (Low "A")', color=GREEN_ACTUAL, ha='center', fontsize=18)

    fig.text(0.5, 0.95, 'Paper 4: Magnitude (A) vs. Sign (σ)',
             ha='center', fontsize=60, color='white', weight='bold')
    fig.text(0.5, 0.90, 'The Destiny Theorem: Sign, Not Magnitude, Determines the Outcome',
             ha='center', fontsize=24, color=WHITE_SOURCE, style='italic')
    fig.text(0.5, 0.05, 'A high magnitude of "works" (A) in the wrong state (σ=-1) fails, while even the lowest magnitude in the right state (σ=+1) succeeds.',
             ha='center', fontsize=20, color='gray', style='italic')

    ax.view_init(elev=20, azim=25)
    ax.set_xlim([-12, 12])
    ax.set_ylim([-12, 12])
    ax.set_zlim([-15, 15])
    
    plt.savefig(f'{output_dir}/P4-04-magnitude-vs-sign-O-4-of-5.png',
                dpi=300, facecolor=DARK_BG, bbox_inches='tight')
    plt.close()
    print("✓ Created V4: Magnitude vs Sign")

# ============================================================================
# Visualization 5: Age of Accountability (Null State)
# ============================================================================

def create_v5_null_state():
    fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
    ax = fig.add_subplot(111, projection='3d', facecolor=DARK_BG)
    ax.set_axis_off()

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

    create_sphere_with_glow(0, 0, 0, 2.5, WHITE_SOURCE, WHITE_SOURCE, 0.9)
    ax.text(0, 0, 4, 'Null State Soul (σ = 0)', color=WHITE_SOURCE, 
            ha='center', fontsize=24, weight='bold')
    ax.text(0, 0, -4, '(Pre-Accountability)', color='gray', 
            ha='center', fontsize=20, style='italic')

    x_r = np.linspace(-8, 8, 50)
    y_r = np.linspace(-8, 8, 50)
    X_r, Y_r = np.meshgrid(x_r, y_r)
    Z_r = -0.05 * (X_r**2 + Y_r**2) + 10
    ax.plot_surface(X_r, Y_r, Z_r, color=GOLD_LOGOS, alpha=0.3, 
                    rstride=1, cstride=1, linewidth=0, antialiased=True)
    ax.text(0, 0, 12, 'State +1 (Default Path)', color=GOLD_LOGOS, ha='center', fontsize=22)

    Z_l = 0.05 * (X_r**2 + Y_r**2) - 10
    ax.plot_surface(X_r, Y_r, Z_l, color=RED_CHAOS, alpha=0.3, 
                    rstride=1, cstride=1, linewidth=0, antialiased=True)
    ax.text(0, 0, -12, 'State -1 (No "Grip")', color=RED_CHAOS, ha='center', fontsize=22)

    ax.plot([0, 0], [0, 0], [2.5, 8], color=GOLD_LOGOS, 
            linewidth=8, alpha=0.8, linestyle=':')
    ax.text(0, 5, 5, 'Default Path of Grace', color=GOLD_LOGOS, ha='center', fontsize=20)

    ax.quiver(0, 0, -9, 0, 0, 1, color=RED_CHAOS, length=3, 
              linewidth=5, alpha=0.8, label='Sin (No Moral Agency to connect)')
    ax.text(0, 5, -7, 'Sin (No "Grip")', color=RED_CHAOS, ha='center', fontsize=20)

    fig.text(0.5, 0.95, 'Paper 4: Age of Accountability',
             ha='center', fontsize=60, color='white', weight='bold')
    fig.text(0.5, 0.90, 'The Special Case of the Null State (σ = 0)',
             ha='center', fontsize=24, color=WHITE_SOURCE, style='italic')
    fig.text(0.5, 0.05, 'The "null state" soul has no moral agency for sin to "grip," and is drawn to coherence by default.',
             ha='center', fontsize=20, color='gray', style='italic')

    ax.view_init(elev=20, azim=45)
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-15, 15])
    
    plt.savefig(f'{output_dir}/P4-05-null-state-O-5-of-5.png',
                dpi=300, facecolor=DARK_BG, bbox_inches='tight')
    plt.close()
    print("✓ Created V5: Null State (Age of Accountability)")

# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("Generating Paper 4 Visualizations")
    print("="*60)
    
    try:
        create_v1_binary_states()
        create_v2_impossibility_of_works()
        create_v3_grace_operator()
        create_v4_magnitude_vs_sign()
        create_v5_null_state()
        
        print("="*60)
        print("✓ All 5 visualizations created successfully!")
        print(f"✓ Images saved to: {output_dir}")
        print("="*60)
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

