import os
import json
from PIL import Image, ImageDraw

if __name__ == '__main__':
    label_file = '/home/xiekaiyu/ocr/dataset/ICDAR2019LSVT/train_full_labels.json'
    image_file = '/home/xiekaiyu/ocr/dataset/ICDAR2019LSVT/train_full_images/gt_0.jpg'
    visualize_result = '/home/xiekaiyu/ocr/visualize.jpg'

    assert os.path.isfile(label_file), f'file \'{label_file}\' not found!'
    assert os.path.isfile(image_file), f'file \'{image_file}\' not found!'

    image_name = '.'.join((image_file.split('/')[-1]).split('.')[:-1])
    print(f'image_name: {image_name}')

    print(f'loading {label_file} ...')
    with open(label_file, 'r') as f:
        icdar = json.load(f)
    print('label_file loaded')

    im = Image.open(image_file)
    draw = ImageDraw.Draw(im)

    for bbox in icdar[image_name]:
        bbox = bbox['points']
        draw.line((bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]), fill=(255, 0, 0), width=5)
        draw.line((bbox[1][0], bbox[1][1], bbox[2][0], bbox[2][1]), fill=(255, 0, 0), width=5)
        draw.line((bbox[2][0], bbox[2][1], bbox[3][0], bbox[3][1]), fill=(255, 0, 0), width=5)
        draw.line((bbox[3][0], bbox[3][1], bbox[0][0], bbox[0][1]), fill=(255, 0, 0), width=5)

    im.save(visualize_result)
    print(f'result saved to {visualize_result}')
