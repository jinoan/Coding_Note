import os
import cv2
import numpy as np

###### config your path ######
src_path = "data/empty2/"
save_path = "data/processed/"
##############################

src_files = os.listdir(src_path)
srcs = [cv2.imread(os.path.join(src_path, f)) for f in src_files]
box = [None, None]
boxes = [[] for _ in range(len(srcs))]
src_idx = 0
box_idx = 0

def show_box(show_target=True):
    img = srcs[src_idx].copy()
    for i, v in enumerate(boxes[src_idx]):
        if i != box_idx:
            img = cv2.rectangle(img, v[0], v[1], (255, 0, 0), 2)
    if show_target:
        if 0 <= box_idx < len(boxes[src_idx]):
            v = boxes[src_idx][box_idx]
            img = cv2.rectangle(img, v[0], v[1], (0, 0, 255), 2)
    cv2.imshow("img", img)
    return img

def on_mouse(event, x, y, flags, srcs):
    global box, boxes, src_idx, box_idx
    img = show_box()
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(boxes[src_idx]) > 0:
            box_idx += 1
        box[0] = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        box[1] = (x, y)
        if box_idx == len(boxes[src_idx]):
            boxes[src_idx].append(box.copy())
        else:
            boxes[src_idx][box_idx] = box.copy()
        img = show_box()
    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:
            img = show_box(False)
            img = cv2.rectangle(img, box[0], (x, y), (0, 0, 255), 2)
            cv2.imshow("img", img)

def draw_box():
    global src_idx, box_idx, boxes
    cv2.namedWindow("img")
    cv2.setMouseCallback("img", on_mouse, srcs)
    while src_idx < len(srcs):
        show_box()
        key = cv2.waitKey(0)
        if key == ord("s"):
            if src_idx > 0:
                src_idx -= 1
                box_idx = 0
        elif key == 13 or key == ord("w"):
            src_idx += 1
            box_idx = 0
        elif key == ord("a"):
            if box_idx > 0:
                box_idx -= 1
        elif key == ord("d"):
            if box_idx < len(boxes[src_idx])-1:
                box_idx += 1
        elif key == 8:
            if len(boxes[src_idx]) > 0:
                boxes[src_idx].pop(box_idx)
                if box_idx > 0:
                    box_idx -= 1
        elif key == 27:  # esc
            break

    cv2.destroyAllWindows()

def crop_box():
    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    for i, (src, box) in enumerate(zip(srcs, boxes)):
        prefix, suffix = src_files[i].split(".")
        for j, v in enumerate(box):
            crop = src[v[0][1]:v[1][1], v[0][0]:v[1][0], :]
            fname = prefix + f"_{j}." + suffix
            cv2.imwrite(os.path.join(save_path, fname), crop)

if __name__ == "__main__":
    draw_box()
    crop_box()