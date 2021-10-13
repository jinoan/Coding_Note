import os
import cv2
import xml.etree.ElementTree as ET

def cvat2labelimg(img_dir='./images', cvat_xml='./annotations.xml', res_dir='result', res_size=None):
    # make dir
    res = res_dir
    i = 1
    while os.path.isdir(res):
        i += 1
        res = f"{res_dir.lstrip('/')}_{i}"
    os.mkdir(res)
    os.mkdir(os.path.join(res, 'images'))
    os.mkdir(os.path.join(res, 'xmls'))

    # get boxes
    tree = ET.parse(cvat_xml)
    root = tree.getroot()
    track = root.find('track')
    label = track.get('label')
    boxes = track.findall('box')

    # get image size
    src_size = root.find('meta').find('task').find('original_size')
    src_size = (int(src_size.find('height').text), int(src_size.find('width').text))
    if res_size is None:
        res_size = src_size

    for box in boxes:
        frame_no = box.get('frame')
        frame_name = 'frame_' + frame_no.zfill(6)
        print(frame_name, end=' ')

        img_file = frame_name + '.PNG'

        # resize image
        if not os.path.isfile(os.path.join(res, 'images', img_file)):
            img = cv2.imread(os.path.join(img_dir, img_file))
            img = resize_img(img, src_size, res_size)
            cv2.imwrite(os.path.join(res, 'images', img_file), img)  # save resized image
        else:
            img = cv2.imread(os.path.join(res, 'images', img_file))

        # resize box
        xtl = float(box.get('xtl'))
        ytl = float(box.get('ytl'))
        xbr = float(box.get('xbr'))
        ybr = float(box.get('ybr'))
        box = [xtl, ytl, xbr, ybr]
        box = resize_box(box, src_size, res_size)
        
        # save box
        xml_file = frame_name + '.xml'
        if not os.path.isfile(os.path.join(res, 'xmls', xml_file)):
            root = ET.Element('annotation')
            folder = ET.SubElement(root, 'folder')
            folder.text = os.path.dirname(res)
            filename = ET.SubElement(root, 'filename')
            filename.text = img_file
            path = ET.SubElement(root, 'path')
            path.text = os.path.abspath(os.path.join(res, 'images', img_file))
            source = ET.SubElement(root, 'source')
            database = ET.SubElement(source, 'database')
            database.text = 'Unknown'
            size = ET.SubElement(root, 'size')
            width = ET.SubElement(size, 'width')
            width.text = str(res_size[1])
            height = ET.SubElement(size, 'height')
            height.text = str(res_size[0])
            depth = ET.SubElement(size, 'depth')
            depth.text = '3'
            segmented = ET.SubElement(root, 'segmented')
            segmented.text = '0'
        else:
            tree = ET.parse(os.path.join(res, 'xmls', xml_file))
            root = tree.getroot()
        obj = ET.SubElement(root, 'object')
        name = ET.SubElement(obj, 'name')
        name.text = label
        pose = ET.SubElement(obj, 'pose')
        pose.text = 'Unspecified'
        truncated = ET.SubElement(obj, 'truncated')
        truncated.text = '0'
        difficult = ET.SubElement(obj, 'difficult')
        difficult.text = '0'
        bndbox = ET.SubElement(obj, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(box[0])
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(box[1])
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(box[2])
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(box[3])
        tree = ET.ElementTree(root)
        tree.write(os.path.join(res, 'xmls', xml_file))
        
        print('done')

    print('finish!')
        
def resize_img(img, src_size, res_size):
    # resize image
    if src_size[0] == res_size[0] and src_size[1] == res_size[1]:
        return img
    if src_size[0] > res_size[0] and src_size[1] > res_size[1]:
        inter = cv2.INTER_AREA
    elif src_size[0] < res_size[0] and src_size[1] < res_size[0]:
        inter = cv2.INTER_LINEAR
    else:
        inter = cv2.INTER_CUBIC
    img = cv2.resize(img, res_size, interpolation=inter)
    return img

def resize_box(box, src_size, res_size):
    # resize box
    if src_size[0] != res_size[0] or src_size[1] != res_size[1]:
        box[0] *= res_size[1] / src_size[1]
        box[1] *= res_size[0] / src_size[0]
        box[2] *= res_size[1] / src_size[1]
        box[3] *= res_size[0] / src_size[0]
    box[0] = int(box[0] + 0.5)
    box[1] = int(box[1] + 0.5)
    box[2] = int(box[2] + 0.5)
    box[3] = int(box[3] + 0.5)
    return box

if __name__ == '__main__':
    import argparse
    import ast

    parser = argparse.ArgumentParser(description="Convert CVAT data form to Labelimg data form.")
    parser.add_argument('--img-dir', '-i', type=str, default='./images', help="A directory containing image files")
    parser.add_argument('--cvat-xml', '-c', type=str, default='./annotations.xml', help="'CVAT for video' form annotation xml file")
    parser.add_argument('--res-dir', '-r', type=str, default='./result', help="A directory to load processed dataset")
    parser.add_argument('--img-size', '-s', type=str, default=None, help="Result image size. Write like '(128, 128)'")
    args = parser.parse_args()

    cvat2labelimg(args.img_dir, args.cvat_xml, args.res_dir, ast.literal_eval(args.img_size))
