from common.objectives import Objectives
from containers.grid import Grid
import numpy as np


def load_map(filepath, width, height, w=1, mode=1):
    grid_array = [[[] for x in range(width)] for y in range(height)]

    objectives = {}
    obj_storage = {}
    pickups = 0

    # only obstacles will be loaded
    with open(filepath) as f:
        for i in range(height):
            for j in range(width):
                c = f.read(1)

                if '\n' in c:
                    c = f.read(1)

                if 'D' in c:
                    obj_storage["dropoff"] = (i, j)

                if 'P' in c:
                    # discard read weight
                    f.read(1)
                    weight = w  # f.read(1)
                    c += str(pickups)
                    obj_storage[pickups] = (i, j, int(weight))
                    pickups += 1

                if '.' in c or '-' in c:
                    continue

                if '#' in c:
                    grid_array[i][j] = [c]

        for i in range(pickups):
            if "dropoff" in obj_storage:
                y, x, weight = obj_storage[i]
                objectives[i] = (Objectives((y, x), obj_storage["dropoff"], weight))

        # print("End of file")

    grid_obj = Grid(grid_array, width, height, obstacle_lane=mode == 6)

    if mode == 6:
        # obstacle lane
        objectives = spawn_target_at_end(width, height)
    else:
        if len(objectives) == 0:
            objectives[0] = spawn_objectives_randomly(grid_obj, w)

    return grid_obj, objectives


def spawn_target_at_end(width, height):
    # lack of objective; generate randoms
    results = {}
    weight = 1
    # generate target at the end of the map
    for i in range(height - 2):
        results[i] = Objectives((-1, -1), (i + 1, width - 2), weight)
    return results


def spawn_objectives_randomly(grid_obj, w):
    # lack of objective; generate randoms
    weight = w  # need 2 agents to carry
    x, y = grid_obj.calculate_random_pos()  # pickup
    x1, y1 = x, y
    while x == x1 and y == y1:
        x1, y1 = grid_obj.calculate_random_pos()  # dropoff
    return Objectives((y, x), (y1, x1), weight)


def create_test_maps(map_path, w, h):
    # generate some maps for me

    for i in range(150):
        f = open("{}v{}.map".format(map_path, i), "w")
        grid, obj = load_map("{}empty.map".format(map_path), w, h, w=1, mode=6)
        row, column = len(grid.data), len(grid.data[0])

        p_pos, d_pos = obj[0].get_pickup_pos(), obj[0].get_dropoff_pos()

        for y in range(row):
            rowContent = ""
            for x in range(column):
                no_objectives_placed = True
                for i, value in obj.items():
                    d_y, d_x = value.get_dropoff_pos()
                    if y == p_pos[0] and x == p_pos[1]:
                        rowContent += "P1"
                        x += 1
                        no_objectives_placed = False
                    elif y == d_y and x == d_x:
                        rowContent += "D"
                        no_objectives_placed = False
                if len(grid.data[y][x]) == 0 and no_objectives_placed:
                    rowContent += "."
                elif no_objectives_placed:
                    rowContent += grid.data[y][x][0]

            f.write(rowContent + "\n")
        f.close()


def test_sensoric_distance_calculation(map_path):
    grid, _ = load_map("{}empty.map".format(map_path), 10, 6)
    sensoric_list = grid.get_sensoric_distance(np.array([2, 1]))

    print(sensoric_list)  # should contain north and west obstacle


if __name__ == "__main__":
    create_test_maps("../maps/obstacle_lane/", 16, 5)
    # test_sensoric_distance_calculation("../maps/small_room/")
