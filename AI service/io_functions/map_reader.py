from common.objectives import Objectives
from containers.grid import Grid
import numpy as np


def load_map(filepath, width, height):
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
                    weight = f.read(1)
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

    grid_obj = Grid(grid_array, width, height)

    if len(objectives) == 0:
        # lack of objective; generate randoms
        weight = 1  # need 2 agents to carry
        x, y = grid_obj.calculate_random_pos()  # pickup
        x1, y1 = x, y
        while x == x1 and y == y1:
            x1, y1 = grid_obj.calculate_random_pos()  # dropoff
        objectives[0] = Objectives((y, x), (y1, x1), weight)

    return grid_obj, objectives


def create_test_maps(map_path):
    # generate some maps for me

    for i in range(150):
        f = open("{}v{}.map".format(map_path, i), "w")
        grid, obj = load_map("{}empty.map".format(map_path), 13, 8)
        row, column = len(grid.data), len(grid.data[0])

        p_pos, d_pos = obj[0].get_pickup_pos(), obj[0].get_dropoff_pos()

        for y in range(row):
            rowContent = ""
            for x in range(column):
                if y == p_pos[0] and x == p_pos[1]:
                    rowContent += "P1"
                    x += 1
                elif y == d_pos[0] and x == d_pos[1]:
                    rowContent += "D"
                elif len(grid.data[y][x]) == 0:
                    rowContent += "."
                else:
                    rowContent += grid.data[y][x][0]

            f.write(rowContent + "\n")
        f.close()


def test_sensoric_distance_calculation(map_path):
    grid, _ = load_map("{}empty.map".format(map_path), 10, 6)
    sensoric_list = grid.get_sensoric_distance(np.array([2, 1]))

    print(sensoric_list)  # should contain north and west obstacle


if __name__ == "__main__":
    create_test_maps("../maps/normal_room/")
    # test_sensoric_distance_calculation("../maps/small_room/")
