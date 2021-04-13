import os


class Dataset(object):
    def __init__(self, name, version, label, images_dir):
        assert isinstance(name, str)
        assert version in ['2017', '2019'], f'only support icdar 2017, 2019'
        assert os.path.isfile(label) or os.path.isdir(label), f'\'{label}\' not found'
        assert os.path.isdir(images_dir), f'dir \'{images_dir}\' not found'

        self.name = name
        self.version = version
        self.label = label
        self.images_dir = images_dir
