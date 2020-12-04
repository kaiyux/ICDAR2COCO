from ICDAR2COCO import COCOSplit

if __name__ == '__main__':
    images_dir = '/home/xiekaiyu/ocr/dataset/ICDAR2019LSVT/train_full_images'
    label_file = '/home/xiekaiyu/ocr/dataset/ICDAR2019LSVT/coco_labels.json'
    target_dir = '/home/xiekaiyu/ocr/dataset/ICDAR2019LSVT/coco'

    split = COCOSplit(images_dir, label_file, target_dir)
    split.split()
