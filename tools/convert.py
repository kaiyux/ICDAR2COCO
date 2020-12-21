from ICDAR2COCO import COCOConverter

if __name__ == "__main__":
    icdar_label_file = [
        '/home/xiekaiyu/ocr/dataset/ICDAR2019LSVT/train_full_labels.json',
        '/home/xiekaiyu/ocr/dataset/ICDAR2019ArT/train_labels.json',
    ]
    icdar_images_dir = [
        '/home/xiekaiyu/ocr/dataset/ICDAR2019LSVT/train_full_images',
        '/home/xiekaiyu/ocr/dataset/ICDAR2019ArT/train_images',
    ]
    coco_images_dir = '/home/xiekaiyu/ocr/dataset/ICDAR2COCO/train_images'
    coco_label_file = '/home/xiekaiyu/ocr/dataset/ICDAR2COCO/coco_labels.json'

    converter = COCOConverter(icdar_label_file, icdar_images_dir, coco_images_dir, coco_label_file)
    converter.convert()
