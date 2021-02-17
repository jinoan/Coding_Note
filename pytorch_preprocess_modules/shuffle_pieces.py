# This module requires Albumentations.
# https://albumentations.ai/
# pip install -U albumentations

import random
import albumentations as A
from albumentations.core.transforms_interface import ImageOnlyTransform

def shuffle_pieces(img, num_pieces: list):
    n = random.choice(num_pieces)
    transformed_img = img.copy()
    l = img.shape[0] // n
    pieces = [transformed_img[h:h+l, w:w+l].copy() for h in range(0, n*l, l) for w in range(0, n*l, l)]
    random.shuffle(pieces)
    random_rotate_90 = A.RandomRotate90(p=1)
    for i, h in enumerate(range(0, n*l, l)):
        for j, w in enumerate(range(0, n*l, l)):
            transformed_img[h:h+l, w:w+l] = random_rotate_90(image=pieces[i*n+j])["image"]
    return transformed_img

class ShufflePieces(ImageOnlyTransform):
    def __init__(
        self,
        always_apply=False,
        num_pieces=[4],
        p=1
    ):
        super(ShufflePieces, self).__init__(always_apply, p)
        self.num_pieces = num_pieces
    
    def apply(self, img, **params):
        return shuffle_pieces(img, self.num_pieces)