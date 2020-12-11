from PIL import Image
import json
import os
from shapely.geometry import Polygon
from tqdm import tqdm
from .utils import *


class COCOConverter(object):
    def __init__(self, icdar_label_file, icdar_images_dir, coco_label_file, info='icdar', licenses='none',
                 with_angle=False):
        assert os.path.isfile(icdar_label_file), f'file \'{icdar_label_file}\' not found!'
        print(f'loading {icdar_label_file} ...')
        with open(icdar_label_file, 'r') as f:
            self.icdar = json.load(f)
            # print(self.icdar)
        print('icdar_label_file loaded')

        assert os.path.isdir(icdar_images_dir), f'dir \'{icdar_images_dir}\' not found!'
        self.icdar_images_dir = icdar_images_dir

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
        for index, image_name in tqdm(enumerate(self.icdar.keys())):
            skip = True
            for ann in self.icdar[image_name]:
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
                                        index,
                                        category_id=1,  # text regions are foregrounds
                                        segmentation=[segmentation],
                                        area=area,
                                        bbox=bbox,
                                        iscrowd=0)
                    ann_id += 1

            if skip:
                continue

            image_name += '.jpg'
            image_path = os.path.join(self.icdar_images_dir, image_name)
            assert os.path.isfile(image_path), f'image {image_name} not found in {self.icdar_images_dir}'
            im = Image.open(image_path)
            width, height = im.size
            im.close()
            self.add_image(index, width, height, image_name)

        with open(self.coco_label_file, 'w')as f:
            json.dump(self.data, f)
        # print(self.data)
        print('done')
