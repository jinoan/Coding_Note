# This module requires Albumentations.
# https://albumentations.ai/
# pip install -U albumentations

import random
import albumentations as A
from albumentations.core.transforms_interface import ImageOnlyTransform

def self_cut_mix(img):
    transformed_img = img.copy()
    l = random.randrange(img.shape[0] // 8, img.shape[0] // 2 + 1)
    
    # cut
    if random.choice([True, False]):
        i1 = random.randrange(l, img.shape[0] - l + 1)
        j1 = random.randrange(0, img.shape[0] - l + 1)
        i2 = random.randrange(0, i1 - l + 1)
        j2 = random.randrange(0, img.shape[0] - l + 1)
    else:
        i1 = random.randrange(0, img.shape[0] - l + 1)
        j1 = random.randrange(l, img.shape[0] - l + 1)
        i2 = random.randrange(0, img.shape[0] - l + 1)
        j2 = random.randrange(0, j1 - l + 1)
        
    p1 = img[i1:i1+l, j1:j1+l].copy()
    p2 = img[i2:i2+l, j2:j2+l].copy()
    
    # rotate piece
    random_rotate_90 = A.RandomRotate90(p=1)
    p1 = random_rotate_90(image=p1)["image"]
    p2 = random_rotate_90(image=p2)["image"]
    
    # mix
    if random.choice([True, False]):
        transformed_img[i1:i1+l, j1:j1+l] = p2
        transformed_img[i2:i2+l, j2:j2+l] = p1
    else:
        transformed_img[i1:i1+l, j1:j1+l] = p1
        transformed_img[i2:i2+l, j2:j2+l] = p2

    return transformed_img

class SelfCutMix(ImageOnlyTransform):
    def __init__(
        self,
        always_apply=False,
        p=1
    ):
        super(SelfCutMix, self).__init__(always_apply, p)
    
    def apply(self, img, **params):
        return self_cut_mix(img)