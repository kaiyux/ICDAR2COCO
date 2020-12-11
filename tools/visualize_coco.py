import os
import json
from PIL import Image, ImageDraw


def xywh2xyxy(x, y, w, h):
    ul = (x, y)
    ur = (x + w, y)
    br = (x + w, y + h)
    bl = (x, y + h)
    return ul, ur, br, bl


if __name__ == '__main__':
    label_file = '/home/xiekaiyu/ocr/dataset/ICDAR2019ArT/coco_labels.json'
    image_file = '/home/xiekaiyu/ocr/dataset/ICDAR2019ArT/train_images/gt_0.jpg'
    visualize_result = '/home/xiekaiyu/ocr/visualize.jpg'

    assert os.path.isfile(label_file), f'file \'{label_file}\' not found!'
    assert os.path.isfile(image_file), f'file \'{image_file}\' not found!'

    image_name = image_file.split('/')[-1]
    print(f'image_name: {image_name}')

    print(f'loading {label_file} ...')
    with open(label_file, 'r') as f:
        coco = json.load(f)
    print('label_file loaded')

    filename2id = {}
    for image in coco['images']:
        filename2id[image['file_name']] = image['id']

    segs = []
    bboxs = []

    for ann in coco['annotations']:
        if ann['image_id'] == filename2id[image_name]:
            segs.extend(ann['segmentation'])
            bboxs.append(ann['bbox'])

    print(f'{len(bboxs)} bboxs')
    print(segs)
    print(bboxs)

    im = Image.open(image_file)
    draw = ImageDraw.Draw(im)

    for bbox in bboxs:
        x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
        coord = xywh2xyxy(x, y, w, h)
        draw.line((coord[0][0], coord[0][1], coord[1][0], coord[1][1]), fill=(255, 0, 0), width=5)
        draw.line((coord[1][0], coord[1][1], coord[2][0], coord[2][1]), fill=(255, 0, 0), width=5)
        draw.line((coord[2][0], coord[2][1], coord[3][0], coord[3][1]), fill=(255, 0, 0), width=5)
        draw.line((coord[3][0], coord[3][1], coord[0][0], coord[0][1]), fill=(255, 0, 0), width=5)

    for seg in segs:
        i = 0
        while i + 2 < len(seg):
            draw.line((seg[i], seg[i + 1], seg[i + 2], seg[i + 3]), fill=(0, 255, 0), width=5)
            i += 2
        draw.line((seg[i], seg[i + 1], seg[0], seg[1]), fill=(0, 255, 0), width=5)

    im.save(visualize_result)
    print(f'result saved to {visualize_result}')
