import matplotlib.pyplot as plt
import networkx as nx

# --- Configuration ---
plt.rcParams['figure.facecolor'] = '#121212'
plt.rcParams['text.color'] = '#CCCCCC'

print("Rendering Master Equation Network Diagram...")

try:
    # --- Data: Master Equation Convergence (10 Variables) ---
    G = nx.DiGraph()

    # Center Node (The Master Equation / Unified Soul)
    G.add_node("X", label=r"$\chi$ Master Equation" + "\n(Unified Soul Field)", pos=(0, 0), shape="o", color="#FFD700")

    # Outer Nodes (The 10 Universal Laws/Variables)
    laws = {
        "G": (-4, 2, "Gravity/Grace"), 
        "M": (-2, 4, "Mass/Motion"),
        "E": (2, 4, "Energy/Light"), 
        "S": (4, 2, "Entropy/Sin"),
        "T": (4, -2, "Time/Eternity"), 
        "K": (2, -4, "Knowledge/Logos"),
        "R": (-2, -4, "Relationships/Rxn"), 
        "Q": (-4, -2, "Quantum/Choice"),
        "F": (0, 5, "Forces/Faith"), 
        "C": (0, -5, "Consciousness/Soul") 
    }

    laws_list = list(laws.keys())

    # Edges (Convergence to the Center)
    for key in laws_list:
        G.add_edge(key, "X", label=key, weight=5)

    # --- The Plot ---
    pos = {key: (x, y) for key, (x, y, label) in laws.items()}
    pos['X'] = (0, 0)

    labels = {key: label for key, (x, y, label) in laws.items()}
    labels['X'] = r"$\chi$ (Unified Soul)"

    fig, ax = plt.subplots(figsize=(14, 14), facecolor='#121212')

    # Draw Convergence Edges with gradient effect
    for edge in G.edges():
        x_coords = [pos[edge[0]][0], pos[edge[1]][0]]
        y_coords = [pos[edge[0]][1], pos[edge[1]][1]]
        ax.plot(x_coords, y_coords, color='#00FFFF', linewidth=2, alpha=0.6, zorder=1)

    # Draw Outer Nodes (Laws)
    outer_nodes = nx.draw_networkx_nodes(G, pos, nodelist=laws_list, node_color='#FFA07A', 
                           node_size=2000, edgecolors='#CCCCCC', linewidths=2, ax=ax)
    outer_nodes.set_zorder(3)

    # Draw Center Node (Master Equation)
    center_nodes = nx.draw_networkx_nodes(G, pos, nodelist=["X"], node_color='#FFD700', 
                           node_size=5000, edgecolors='#FFFFFF', linewidths=3, ax=ax)
    center_nodes.set_zorder(4)

    # Draw Labels
    for node, (x, y) in pos.items():
        label = labels[node]
        fontsize = 11 if node != "X" else 12
        fontweight = 'bold' if node == "X" else 'normal'
        color = 'black' if node == "X" else 'white'
        
        ax.text(x, y, label, fontsize=fontsize, fontweight=fontweight, 
                color=color, ha='center', va='center', zorder=5)

    ax.set_title(r"Figure 3: The Master Equation ($\chi$) - The Universal Blueprint", 
                 color='#CCCCCC', fontsize=16, fontweight='bold', pad=20)
    
    ax.text(0, -7.5, "All 10 Laws converge to the unified field χ\nGravity + Mass + Energy + Entropy + Time + Knowledge + Relationships + Quantum + Forces + Consciousness",
            fontsize=11, ha='center', color='#00FFFF', style='italic',
            bbox=dict(boxstyle='round', facecolor='#1C1C1C', alpha=0.8, edgecolor='#00FFFF', linewidth=2))

    ax.axis('off')
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig('master_equation_network.png', dpi=300, facecolor='#121212', bbox_inches='tight')
    print("Image saved as 'master_equation_network.png'")
    plt.close()
    
except Exception as e:
    print(f"Error rendering Master Equation Network: {e}")
    import traceback
    traceback.print_exc()

print("--- Master Equation Network rendering complete. ---")

