import time
from haversine import haversine
import xmltodict
import numpy as np
from sklearn.neighbors import KDTree

s = time.time()
doc = {}
with open('data/hanoi_graph.graphml', 'r', encoding='utf-8') as fd:
    doc = xmltodict.parse(fd.read())
print(time.time() - s)

"""lấy dữ liệu(kinh độ và vĩ độ) dựa vào osmid """


def getLatLon(OSMId):
    lat, lon = 0, 0
    nodes = doc['graphml']['graph']['node']
    for eachNode in range(len(nodes)):
        if nodes[eachNode]["@id"] == str(OSMId):
            lat = float(nodes[eachNode]["data"][0]["#text"])
            lon = float(nodes[eachNode]["data"][1]["#text"])
    return lat, lon


""" lấy ra id của node trong file graphml """


def getOSMId(lat, lon):
    nodes = doc['graphml']['graph']['node']
    for node in nodes:
        # Giả định rằng d4 là key cho latitude và d5 là key cho longitude
        node_lat = next((data['#text'] for data in node['data'] if data['@key'] == 'd4'), None)
        node_lon = next((data['#text'] for data in node['data'] if data['@key'] == 'd5'), None)

        if str(node_lat) == str(lat) and str(node_lon) == str(lon):
            return node['@id']
    return 0


# hàm định giá bằng công thức haversine
def calculate_heuristic(curr, destination):
    return haversine(curr, destination)


# hàm tính node lân cận
def get_neighbours(OSMId, destination_lat_lon):
    neighbour_dict = {}
    temp_list = []
    edges = doc['graphml']['graph']['edge']
    for eachEdge in range(len(edges)):
        if edges[eachEdge]["@source"] == str(OSMId):
            temp_nbr = {}

            neighbour_cost = 0
            neighbour_id = edges[eachEdge]["@target"]
            neighbour_lat_lon = getLatLon(neighbour_id)

            data_points = edges[eachEdge]["data"]
            for eachData in range(len(data_points)):
                # key data cho cost
                if data_points[eachData]["@key"] == "d13":
                    neighbour_cost = data_points[eachData]["#text"]

            neighbor_heuristic = calculate_heuristic(neighbour_lat_lon, destination_lat_lon)

            temp_nbr[neighbour_id] = [neighbour_lat_lon, neighbour_cost, neighbor_heuristic]
            temp_list.append(temp_nbr)

    neighbour_dict[OSMId] = temp_list
    return neighbour_dict


# lấy ra thông tin các nút lân cận
def get_neighbour_info(neighbour_dict):
    neighbour_id = 0
    neighbour_heuristic = 0
    neighbour_cost = 0
    for key, value in neighbour_dict.items():
        neighbour_id = key
        neighbour_heuristic = float(value[2])
        neighbour_cost = float(value[1]) / 1000
        neighbour_lat_lon = value[0]

    return neighbour_id, neighbour_heuristic, neighbour_cost, neighbour_lat_lon


# def initialize_kdtree(nodes):
#     locations = [(float(node["data"][0]["#text"]), float(node["data"][1]["#text"])) for node in nodes]
#     locations_arr = np.array(locations, dtype=np.float32)
#     return KDTree(locations_arr)


def get_KNN(point_location):
    nodes = doc["graphml"]["graph"]["node"]
    locations = []
    for eachNode in range(len(nodes)):
        locations.append((nodes[eachNode]["data"][0]["#text"], nodes[eachNode]["data"][1]["#text"]))

    locations_arr = np.asarray(locations, dtype=np.float32)
    point = np.asarray(point_location, dtype=np.float32)

    tree = KDTree(locations_arr, leaf_size=2)
    dist, ind = tree.query(point.reshape(1, -1), k=6)

    nearest_neighbour_loc = (float(locations[ind[0][0]][0]), float(locations[ind[0][0]][1]))

    return nearest_neighbour_loc


# def get_nearest_node(kdtree, point_location):
#     point = np.array([point_location], dtype=np.float32)
#     dist, ind = kdtree.query(point, k = 1)
#     nearest_node_index = ind[0][0]
#     return kdtree.data[nearest_node_index]

# lấy ra các node ở trên đường đi từ source -> destination, trả về một từ điển
def get_response_path_dict(paths, source, destination):
    final_path = []
    child = destination
    parent = ()
    cost = 0
    while parent != source:
        temp_dict = {}
        try:
            # print(f"Current child: {child}")
            # print(f"Available keys in paths: {list(paths.keys())}")
            cost = cost + float(paths[str(child)]["cost"])
        except KeyError:
            print(f"Key error with child: {child}")
            # Optionally, handle the error or default the cost.

        parent = paths[str(child)]["parent"]
        parent = tuple(float(x) for x in parent.strip('()').split(','))

        temp_dict["lat"] = parent[0]
        temp_dict["lng"] = parent[1]

        final_path.append(temp_dict)
        child = parent

    return final_path, cost
