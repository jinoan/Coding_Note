import numpy as np
import pandas as pd

def iou_calc(a_box, b_box):
    # parameter format: e.g. a_box = [[x_min, y_min, x_max, y_max]]
    
    columns = ['x', 'y']
    index = ['min', 'max']
    
    # make DataFrames
    a_df = pd.DataFrame([a_box[0][:2], a_box[0][2:]], columns=columns, index=index)
    b_df = pd.DataFrame([b_box[0][:2], b_box[0][2:]], columns=columns, index=index)
    
    # concat DataFrames
    c_df = pd.concat([a_df, b_df])
    
    # check x_axis values
    xs_df = c_df.sort_values(by=['x'], axis=0)
    if xs_df.index[1] == 'max':
        print('no intersection')
        return 0.0
    
    # check y_axis values
    ys_df = c_df.sort_values(by=['y'], axis=0)
    if ys_df.index[1] == 'max':
        print('no intersection')
        return 0.0
    
    # calc iou
    intersection = (xs_df['x'][2] - xs_df['x'][1]) * (ys_df['y'][2] - ys_df['y'][1])
    a_area = (a_df['x'][1] - a_df['x'][0]) * (a_df['y'][1] - a_df['y'][0])
    b_area = (b_df['x'][1] - b_df['x'][0]) * (b_df['y'][1] - b_df['y'][0])
    union = a_area + b_area - intersection
    iou = union / intersection
    
    return a_area, b_area, intersection, union, iou