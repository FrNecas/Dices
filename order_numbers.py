var = [1, 5, 5, 6, 4, 3]


def find_index():
    results = []
    for index, number in enumerate(var):
        if number == 5:
            results.append(index)
    for index, result in enumerate(results):
        var[result], var[5 - index] = var[5 - index], var[result]

find_index()
print(var)
