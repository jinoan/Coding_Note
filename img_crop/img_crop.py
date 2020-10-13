# -*- coding:utf-8 -*-

from PIL import Image
import pandas as pd
import os

                    
class Crop:
    def __init__(self, image, boxes, labels, resize=None):
        self.original = image
        images = list(map(lambda b : image.crop(b), boxes))
        if str(type(resize)) == "<class 'tuple'>":
            images = list(map(lambda i : i.resize(resize), images))
        self.crop_table = pd.DataFrame({'image': images, 'label': labels, 'box': boxes})
        
            
    
    def save(self, path):
        og_file = os.path.basename(self.original.filename)
        self.__check_folder_exists(path)
        table_path = os.path.join(path, 'crop_table.csv')
        if not os.path.exists(table_path):
            pd.DataFrame({'image':[], 'label':[], 'box':[]}).to_csv(table_path, header=True, index_label=False)
        
        file = open(table_path, mode='a')
        for idx in self.crop_table.index:
            img = self.crop_table.loc[idx, 'image']
            lb = self.crop_table.loc[idx, 'label']
            pth = os.path.join(path, lb)
            self.__check_folder_exists(pth)
            img_path = os.path.join(pth, f'({lb}).jpg'.join(og_file.split('.jpg')))
            img.save(img_path, 'JPEG')
            ct = self.crop_table.loc[self.crop_table['label'] == lb, 'label':]
            ct['image'] = [img_path]
            ct = pd.DataFrame(ct, columns=['image', 'label', 'box'])
            
            ct.to_csv(file, mode='a', header=False, index=False, index_label=False)
        file.close()
        
    #file check function
    def __check_folder_exists(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print ('create ' + path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
