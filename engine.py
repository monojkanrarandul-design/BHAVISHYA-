import torch
import torch.nn as nn
from torch_geometric.data import Data
from torch_geometric.nn import GATConv

class UrbanCascadingGNN(nn.Module):
    """
    Graph Attention Network (GAT) to model how localized failure 
    (e.g., flooded road or damaged transformer) propagates across urban infrastructure.
    """
    def __init__(self, in_channels=4, hidden_channels=16, out_channels=1):
        super(UrbanCascadingGNN, self).__init__()
        # Node features: [rainfall, current_load, capacity, historical_risk]
        self.gat1 = GATConv(in_channels, hidden_channels, heads=2)
        self.gat2 = GATConv(hidden_channels * 2, out_channels, heads=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x, edge_index):
        x = torch.relu(self.gat1(x, edge_index))
        x = self.gat2(x, edge_index)
        return self.sigmoid(x)

def build_mock_city_graph():
    # 4 Nodes: 0: Substation, 1: Drainage Pump, 2: Road Flyover, 3: Trauma Hospital
    # Features: [Rainfall (0-1), Load (0-1), Capacity (0-1), HistRisk (0-1)]
    x = torch.tensor([
        [0.8, 0.9, 0.4, 0.5],  # Substation under heavy rain
        [0.8, 0.7, 0.3, 0.6],  # Pump overloaded
        [0.6, 0.95, 0.2, 0.8], # Flyover near gridlock
        [0.2, 0.85, 0.5, 0.4]  # Hospital reaching max emergency load
    ], dtype=torch.float)

    # Directed dependency edges: 0 -> 1 -> 2 -> 3
    edge_index = torch.tensor([
        [0, 1, 2],
        [1, 2, 3]
    ], dtype=torch.long)

    return Data(x=x, edge_index=edge_index)

if __name__ == "__main__":
    city_graph = build_mock_city_graph()
    model = UrbanCascadingGNN()
    
    with torch.no_grad():
        node_failure_probabilities = model(city_graph.x, city_graph.edge_index)

    nodes = ["Power Substation", "Drainage Pump B", "Flyover Junction", "Trauma Hospital"]
    print("--- BHAVISHYA GNN Cascading Risk Output ---")
    for name, prob in zip(nodes, node_failure_probabilities):
        print(f"Node: {name:<20} Predicted Failure Risk: {prob.item() * 100:.1f}%")