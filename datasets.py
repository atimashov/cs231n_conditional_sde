import torch
from torch.utils.data import DataLoader
import torchvision.transforms as T
import os
import json
from PIL import Image, JpegImagePlugin
from tqdm import tqdm

class COCODataset(torch.utils.data.Dataset):
    def __init__(
            self, imgs_dir, captions_path, transform = None, tgt_img_size = (256, 256)
    ):
        # create list of images directories
        self.imgs_path = ['{}/{}'.format(imgs_dir, img_name) for img_name in os.listdir(imgs_dir)]

        # create JSON captions
        f = open(captions_path)
        self.captions = json.load(f)

        # create transform
        if transform is None:
            self.transform = T.Compose([
                T.Resize(tgt_img_size),
                T.ToTensor(),
                T.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
            ])
        else:
            self.transform = transform

    def __len__(self):
        return len(self.imgs_path)

    def __getitem__(self, index):
        img_path = self.imgs_path[index]
        image = Image.open(img_path) # in PIL
        image = self.transform(image)

        # TODO: create captions
        return image, torch.zeros(1)

def test():
    imgs_dir = '{}/images'
    captions_path = 1
    data = COCODataset(
        imgs_dir = imgs_dir, captions_path = captions_path
    )
    data_loader = DataLoader(
        data, batch_size = 4, shuffle = True, num_workers = 6, drop_last=True, pin_memory = True
    )
    loop = tqdm(data_loader, leave = True)
    for batch_idx, (imgs, captions) in enumerate(loop):
        loop.set_postfix(imgs_shape=imgs.shape, lables_shape = captions.shape)

if __name__=='__main__':
	test()