from PIL import Image
import json
import os
from shapely.geometry import Polygon
from tqdm import tqdm
from .utils import *


class COCOConverter(object):
    def __init__(self, datasets, coco_images_dir, coco_label_file,
                 info='icdar', licenses='none', with_angle=False):
        self.datasets = datasets
        assert os.path.isdir(coco_images_dir), f'dir \'{coco_images_dir}\' not found!'
        self.coco_images_dir = coco_images_dir
        self.coco_label_file = coco_label_file

        self.data = {
            "info": info,
            "images": [],
            "annotations": [],
            "categories": [
                {
                    "id": 1,
                    "name": "text",
                    "supercategory": "foreground"
                }
            ],
            "licenses": licenses
        }

        self.with_angle = with_angle

    def add_image(self, id, width, height, filename):
        image = {
            "id": id,
            "width": width,
            "height": height,
            "file_name": filename
        }
        self.data['images'].append(image)

    def add_annotation(self, id, image_id, category_id, segmentation, area, bbox, iscrowd):
        annotation = {
            "id": id,
            "image_id": image_id,
            "category_id": category_id,
            "segmentation": segmentation,
            "area": area,
            "bbox": bbox,
            "iscrowd": iscrowd
        }
        self.data['annotations'].append(annotation)

    def convert(self):
        print('start converting...')
        ann_id = 0
        image_id = 0
        for dataset in self.datasets:
            print(f'converting {dataset.name}')

            if dataset.version == '2017':
                icdar_label_dir = dataset.label
                icdar_images_dir = dataset.images_dir
                label_files = os.listdir(icdar_label_dir)
                for label_file in tqdm(label_files):
                    label_file_path = os.path.join(icdar_label_dir, label_file)
                    skip = True
                    with open(label_file_path, 'r', encoding='utf8')as f:
                        for line in f:
                            line = line.strip()
                            iterms = line.split(',')
                            points = iterms[:8]
                            script = iterms[8]
                            transcription = iterms[9]
                            if script != 'None' and transcription != '###':
                                skip = False

                                segmentation = []
                                for point in points:
                                    segmentation.append(int(point))

                                xs = [int(points[i]) for i in range(0, len(points), 2)]
                                ys = [int(points[i]) for i in range(1, len(points), 2)]
                                xmin = min(xs)
                                xmax = max(xs)
                                ymin = min(ys)
                                ymax = max(ys)

                                width = xmax - xmin
                                height = ymax - ymin
                                bbox = [xmin, ymin, width, height]

                                points = [[xs[i], ys[i]] for i in range(len(xs))]
                                poly = Polygon(points)
                                area = round(poly.area, 2)

                                self.add_annotation(ann_id,
                                                    image_id,
                                                    category_id=1,  # text regions are foregrounds
                                                    segmentation=[segmentation],
                                                    area=area,
                                                    bbox=bbox,
                                                    iscrowd=0)
                                ann_id += 1

                    if not skip:
                        img_idx = label_file.split('_')[-1].split('.')[0]
                        image_path = os.path.join(icdar_images_dir, 'img_' + img_idx)
                        if os.path.isfile(image_path + '.jpg'):
                            im = Image.open(image_path + '.jpg')
                        elif os.path.isfile(image_path + '.png'):
                            im = Image.open(image_path + '.png').convert('RGB')
                        else:
                            raise RuntimeError(f'{img_idx}')
                        width, height = im.size
                        image_name = str(image_id) + '.jpg'
                        im.save(os.path.join(self.coco_images_dir, image_name))
                        im.close()
                        self.add_image(image_id, width, height, image_name)
                        image_id += 1

            elif dataset.version == '2019':
                icdar_label_file = dataset.label
                print(f'loading {icdar_label_file} ...')
                with open(icdar_label_file, 'r') as f:
                    icdar = json.load(f)
                print('icdar_label_file loaded')
                icdar_images_dir = dataset.images_dir
                for image_name in tqdm(icdar.keys()):
                    skip = True
                    for ann in icdar[image_name]:
                        if not ann["illegibility"]:
                            skip = False

                            segmentation = []
                            for point in ann["points"]:
                                segmentation.extend(point)

                            if self.with_angle:
                                top_left = ann["points"][0]
                                top_right = ann["points"][1]
                                bottom_right = ann["points"][2]

                                width = euc_distance(top_left, top_right)
                                height = euc_distance(top_right, bottom_right)
                                angle = azimuth_angle(top_left[0], top_left[1], top_right[0], top_right[1])
                                bbox = [top_left[0], top_left[1], width, height, angle]
                            else:
                                xmin = float('inf')
                                xmax = 0
                                ymin = float('inf')
                                ymax = 0
                                for point in ann["points"]:
                                    xmin = min(xmin, point[0])
                                    xmax = max(xmax, point[0])
                                    ymin = min(ymin, point[1])
                                    ymax = max(ymax, point[1])

                                width = xmax - xmin
                                height = ymax - ymin
                                bbox = [xmin, ymin, width, height]

                            poly = Polygon(ann["points"])
                            area = round(poly.area, 2)

                            self.add_annotation(ann_id,
                                                image_id,
                                                category_id=1,  # text regions are foregrounds
                                                segmentation=[segmentation],
                                                area=area,
                                                bbox=bbox,
                                                iscrowd=0)
                            ann_id += 1

                    if not skip:
                        image_name += '.jpg'
                        image_path = os.path.join(icdar_images_dir, image_name)
                        assert os.path.isfile(image_path), f'image {image_name} not found in {icdar_images_dir}'
                        im = Image.open(image_path)
                        width, height = im.size
                        image_name = str(image_id) + '.jpg'
                        im.save(os.path.join(self.coco_images_dir, image_name))
                        im.close()
                        self.add_image(image_id, width, height, image_name)
                        image_id += 1

        with open(self.coco_label_file, 'w')as f:
            json.dump(self.data, f)
        # print(self.data)
        print(f'Done. {image_id + 1} images totally.')
