from torch.utils.data import Dataset
from torchvision.io import read_image
import pandas as pd
from pathlib import Path


class TracedDigitsDataset(Dataset):

    def __init__(self, data_dir, transform=None, target_transform=None):
        self.data_dir = Path(__file__).parent / data_dir
        self.img_labels = pd.read_csv(self.data_dir / 'TracedDigits.csv')
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        label = self.img_labels.iloc[idx, 1]
        img_path = self.data_dir / str(label) / self.img_labels.iloc[idx, 0]
        image = read_image(img_path)
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label
