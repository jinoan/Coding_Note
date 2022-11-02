def find_indices(lst, tg):
    indices = []
    i = -1
    while True:
        try:
            i = lst.index(tg, i+1)
        except ValueError:
            break
        indices.append(i)
    return indices