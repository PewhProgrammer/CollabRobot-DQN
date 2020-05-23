from common.objectives import Objectives


def load_map(filepath, width, height):
    grid = [[[] for x in range(width)] for y in range(height)]

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
                    grid[i][j] = [c]

        for i in range(pickups):
            if "dropoff" in obj_storage:
                y, x, weight = obj_storage[i]
                objectives[i] = (Objectives((y, x), obj_storage["dropoff"], weight))

        # print("End of file")

    return grid, objectives


if __name__ == "__main__":
    load_map('../maps/sample_easy.map')
