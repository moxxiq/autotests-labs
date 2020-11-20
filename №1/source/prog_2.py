def sum_min_max(lst):
    if not lst:
        return 0
    minmax_idx = [min(range(len(lst)), key=lst.__getitem__),
                  max(range(len(lst)), key=lst.__getitem__)]
    minmax_idx.sort()
    return sum(lst[minmax_idx[0]:minmax_idx[1] + 1])
