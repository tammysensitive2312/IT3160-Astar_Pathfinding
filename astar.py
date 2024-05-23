import time
import heapq as heap
import convertJson as cj


def aStar(source, destination):
    open_list = []
    # giá trị g
    g_values = {}

    path = {}
    closed_list = {}

    source_id = cj.getOSMId(source[0], source[1])
    dest_id = cj.getOSMId(destination[0], destination[1])

    g_values[source_id] = 0
    # dòng tính giá trị h
    h_source = cj.calculate_heuristic(source, destination)

    open_list.append((h_source, source_id))

    s = time.time()
    while len(open_list) > 0:
        curr_state = open_list[0][1]

        # print(curr_state)
        heap.heappop(open_list)
        closed_list[curr_state] = ""

        if curr_state == dest_id:
            print("We have reached to the goal")
            print("Final path:", path)  # In ra đường đi cuối cùng
            break

        nbrs = cj.get_neighbours(curr_state, destination)
        values = nbrs[curr_state]

        for eachNeighbour in values:
            neighbour_id, neighbour_heuristic, neighbour_cost, neighbour_lat_lon = cj.get_neighbour_info(eachNeighbour)
            current_inherited_cost = g_values[curr_state] + neighbour_cost

            if neighbour_id in closed_list:
                continue
            else:
                g_values[neighbour_id] = current_inherited_cost
                neighbour_fvalue = neighbour_heuristic + current_inherited_cost
                open_list.append((neighbour_fvalue, neighbour_id))

            path[str(neighbour_lat_lon)] = {"parent": str(cj.getLatLon(curr_state)), "cost": neighbour_cost}
            print("Current path update:", path)

        open_list = list(set(open_list))
        heap.heapify(open_list)

    print("Time taken to find path(in second): " + str(time.time() - s))
    return path
