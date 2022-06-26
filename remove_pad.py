import numpy as np

def remove_pad(img, axis=0, threshold=5):
    seq = [slice(0, s) for s in img.shape]

    # forward
    seq[axis] = (n := 0)
    while np.average(img[tuple(seq)]) < threshold:
        seq[axis] = (n := n + 1)
    
    seq[axis] = slice(n, None)
    img = img[tuple(seq)]

    # backward
    seq[axis] = (n := -1)
    while np.average(img[tuple(seq)]) < threshold:
        seq[axis] = (n := n - 1)

    if (n := n + 1) == 0:
        n = None

    seq[axis] = slice(None, n)
    img = img[tuple(seq)]

    return img