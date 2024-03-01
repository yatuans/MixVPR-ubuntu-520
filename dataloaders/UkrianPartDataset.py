from pathlib import Path
import numpy as np
from PIL import Image
from torch.utils.data import Dataset

# NOTE: you need to download the mapillary_sls dataset from  https://github.com/FrederikWarburg/mapillary_sls
# make sure the path where the mapillary_sls validation dataset resides on your computer is correct.
# the folder named train_val should reside in DATASET_ROOT path (that's the only folder you need from mapillary_sls)
# I hardcoded the groundtruth for image to image evaluation, otherwise it would take ages to run the groundtruth script at each epoch.

BASE_PATH  = r'/media/cartolab3/be59206e-0fa5-47d3-b128-2e1d009ec2c7/yts_files/datasets/yts_history_satellite_from_esri/'
path_obj = Path(BASE_PATH)
if not path_obj.exists():
    raise Exception('Please make sure the path to mapillary_sls dataset is correct')

if not path_obj.joinpath('train_val'):
    raise Exception(f'Please make sure the directory train_val from mapillary_sls dataset is situated in the directory {BASE_PATH}')

class MSLS(Dataset):
    def __init__(self, input_transform = None):
        
        self.input_transform = input_transform
        
        # hard coded reference image names, this avoids the hassle of listing them at each epoch.
        self.dbImages = np.load('datasets/ukrian-part_val/ukrian-part_dbImages.npy')
        
        # hard coded query image names.
        self.qImages = np.load('datasets/ukrian-part_val/ukrian-part_qImages.npy')
        
        # hard coded index of query images
        self.qIdx = np.load('datasets/ukrian-part_val/ukrian-part_qIdx.npy')
        
        # hard coded groundtruth (correspondence between each query and its matches)
        self.pIdx = np.load('datasets/ukrian-part_val/ukrian-part_pIdx.npy', allow_pickle=True)
        
        # concatenate reference images then query images so that we can use only one dataloader
        self.images = np.concatenate((self.dbImages, self.qImages[self.qIdx]))
        
        # we need to keeo the number of references so that we can split references-queries 
        # when calculating recall@K
        self.num_references = len(self.dbImages)
    
    def __getitem__(self, index):
        img = Image.open(BASE_PATH+self.images[index])

        if self.input_transform:
            img = self.input_transform(img)

        return img, index

    def __len__(self):
        return len(self.images)

# if __name__ == '__main__':
    # dataset = MSLS()
    # a = dataset[0]
    # print(dataset.__getitem__(0))
    # # print(dataset.pIdx)
    # # print(dataset.dbImages)
    # # print(dataset.pIdx)
    # print(f'len of dbImages:{len(dataset.dbImages)}')
    # print(f'len of pIdx:{len(dataset.pIdx)}')
    # print(f'len of qImages:{len(dataset.qImages)}')
    # print(f'len of qIdx:{len(dataset.qIdx)}')
