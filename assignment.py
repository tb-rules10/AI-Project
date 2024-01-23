import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

MAX_STATIONS = 6
MAX_DISTANCE = 150

class FrequencyAssignmentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Frequency Assignment GUI")

        self.create_distance_matrix()

        self.create_widgets()

        self.graph = nx.Graph()

    def create_distance_matrix(self):
        self.distance_matrix = [
            [0, 85, 175, 200, 50, 100],
            [85, 0, 125, 175, 100, 160],
            [175, 125, 0, 100, 200, 250],
            [200, 175, 100, 0, 210, 220],
            [50, 100, 200, 210, 0, 100],
            [100, 160, 250, 220, 100, 0]
        ]

    def create_widgets(self):
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve_frequency_assignment)
        self.solve_button.pack()

        self.graph_frame = ttk.Frame(self.root)
        self.graph_frame.pack(expand=True, fill=tk.BOTH)

    def solve_frequency_assignment(self):
        self.graph.clear()
        self.create_distance_matrix()

        graph = self.build_graph()
        result = self.graph_coloring(graph)

        if result:
            num_channels = max(result)
            channel_assignment = " ".join(map(str, result))
            message = f"Number of channels needed: {num_channels}\nChannel assignment for each station: {channel_assignment}"
            self.result_label.config(text=message)

            self.plot_graph(graph, result)
        else:
            messagebox.showerror("Error", "Unable to find a solution.")

    def build_graph(self):
        graph = [[0] * MAX_STATIONS for _ in range(MAX_STATIONS)]
        for i in range(MAX_STATIONS):
            for j in range(i + 1, MAX_STATIONS):
                if self.distance_matrix[i][j] <= MAX_DISTANCE:
                    graph[i][j] = 1
                    graph[j][i] = 1
                    self.graph.add_edge(i + 1, j + 1)  # Adjust indexing to start from 1
        return graph

    def is_safe(self, station, color, graph, result):
        for i in range(MAX_STATIONS):
            if graph[station][i] and color == result[i]:
                return False
        return True

    def graph_coloring(self, graph):
        result = [0] * MAX_STATIONS
        m = 1

        while True:
            if self.graph_coloring_util(0, m, graph, result):
                return result
            m += 1

    def graph_coloring_util(self, station, m, graph, result):
        if station == MAX_STATIONS:
            return True

        for color in range(1, m + 1):
            if self.is_safe(station, color, graph, result):
                result[station] = color

                if self.graph_coloring_util(station + 1, m, graph, result):
                    return True

                result[station] = 0

        return False

    def plot_graph(self, graph, result):
        fig, ax = plt.subplots()
        pos = nx.spring_layout(self.graph)
        colors = [result[node - 1] for node in self.graph.nodes]  # Adjust indexing to start from 1

        nx.draw_networkx_nodes(self.graph, pos, node_color=colors, cmap=plt.cm.rainbow, node_size=500)
        nx.draw_networkx_labels(self.graph, pos, labels={node: str(node) for node in self.graph.nodes})  # Labels from 1 to 6
        nx.draw_networkx_edges(self.graph, pos)

        # Create an Axes for the Colorbar
        cax = fig.add_axes([0.85, 0.1, 0.02, 0.8])
        cbar = plt.colorbar(mappable=plt.cm.ScalarMappable(cmap=plt.cm.rainbow), cax=cax)
        cbar.set_label("Channel Assignment")

        plt.title("Graph Coloring for Frequency Assignment")
        plt.axis("off")

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = FrequencyAssignmentGUI(root)
    root.mainloop()
