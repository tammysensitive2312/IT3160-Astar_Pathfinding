import osmnx as ox
import networkx as nx
from shapely.wkt import loads


# " lớp để trích xuất dữ liệu từ osm (dạng file .osm.pbf) sử dụng osmnx\n"
# """xuất dữ liệu dưới dạng file nhẹ và dữ xử lý hơn .graphml dạng file """
class CityGraph:
    def __init__(self, city_name):
        self.city_name = city_name
        self.graph = None

    def download_graph(self):
        """Download the street network graph of the city using OSMnx."""
        self.graph = ox.graph_from_address(self.city_name, network_type='drive', simplify=True)

    def clean_graph(self):
        """Convert unsupported data types."""
        for u, v, data in self.graph.edges(data=True):
            for key in list(data):
                if isinstance(data[key], list):  # Check if the attribute is a list
                    # Convert list to string or remove it
                    data[key] = ', '.join(map(str, data[key]))
                elif hasattr(data[key], '__geo_interface__'):  # Check for Shapely geometries
                    data[key] = str(data[key])
        for node, data in self.graph.nodes(data=True):
            for key in list(data):
                if isinstance(data[key], list):  # Same check for nodes
                    data[key] = ', '.join(map(str, data[key]))

    def restore_geometry(self):
        """Restore geometry objects from WKT strings for visualization."""
        for u, v, data in self.graph.edges(data=True):
            for key in list(data):
                if isinstance(data[key], str) and data[key].startswith('LINESTRING'):
                    data[key] = loads(data[key])

    def save_graph(self, file_path):
        """Save the graph to a GraphML file."""
        self.clean_graph()  # Clean the graph before saving
        nx.write_graphml(self.graph, file_path)

    def display_graph(self):
        """Display the graph using OSMnx built-in plot function."""
        self.restore_geometry()
        ox.plot_graph(self.graph, figsize=(12, 12), node_size=0, edge_linewidth=1, edge_color='#2a2a2a')


if __name__ == "__main__":
    # hanoi_graph = ox.graph_from_address('Hanoi, Vietnam')
    # ox.plot_graph(hanoi_graph)

    city_graph = CityGraph("Nam Dinh, Vietnam")
    city_graph.download_graph()
    file_path = 'data/namdinh.graphml'
    city_graph.save_graph(file_path)
    city_graph.display_graph()
    print(f"Graph has been saved to {file_path}")
