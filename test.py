import unittest
import xmltodict

from convertJson import get_neighbours, getLatLon, calculate_heuristic


def setup_module():
    global doc
    with open('data/hanoi.graphml', 'r', encoding='utf-8') as fd:
        doc = xmltodict.parse(fd.read())


class TestGetNeighbours(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_module()

    def test_get_neighbours_structure(self):
        osm_id = '75618721'
        destination_lat_lon = (21.0323034, 105.8513234)
        result = get_neighbours(osm_id, destination_lat_lon)

        self.assertIsInstance(result, dict)
        self.assertIn(osm_id, result)
        self.assertIsInstance(result[osm_id], list)

        # Kiểm tra cấu trúc và chi tiết của các node lân cận
        if result[osm_id]:
            for neighbour in result[osm_id]:
                self.assertIsInstance(neighbour, dict)
                for key, value in neighbour.items():
                    self.assertIsInstance(key, str)  # ID của node lân cận
                    self.assertIsInstance(value, list)  # Chi tiết bao gồm tọa độ, chi phí và heuristic
                    self.assertEqual(len(value), 3)
                    latlon, cost, heuristic = value
                    self.assertIsInstance(latlon, tuple)
                    self.assertIsInstance(cost, str)
                    self.assertIsInstance(heuristic, float)

    def test_get_neighbours_correctness(self):
        osm_id = '75618721'
        destination_lat_lon = (21.0323034, 105.8513234)
        result = get_neighbours(osm_id, destination_lat_lon)

        expected_target_id = '75619046'
        neighbours = result[osm_id]
        found = any(expected_target_id in nbr for nbr in neighbours)
        self.assertTrue(found, "Target ID should be in the neighbours list")

        # Để kiểm tra tính chính xác của heuristic và chi phí
        for neighbour in neighbours:
            if expected_target_id in neighbour:
                _, cost, heuristic = neighbour[expected_target_id]
                expected_cost = '64.981'  # Giả sử đây là chi phí mong đợi dựa trên dữ liệu mẫu
                self.assertEqual(cost, expected_cost)
                # Kiểm tra heuristic bằng cách gọi hàm calculate_heuristic
                latlon = getLatLon(expected_target_id)
                expected_heuristic = calculate_heuristic(latlon, destination_lat_lon)
                self.assertAlmostEqual(heuristic, expected_heuristic, places=2)

    # def test_get_LatLon(self):
    #     getLatLon()


if __name__ == '__main__':
    unittest.main()
