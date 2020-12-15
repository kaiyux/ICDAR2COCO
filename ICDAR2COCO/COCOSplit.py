import os
import json
from tqdm import tqdm
import shutil


class COCOSplit(object):
    def __init__(self, images_dir, label_file, target_dir, train=8, test=1, val=1, ratio_mode=True):
        assert os.path.isfile(label_file), f'file \'{label_file}\' not found!'
        print(f'loading {label_file} ...')
        with open(label_file, 'r') as f:
            self.coco = json.load(f)
        print('label_file loaded')

        assert os.path.isdir(images_dir), f'dir \'{images_dir}\' not found!'
        self.images_dir = images_dir

        assert not os.path.exists(target_dir), f'target_dir {target_dir} exists!'

        annotations_dir = os.path.join(target_dir, 'annotations')
        self.train_dir = os.path.join(target_dir, 'train')
        self.test_dir = os.path.join(target_dir, 'test')
        self.val_dir = os.path.join(target_dir, 'val')
        dirs = [annotations_dir, self.train_dir, self.test_dir, self.val_dir]
        print('create dir:')
        for d in dirs:
            print(d)
            os.makedirs(d)

        self.train_label = os.path.join(annotations_dir, 'train.json')
        self.test_label = os.path.join(annotations_dir, 'test.json')
        self.val_label = os.path.join(annotations_dir, 'val.json')
        print('labels will be saved into:')
        print(self.train_label)
        print(self.test_label)
        print(self.val_label)
        self.target_dir = target_dir

        self.ratio_mode = ratio_mode
        if ratio_mode:
            num = train + test + val
            self.train = train / num
            self.test = test / num
            self.val = val / num
        else:
            self.train = train
            self.test = test
            self.val = val

    def get_images_dir(self, mode):
        dir_dict = {
            'train': self.train_dir,
            'test': self.test_dir,
            'val': self.val_dir
        }
        return dir_dict[mode]

    def split(self):
        if self.ratio_mode:
            num_images = len(self.coco['images'])
            num_trainset = int(num_images * self.train)
            num_testset = int(num_images * self.test)
            num_valset = int(num_images * self.val)
        else:
            num_images = self.train + self.test + self.val
            num_trainset = self.train
            num_testset = self.test
            num_valset = self.val

        print(f'{num_images} images in label file')
        print(f'train set: {num_trainset}')
        print(f'test set: {num_testset}')
        print(f'val set: {num_valset}')

        images = []
        annotations = []
        image_id = 0
        ann_id = 0
        mode = 'train'

        # use dict to speed up
        mem = {}
        for index, ann in enumerate(self.coco["annotations"]):
            if ann['image_id'] in mem.keys():
                mem[ann['image_id']].append(index)
            else:
                mem[ann['image_id']] = [index]

        for i, img in tqdm(enumerate(self.coco['images'])):
            image = img.copy()

            file_name = image['file_name']

            shutil.copy(os.path.join(self.images_dir, file_name), self.get_images_dir(mode))

            image['id'] = image_id
            images.append(image)

            for index in mem[img['id']]:
                annotation = self.coco["annotations"][index].copy()
                annotation['id'] = ann_id
                annotation['image_id'] = image_id
                annotations.append(annotation)
                ann_id += 1

            image_id += 1

            if i == num_trainset - 1:
                data = {
                    "info": self.coco['info'],
                    "images": images,
                    "annotations": annotations,
                    "categories": self.coco['categories'],
                    "licenses": self.coco['licenses']
                }
                with open(self.train_label, 'w')as f:
                    json.dump(data, f)
                    print('train_label saved')

                images = []
                annotations = []
                image_id = 0
                ann_id = 0
                mode = 'test'
            elif i == num_trainset + num_testset - 1:
                data = {
                    "info": self.coco['info'],
                    "images": images,
                    "annotations": annotations,
                    "categories": self.coco['categories'],
                    "licenses": self.coco['licenses']
                }
                with open(self.test_label, 'w')as f:
                    json.dump(data, f)
                    print('test_label saved')

                images = []
                annotations = []
                image_id = 0
                ann_id = 0
                mode = 'val'
            elif i == num_images - 1:
                data = {
                    "info": self.coco['info'],
                    "images": images,
                    "annotations": annotations,
                    "categories": self.coco['categories'],
                    "licenses": self.coco['licenses']
                }
                with open(self.val_label, 'w')as f:
                    json.dump(data, f)
                    print('val_label saved')

                return
