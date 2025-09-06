def calc_pos(n, w, ind):
    f = 1280-ind*2-w*n
    arr = [ind]
    for i in range(n-1):
        arr.append(arr[-1]+w+f//(n-1))
    return arr
