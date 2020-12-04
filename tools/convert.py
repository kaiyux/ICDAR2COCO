from ICDAR2COCO import COCOConverter

if __name__ == "__main__":
    icdar_label_file = '/home/xiekaiyu/workspace/ICDAR2COCO/example/example.json'
    icdar_images_dir = '/home/xiekaiyu/ocr/dataset/ICDAR2019ArT/train_images'
    coco_label_file = '/home/xiekaiyu/workspace/ICDAR2COCO/example/output.json'

    converter = COCOConverter(icdar_label_file, icdar_images_dir, coco_label_file)
    converter.convert()
