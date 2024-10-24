import networkx as nx
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Crear el grafo
G = nx.Graph()

# Configurar la interfaz principal
root = tk.Tk()
root.title("Generador de Grafos")
root.configure(bg="purple")

# Configuración de la interfaz (izquierda y derecha)
frame_left = tk.Frame(root, bg="purple")
frame_left.pack(side=tk.LEFT, padx=10, pady=10)
frame_right = tk.Frame(root, bg="purple")
frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

# Área para entrada de vértices y aristas
tk.Label(frame_left, text="Agregar Vértice", bg="purple", fg="white").pack()
vertex_entry = tk.Entry(frame_left)
vertex_entry.pack()

tk.Label(frame_left, text="Arista (A--B)", bg="purple", fg="white").pack()
edge_entry = tk.Entry(frame_left)
edge_entry.pack()

# Botón para generar el grafo
generate_button = tk.Button(frame_left, text="Generar Grafo", command=lambda: dibujar_grafos())
generate_button.pack(pady=10)

# Listas para mostrar vértices y aristas
tk.Label(frame_right, text="Vertices", bg="purple", fg="white").pack()
vertices_list = tk.Listbox(frame_right, width=20)
vertices_list.pack()

tk.Label(frame_right, text="Aristas", bg="purple", fg="white").pack()
aristas_list = tk.Listbox(frame_right, width=20)
aristas_list.pack()

# Configuración de la figura para graficar
figure = Figure(figsize=(10, 5))
ax1 = figure.add_subplot(121)
ax2 = figure.add_subplot(122)
canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().pack()

def actualizar_resumen():
    """Actualiza las listas de vértices y aristas en la interfaz."""
    vertices_list.delete(0, tk.END)
    aristas_list.delete(0, tk.END)
    
    for vertice in G.nodes():
        vertices_list.insert(tk.END, vertice)
    
    for arista in G.edges():
        aristas_list.insert(tk.END, f"{arista[0]}--{arista[1]}")

def agregar_vertice():
    """Agrega un vértice al grafo."""
    vertice = vertex_entry.get().strip()
    if vertice and not G.has_node(vertice):
        G.add_node(vertice)
        actualizar_resumen()

def agregar_arista():
    """Agrega una arista al grafo a partir de la entrada de texto."""
    entrada = edge_entry.get().strip()
    if '--' in entrada:
        origen, destino = entrada.split('--')
        origen = origen.strip()
        destino = destino.strip()
        if origen and destino:
            G.add_edge(origen, destino)
            actualizar_resumen()

def dibujar_grafos(traversal_edges=None):
    """Dibuja los dos grafos: original y con el algoritmo aplicado."""
    ax1.clear()
    ax2.clear()

    pos = nx.spring_layout(G)
    # Dibujar grafo original con etiquetas
    nx.draw(G, pos, ax=ax1, with_labels=True, edge_color='black', node_color='black', font_color='white')
    ax1.set_title("Grafo Original")

    # Dibujar resultado del algoritmo
    if traversal_edges:
        nx.draw(G, pos, ax=ax2, with_labels=True, edge_color='black', node_color='black', font_color='white')
        nx.draw_networkx_edges(G, pos, edgelist=traversal_edges, edge_color='red', ax=ax2)
        ax2.set_title("Resultado del Algoritmo")
    else:
        nx.draw(G, pos, ax=ax2, with_labels=True, edge_color='black', node_color='black', font_color='white')
        ax2.set_title("Resultado del Algoritmo (Sin datos)")

    canvas.draw()

def ejecutar_algoritmo(traversal_func):
    """Ejecuta el algoritmo de búsqueda seleccionado (anchura o profundidad)."""
    if not G.nodes:
        messagebox.showerror("Error", "El grafo está vacío.")
        return
    
    origen = vertex_entry.get().strip()
    if not G.has_node(origen):
        messagebox.showerror("Error", "El vértice no existe en el grafo.")
        return

    traversal_edges = list(traversal_func(G, source=origen))
    dibujar_grafos(traversal_edges)

# Botones para agregar vértices y aristas, y ejecutar los algoritmos
tk.Button(frame_left, text="Agregar Vértice", command=agregar_vertice).pack(pady=5)
tk.Button(frame_left, text="Agregar Arista", command=agregar_arista).pack(pady=5)
tk.Button(frame_left, text="Búsqueda en Anchura", command=lambda: ejecutar_algoritmo(nx.bfs_edges)).pack(pady=5)
tk.Button(frame_left, text="Búsqueda en Profundidad", command=lambda: ejecutar_algoritmo(nx.dfs_edges)).pack(pady=5)

# Iniciar la interfaz
root.mainloop()
