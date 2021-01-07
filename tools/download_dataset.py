# import wget

urls = {
    'ICDAR2017': {
        'MLT': {
            'detection': {
                'trainset': {
                    'train_images': [
                        'http://datasets.cvc.uab.es/rrc/ch8_training_images_1.zip',
                        'http://datasets.cvc.uab.es/rrc/ch8_training_images_2.zip',
                        'http://datasets.cvc.uab.es/rrc/ch8_training_images_3.zip',
                        'http://datasets.cvc.uab.es/rrc/ch8_training_images_4.zip',
                        'http://datasets.cvc.uab.es/rrc/ch8_training_images_5.zip',
                        'http://datasets.cvc.uab.es/rrc/ch8_training_images_6.zip',
                        'http://datasets.cvc.uab.es/rrc/ch8_training_images_7.zip',
                        'http://datasets.cvc.uab.es/rrc/ch8_training_images_8.zip'
                    ],
                    'train_labels': 'http://datasets.cvc.uab.es/rrc/ch8_training_localization_transcription_gt_v2.zip'
                },
                'validset': {
                    'valid_images': 'https://rrc.cvc.uab.es/downloads/ch8_validation_images.zip',
                    'valid_labels': 'http://datasets.cvc.uab.es/rrc/ch8_validation_localization_transcription_gt_v2.zip'
                },
                'testset': 'http://datasets.cvc.uab.es/rrc/ch8_test_images.zip'
            },
            'recog': {
                'trainset': [
                    'http://datasets.cvc.uab.es/rrc/ch8_training_word_images_gt_part_1.zip',
                    'http://datasets.cvc.uab.es/rrc/ch8_training_word_images_gt_part_2.zip',
                    'http://datasets.cvc.uab.es/rrc/ch8_training_word_images_gt_part_3.zip',
                ],
                'validset': {
                    'valid_images': 'https://rrc.cvc.uab.es/downloads/ch8_validation_word_images_gt.zip',
                    'valid_labels': 'http://datasets.cvc.uab.es/rrc/ch8_validation_word_gt_v2.zip'
                },
                'testset': 'http://datasets.cvc.uab.es/rrc/ch8_test_word_images.zip'
            }
        }
    },
    'ICDAR2019': {
        'ArT': {
            'trainset': {
                'detection': {
                    'train_images': 'https://dataset-bj.cdn.bcebos.com/art/train_images.tar.gz',
                    'train_labels': 'https://dataset-bj.cdn.bcebos.com/art/train_labels.json'
                },
                'recog': {
                    'train_images': 'https://dataset-bj.cdn.bcebos.com/art/train_task2_images.tar.gz',
                    'train_labels': 'https://dataset-bj.cdn.bcebos.com/art/train_task2_labels.json'
                }
            },
            'testset': {
                'detection': [
                    'https://dataset-bj.cdn.bcebos.com/art/test_part1_images.tar.gz',
                    'https://dataset-bj.cdn.bcebos.com/art/test_part2_images.tar.gz'
                ],
                'recog': [
                    'https://dataset-bj.cdn.bcebos.com/art/test_part1_task2_images.tar.gz',
                    'https://dataset-bj.cdn.bcebos.com/art/test_part2_task2_images.tar.gz'
                ]
            }
        },
        'LSVT': {
            'trainset': {
                'train_images': [
                    'https://dataset-bj.cdn.bcebos.com/lsvt/train_full_images_0.tar.gz',
                    'https://dataset-bj.cdn.bcebos.com/lsvt/train_full_images_1.tar.gz',
                ],
                'train_labels': 'https://dataset-bj.cdn.bcebos.com/lsvt/train_full_labels.json'
            },
            'testset': [
                'https://dataset-bj.cdn.bcebos.com/lsvt/test_part1_images.tar.gz',
                'https://dataset-bj.cdn.bcebos.com/lsvt/test_part2_images.tar.gz'
            ]
        }
    }
}


def download(path, urls):
    pass


if __name__ == '__main__':
    path = ''
    download(path, urls)
