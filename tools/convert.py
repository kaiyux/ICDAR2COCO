from ICDAR2COCO import Dataset, COCOConverter

if __name__ == "__main__":
    icdar_2017_mlt = Dataset('icdar_2017_mlt', '2017',
                             '/home/xiekaiyu/ocr/dataset/ICDAR2017MLT/train_gt',
                             '/home/xiekaiyu/ocr/dataset/ICDAR2017MLT/train')
    icdar_2019_lsvt = Dataset('icdar_2019_lsvt', '2019',
                              '/home/xiekaiyu/ocr/dataset/ICDAR2019LSVT/train_full_labels.json',
                              '/home/xiekaiyu/ocr/dataset/ICDAR2019LSVT/train_full_images',
                              )
    icdar_2019_art = Dataset('icdar_2019_art', '2019',
                             '/home/xiekaiyu/ocr/dataset/ICDAR2019ArT/train_labels.json',
                             '/home/xiekaiyu/ocr/dataset/ICDAR2019ArT/train_images')

    datasets = [icdar_2017_mlt, icdar_2019_lsvt, icdar_2019_art]

    coco_images_dir = '/home/xiekaiyu/ocr/dataset/test/train_images'
    coco_label_file = '/home/xiekaiyu/ocr/dataset/test/coco_labels.json'

    converter = COCOConverter(datasets, coco_images_dir, coco_label_file)
    converter.convert()
