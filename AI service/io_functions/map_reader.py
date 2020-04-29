from common.objectives import Objectives


def load_map(filepath, width, height):
    grid = [[[] for x in range(width)] for y in range(height)]

    objectives = {}
    obj_storage = [[] for x in range(10)]

    with open(filepath) as f:
        for i in range(height):
            for j in range(width):
                c = f.read(1)

                if '\n' in c:
                    c = f.read(1)

                if 'P' in c or 'D' in c:
                    id = f.read(1)
                    c += id
                    num = int(id)
                    if len(obj_storage[num]) > 0:
                        # there already exists a the partner dropoff object
                        if 'P' in c:
                            objectives[num] = (Objectives((i, j), obj_storage[num]))
                        else:
                            objectives[num] = (Objectives(obj_storage[num], (i, j)))
                    else:
                        obj_storage[num] = (i, j)

                if '.' in c or '-' in c:
                    continue

                grid[i][j] = [c]

        # print("End of file")

    return grid, objectives


if __name__ == "__main__":
    load_map('../maps/sample_easy.map')
