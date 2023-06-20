
import argparse
import pickle
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils import data
from torchvision import utils, transforms
import numpy as np
from torchvision.datasets import ImageFolder
from training.dataset import (
    MultiResolutionDataset,
    GTMaskDataset,
)
from scipy import linalg
import random
import time
import os
from tqdm import tqdm
from copy import deepcopy
import cv2
from PIL import Image
from itertools import combinations
from training.model import Generator, Encoder
import pickle
device = "cuda"
transform = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5), inplace=True),
    ]
)
mask_path = f"data/celeba_hq/local_editing"
src_path = f"data/celeba_hq/test/aaa"

path = f"data/celeba_hq/test2/src/1/00001.png"
# print(os.path.exists(path))
image=Image.open(path)
# dataset = GTMaskDataset("data/celeba_hq", transform, 512)
#
# aaa = (
#     f"data/celeba_hq/local_editing/new_mapping.txt"
# )
# a = ['{0:05}'.format(num) for num in range(0, 1000)]
# with open(aaa, "w") as fp:
#     for i in range(len(a)):
#         L = str(i) + "    " + a[i] + "    " + a[i] + ".png\n"
#         fp.writelines(L)




import os

# a = ['data/celeba_hq/local_editing/GT_labels/17619.png', 'data/celeba_hq/local_editing/GT_labels/9798.png', 'data/celeba_hq/local_editing/GT_labels/28666.png', 'data/celeba_hq/local_editing/GT_labels/3556.png', 'data/celeba_hq/local_editing/GT_labels/12026.png', 'data/celeba_hq/local_editing/GT_labels/9585.png', 'data/celeba_hq/local_editing/GT_labels/29789.png', 'data/celeba_hq/local_editing/GT_labels/7441.png', 'data/celeba_hq/local_editing/GT_labels/19128.png', 'data/celeba_hq/local_editing/GT_labels/7835.png', 'data/celeba_hq/local_editing/GT_labels/27248.png', 'data/celeba_hq/local_editing/GT_labels/27450.png', 'data/celeba_hq/local_editing/GT_labels/11435.png', 'data/celeba_hq/local_editing/GT_labels/16619.png', 'data/celeba_hq/local_editing/GT_labels/23939.png', 'data/celeba_hq/local_editing/GT_labels/2377.png', 'data/celeba_hq/local_editing/GT_labels/6538.png', 'data/celeba_hq/local_editing/GT_labels/15760.png', 'data/celeba_hq/local_editing/GT_labels/496.png', 'data/celeba_hq/local_editing/GT_labels/17669.png', 'data/celeba_hq/local_editing/GT_labels/29864.png', 'data/celeba_hq/local_editing/GT_labels/4385.png', 'data/celeba_hq/local_editing/GT_labels/15663.png', 'data/celeba_hq/local_editing/GT_labels/12728.png', 'data/celeba_hq/local_editing/GT_labels/10157.png', 'data/celeba_hq/local_editing/GT_labels/27790.png', 'data/celeba_hq/local_editing/GT_labels/6184.png', 'data/celeba_hq/local_editing/GT_labels/10607.png', 'data/celeba_hq/local_editing/GT_labels/21064.png', 'data/celeba_hq/local_editing/GT_labels/11626.png', 'data/celeba_hq/local_editing/GT_labels/26210.png', 'data/celeba_hq/local_editing/GT_labels/565.png', 'data/celeba_hq/local_editing/GT_labels/21830.png', 'data/celeba_hq/local_editing/GT_labels/19797.png', 'data/celeba_hq/local_editing/GT_labels/10852.png', 'data/celeba_hq/local_editing/GT_labels/22035.png', 'data/celeba_hq/local_editing/GT_labels/20523.png', 'data/celeba_hq/local_editing/GT_labels/29238.png', 'data/celeba_hq/local_editing/GT_labels/9839.png', 'data/celeba_hq/local_editing/GT_labels/11104.png', 'data/celeba_hq/local_editing/GT_labels/27914.png', 'data/celeba_hq/local_editing/GT_labels/5454.png', 'data/celeba_hq/local_editing/GT_labels/19963.png', 'data/celeba_hq/local_editing/GT_labels/7444.png', 'data/celeba_hq/local_editing/GT_labels/28902.png', 'data/celeba_hq/local_editing/GT_labels/28794.png', 'data/celeba_hq/local_editing/GT_labels/4166.png', 'data/celeba_hq/local_editing/GT_labels/10337.png', 'data/celeba_hq/local_editing/GT_labels/7178.png', 'data/celeba_hq/local_editing/GT_labels/6770.png', 'data/celeba_hq/local_editing/GT_labels/20530.png', 'data/celeba_hq/local_editing/GT_labels/7704.png', 'data/celeba_hq/local_editing/GT_labels/12048.png', 'data/celeba_hq/local_editing/GT_labels/7192.png', 'data/celeba_hq/local_editing/GT_labels/4407.png', 'data/celeba_hq/local_editing/GT_labels/4842.png', 'data/celeba_hq/local_editing/GT_labels/4327.png', 'data/celeba_hq/local_editing/GT_labels/20797.png', 'data/celeba_hq/local_editing/GT_labels/15111.png', 'data/celeba_hq/local_editing/GT_labels/26470.png', 'data/celeba_hq/local_editing/GT_labels/22033.png', 'data/celeba_hq/local_editing/GT_labels/6960.png', 'data/celeba_hq/local_editing/GT_labels/14343.png', 'data/celeba_hq/local_editing/GT_labels/14774.png', 'data/celeba_hq/local_editing/GT_labels/16746.png', 'data/celeba_hq/local_editing/GT_labels/25941.png', 'data/celeba_hq/local_editing/GT_labels/3110.png', 'data/celeba_hq/local_editing/GT_labels/25499.png', 'data/celeba_hq/local_editing/GT_labels/19457.png', 'data/celeba_hq/local_editing/GT_labels/10155.png', 'data/celeba_hq/local_editing/GT_labels/29207.png', 'data/celeba_hq/local_editing/GT_labels/6323.png', 'data/celeba_hq/local_editing/GT_labels/3326.png', 'data/celeba_hq/local_editing/GT_labels/11236.png', 'data/celeba_hq/local_editing/GT_labels/12404.png', 'data/celeba_hq/local_editing/GT_labels/1446.png', 'data/celeba_hq/local_editing/GT_labels/29523.png', 'data/celeba_hq/local_editing/GT_labels/1415.png', 'data/celeba_hq/local_editing/GT_labels/12800.png', 'data/celeba_hq/local_editing/GT_labels/25999.png', 'data/celeba_hq/local_editing/GT_labels/7877.png', 'data/celeba_hq/local_editing/GT_labels/10362.png', 'data/celeba_hq/local_editing/GT_labels/3875.png', 'data/celeba_hq/local_editing/GT_labels/22328.png', 'data/celeba_hq/local_editing/GT_labels/28137.png', 'data/celeba_hq/local_editing/GT_labels/4577.png', 'data/celeba_hq/local_editing/GT_labels/12927.png', 'data/celeba_hq/local_editing/GT_labels/27588.png', 'data/celeba_hq/local_editing/GT_labels/16614.png', 'data/celeba_hq/local_editing/GT_labels/22502.png', 'data/celeba_hq/local_editing/GT_labels/17972.png', 'data/celeba_hq/local_editing/GT_labels/27417.png', 'data/celeba_hq/local_editing/GT_labels/6303.png', 'data/celeba_hq/local_editing/GT_labels/19877.png', 'data/celeba_hq/local_editing/GT_labels/25833.png', 'data/celeba_hq/local_editing/GT_labels/24465.png', 'data/celeba_hq/local_editing/GT_labels/591.png', 'data/celeba_hq/local_editing/GT_labels/11441.png', 'data/celeba_hq/local_editing/GT_labels/22787.png', 'data/celeba_hq/local_editing/GT_labels/21782.png', 'data/celeba_hq/local_editing/GT_labels/1824.png', 'data/celeba_hq/local_editing/GT_labels/26346.png', 'data/celeba_hq/local_editing/GT_labels/6712.png', 'data/celeba_hq/local_editing/GT_labels/19279.png', 'data/celeba_hq/local_editing/GT_labels/20675.png', 'data/celeba_hq/local_editing/GT_labels/23009.png', 'data/celeba_hq/local_editing/GT_labels/10646.png', 'data/celeba_hq/local_editing/GT_labels/12384.png', 'data/celeba_hq/local_editing/GT_labels/7051.png', 'data/celeba_hq/local_editing/GT_labels/15447.png', 'data/celeba_hq/local_editing/GT_labels/23175.png', 'data/celeba_hq/local_editing/GT_labels/13829.png', 'data/celeba_hq/local_editing/GT_labels/1501.png', 'data/celeba_hq/local_editing/GT_labels/25769.png', 'data/celeba_hq/local_editing/GT_labels/12931.png', 'data/celeba_hq/local_editing/GT_labels/10528.png', 'data/celeba_hq/local_editing/GT_labels/29922.png', 'data/celeba_hq/local_editing/GT_labels/2461.png', 'data/celeba_hq/local_editing/GT_labels/5375.png', 'data/celeba_hq/local_editing/GT_labels/19216.png', 'data/celeba_hq/local_editing/GT_labels/26691.png', 'data/celeba_hq/local_editing/GT_labels/6784.png', 'data/celeba_hq/local_editing/GT_labels/17609.png', 'data/celeba_hq/local_editing/GT_labels/28815.png', 'data/celeba_hq/local_editing/GT_labels/5786.png', 'data/celeba_hq/local_editing/GT_labels/19598.png', 'data/celeba_hq/local_editing/GT_labels/8362.png', 'data/celeba_hq/local_editing/GT_labels/19212.png', 'data/celeba_hq/local_editing/GT_labels/3985.png', 'data/celeba_hq/local_editing/GT_labels/25925.png', 'data/celeba_hq/local_editing/GT_labels/28378.png', 'data/celeba_hq/local_editing/GT_labels/12426.png', 'data/celeba_hq/local_editing/GT_labels/15627.png', 'data/celeba_hq/local_editing/GT_labels/22522.png', 'data/celeba_hq/local_editing/GT_labels/14652.png', 'data/celeba_hq/local_editing/GT_labels/10233.png', 'data/celeba_hq/local_editing/GT_labels/11424.png', 'data/celeba_hq/local_editing/GT_labels/155.png', 'data/celeba_hq/local_editing/GT_labels/23491.png', 'data/celeba_hq/local_editing/GT_labels/18838.png', 'data/celeba_hq/local_editing/GT_labels/687.png', 'data/celeba_hq/local_editing/GT_labels/23094.png', 'data/celeba_hq/local_editing/GT_labels/24444.png', 'data/celeba_hq/local_editing/GT_labels/25540.png', 'data/celeba_hq/local_editing/GT_labels/26220.png', 'data/celeba_hq/local_editing/GT_labels/1693.png', 'data/celeba_hq/local_editing/GT_labels/16694.png', 'data/celeba_hq/local_editing/GT_labels/29528.png', 'data/celeba_hq/local_editing/GT_labels/24706.png', 'data/celeba_hq/local_editing/GT_labels/13434.png', 'data/celeba_hq/local_editing/GT_labels/1113.png', 'data/celeba_hq/local_editing/GT_labels/23033.png', 'data/celeba_hq/local_editing/GT_labels/5719.png', 'data/celeba_hq/local_editing/GT_labels/16802.png', 'data/celeba_hq/local_editing/GT_labels/14256.png', 'data/celeba_hq/local_editing/GT_labels/17040.png', 'data/celeba_hq/local_editing/GT_labels/18722.png', 'data/celeba_hq/local_editing/GT_labels/19408.png', 'data/celeba_hq/local_editing/GT_labels/18037.png', 'data/celeba_hq/local_editing/GT_labels/13426.png', 'data/celeba_hq/local_editing/GT_labels/22307.png', 'data/celeba_hq/local_editing/GT_labels/13286.png', 'data/celeba_hq/local_editing/GT_labels/14969.png', 'data/celeba_hq/local_editing/GT_labels/19133.png', 'data/celeba_hq/local_editing/GT_labels/21843.png', 'data/celeba_hq/local_editing/GT_labels/22197.png', 'data/celeba_hq/local_editing/GT_labels/6701.png', 'data/celeba_hq/local_editing/GT_labels/21457.png', 'data/celeba_hq/local_editing/GT_labels/17400.png', 'data/celeba_hq/local_editing/GT_labels/8004.png', 'data/celeba_hq/local_editing/GT_labels/3918.png', 'data/celeba_hq/local_editing/GT_labels/28095.png', 'data/celeba_hq/local_editing/GT_labels/16156.png', 'data/celeba_hq/local_editing/GT_labels/13731.png', 'data/celeba_hq/local_editing/GT_labels/20671.png', 'data/celeba_hq/local_editing/GT_labels/3253.png', 'data/celeba_hq/local_editing/GT_labels/1035.png', 'data/celeba_hq/local_editing/GT_labels/20432.png', 'data/celeba_hq/local_editing/GT_labels/6249.png', 'data/celeba_hq/local_editing/GT_labels/22764.png', 'data/celeba_hq/local_editing/GT_labels/2791.png', 'data/celeba_hq/local_editing/GT_labels/20748.png', 'data/celeba_hq/local_editing/GT_labels/26108.png', 'data/celeba_hq/local_editing/GT_labels/8551.png', 'data/celeba_hq/local_editing/GT_labels/330.png', 'data/celeba_hq/local_editing/GT_labels/19038.png', 'data/celeba_hq/local_editing/GT_labels/24117.png', 'data/celeba_hq/local_editing/GT_labels/14968.png', 'data/celeba_hq/local_editing/GT_labels/26693.png', 'data/celeba_hq/local_editing/GT_labels/17727.png', 'data/celeba_hq/local_editing/GT_labels/12516.png', 'data/celeba_hq/local_editing/GT_labels/4381.png', 'data/celeba_hq/local_editing/GT_labels/18403.png', 'data/celeba_hq/local_editing/GT_labels/29304.png', 'data/celeba_hq/local_editing/GT_labels/11645.png', 'data/celeba_hq/local_editing/GT_labels/342.png', 'data/celeba_hq/local_editing/GT_labels/29820.png', 'data/celeba_hq/local_editing/GT_labels/18820.png', 'data/celeba_hq/local_editing/GT_labels/21498.png', 'data/celeba_hq/local_editing/GT_labels/599.png', 'data/celeba_hq/local_editing/GT_labels/20752.png', 'data/celeba_hq/local_editing/GT_labels/16947.png', 'data/celeba_hq/local_editing/GT_labels/9038.png', 'data/celeba_hq/local_editing/GT_labels/10408.png', 'data/celeba_hq/local_editing/GT_labels/16279.png', 'data/celeba_hq/local_editing/GT_labels/4817.png', 'data/celeba_hq/local_editing/GT_labels/28120.png', 'data/celeba_hq/local_editing/GT_labels/21839.png', 'data/celeba_hq/local_editing/GT_labels/26935.png', 'data/celeba_hq/local_editing/GT_labels/19985.png', 'data/celeba_hq/local_editing/GT_labels/11272.png', 'data/celeba_hq/local_editing/GT_labels/2931.png', 'data/celeba_hq/local_editing/GT_labels/11591.png', 'data/celeba_hq/local_editing/GT_labels/29537.png', 'data/celeba_hq/local_editing/GT_labels/2759.png', 'data/celeba_hq/local_editing/GT_labels/8448.png', 'data/celeba_hq/local_editing/GT_labels/1307.png', 'data/celeba_hq/local_editing/GT_labels/8900.png', 'data/celeba_hq/local_editing/GT_labels/14487.png', 'data/celeba_hq/local_editing/GT_labels/20780.png', 'data/celeba_hq/local_editing/GT_labels/25803.png', 'data/celeba_hq/local_editing/GT_labels/7194.png', 'data/celeba_hq/local_editing/GT_labels/1694.png', 'data/celeba_hq/local_editing/GT_labels/5626.png', 'data/celeba_hq/local_editing/GT_labels/4337.png', 'data/celeba_hq/local_editing/GT_labels/29893.png', 'data/celeba_hq/local_editing/GT_labels/29739.png', 'data/celeba_hq/local_editing/GT_labels/27103.png', 'data/celeba_hq/local_editing/GT_labels/3123.png', 'data/celeba_hq/local_editing/GT_labels/12917.png', 'data/celeba_hq/local_editing/GT_labels/28346.png', 'data/celeba_hq/local_editing/GT_labels/7037.png', 'data/celeba_hq/local_editing/GT_labels/26680.png', 'data/celeba_hq/local_editing/GT_labels/27078.png', 'data/celeba_hq/local_editing/GT_labels/18825.png', 'data/celeba_hq/local_editing/GT_labels/26265.png', 'data/celeba_hq/local_editing/GT_labels/26592.png', 'data/celeba_hq/local_editing/GT_labels/11137.png', 'data/celeba_hq/local_editing/GT_labels/6855.png', 'data/celeba_hq/local_editing/GT_labels/3230.png', 'data/celeba_hq/local_editing/GT_labels/3677.png', 'data/celeba_hq/local_editing/GT_labels/14792.png', 'data/celeba_hq/local_editing/GT_labels/4764.png', 'data/celeba_hq/local_editing/GT_labels/21177.png', 'data/celeba_hq/local_editing/GT_labels/4251.png', 'data/celeba_hq/local_editing/GT_labels/8876.png', 'data/celeba_hq/local_editing/GT_labels/432.png', 'data/celeba_hq/local_editing/GT_labels/13081.png', 'data/celeba_hq/local_editing/GT_labels/26656.png', 'data/celeba_hq/local_editing/GT_labels/23944.png', 'data/celeba_hq/local_editing/GT_labels/14375.png', 'data/celeba_hq/local_editing/GT_labels/11193.png', 'data/celeba_hq/local_editing/GT_labels/14473.png', 'data/celeba_hq/local_editing/GT_labels/21958.png', 'data/celeba_hq/local_editing/GT_labels/2621.png', 'data/celeba_hq/local_editing/GT_labels/16865.png', 'data/celeba_hq/local_editing/GT_labels/14505.png', 'data/celeba_hq/local_editing/GT_labels/23811.png', 'data/celeba_hq/local_editing/GT_labels/8408.png', 'data/celeba_hq/local_editing/GT_labels/16733.png', 'data/celeba_hq/local_editing/GT_labels/17344.png', 'data/celeba_hq/local_editing/GT_labels/3984.png', 'data/celeba_hq/local_editing/GT_labels/18525.png', 'data/celeba_hq/local_editing/GT_labels/27198.png', 'data/celeba_hq/local_editing/GT_labels/15005.png', 'data/celeba_hq/local_editing/GT_labels/24195.png', 'data/celeba_hq/local_editing/GT_labels/6495.png', 'data/celeba_hq/local_editing/GT_labels/12644.png', 'data/celeba_hq/local_editing/GT_labels/28272.png', 'data/celeba_hq/local_editing/GT_labels/10981.png', 'data/celeba_hq/local_editing/GT_labels/13878.png', 'data/celeba_hq/local_editing/GT_labels/10594.png', 'data/celeba_hq/local_editing/GT_labels/12714.png', 'data/celeba_hq/local_editing/GT_labels/10723.png', 'data/celeba_hq/local_editing/GT_labels/516.png', 'data/celeba_hq/local_editing/GT_labels/3536.png', 'data/celeba_hq/local_editing/GT_labels/6560.png', 'data/celeba_hq/local_editing/GT_labels/19820.png', 'data/celeba_hq/local_editing/GT_labels/2565.png', 'data/celeba_hq/local_editing/GT_labels/22297.png', 'data/celeba_hq/local_editing/GT_labels/28349.png', 'data/celeba_hq/local_editing/GT_labels/1229.png', 'data/celeba_hq/local_editing/GT_labels/27970.png', 'data/celeba_hq/local_editing/GT_labels/7905.png', 'data/celeba_hq/local_editing/GT_labels/19105.png', 'data/celeba_hq/local_editing/GT_labels/12290.png', 'data/celeba_hq/local_editing/GT_labels/9921.png', 'data/celeba_hq/local_editing/GT_labels/9375.png', 'data/celeba_hq/local_editing/GT_labels/19208.png', 'data/celeba_hq/local_editing/GT_labels/28097.png', 'data/celeba_hq/local_editing/GT_labels/13532.png', 'data/celeba_hq/local_editing/GT_labels/3732.png', 'data/celeba_hq/local_editing/GT_labels/14516.png', 'data/celeba_hq/local_editing/GT_labels/7741.png', 'data/celeba_hq/local_editing/GT_labels/17261.png', 'data/celeba_hq/local_editing/GT_labels/23012.png', 'data/celeba_hq/local_editing/GT_labels/6908.png', 'data/celeba_hq/local_editing/GT_labels/29355.png', 'data/celeba_hq/local_editing/GT_labels/2830.png', 'data/celeba_hq/local_editing/GT_labels/12166.png', 'data/celeba_hq/local_editing/GT_labels/21038.png', 'data/celeba_hq/local_editing/GT_labels/20435.png', 'data/celeba_hq/local_editing/GT_labels/18967.png', 'data/celeba_hq/local_editing/GT_labels/2034.png', 'data/celeba_hq/local_editing/GT_labels/13424.png', 'data/celeba_hq/local_editing/GT_labels/21276.png', 'data/celeba_hq/local_editing/GT_labels/14174.png', 'data/celeba_hq/local_editing/GT_labels/25277.png', 'data/celeba_hq/local_editing/GT_labels/3167.png', 'data/celeba_hq/local_editing/GT_labels/19861.png', 'data/celeba_hq/local_editing/GT_labels/11719.png', 'data/celeba_hq/local_editing/GT_labels/29889.png', 'data/celeba_hq/local_editing/GT_labels/23699.png', 'data/celeba_hq/local_editing/GT_labels/7391.png', 'data/celeba_hq/local_editing/GT_labels/12133.png', 'data/celeba_hq/local_editing/GT_labels/8319.png', 'data/celeba_hq/local_editing/GT_labels/12538.png', 'data/celeba_hq/local_editing/GT_labels/3734.png', 'data/celeba_hq/local_editing/GT_labels/9381.png', 'data/celeba_hq/local_editing/GT_labels/29599.png', 'data/celeba_hq/local_editing/GT_labels/2301.png', 'data/celeba_hq/local_editing/GT_labels/11814.png', 'data/celeba_hq/local_editing/GT_labels/2856.png', 'data/celeba_hq/local_editing/GT_labels/7873.png', 'data/celeba_hq/local_editing/GT_labels/6338.png', 'data/celeba_hq/local_editing/GT_labels/9229.png', 'data/celeba_hq/local_editing/GT_labels/11643.png', 'data/celeba_hq/local_editing/GT_labels/4488.png', 'data/celeba_hq/local_editing/GT_labels/2648.png', 'data/celeba_hq/local_editing/GT_labels/20502.png', 'data/celeba_hq/local_editing/GT_labels/15589.png', 'data/celeba_hq/local_editing/GT_labels/18696.png', 'data/celeba_hq/local_editing/GT_labels/11229.png', 'data/celeba_hq/local_editing/GT_labels/1470.png', 'data/celeba_hq/local_editing/GT_labels/28951.png', 'data/celeba_hq/local_editing/GT_labels/5991.png', 'data/celeba_hq/local_editing/GT_labels/13747.png', 'data/celeba_hq/local_editing/GT_labels/7120.png', 'data/celeba_hq/local_editing/GT_labels/13252.png', 'data/celeba_hq/local_editing/GT_labels/2897.png', 'data/celeba_hq/local_editing/GT_labels/24535.png', 'data/celeba_hq/local_editing/GT_labels/3026.png', 'data/celeba_hq/local_editing/GT_labels/20508.png', 'data/celeba_hq/local_editing/GT_labels/24355.png', 'data/celeba_hq/local_editing/GT_labels/3115.png', 'data/celeba_hq/local_editing/GT_labels/9274.png', 'data/celeba_hq/local_editing/GT_labels/18409.png', 'data/celeba_hq/local_editing/GT_labels/21263.png', 'data/celeba_hq/local_editing/GT_labels/18792.png', 'data/celeba_hq/local_editing/GT_labels/18209.png', 'data/celeba_hq/local_editing/GT_labels/20648.png', 'data/celeba_hq/local_editing/GT_labels/6408.png', 'data/celeba_hq/local_editing/GT_labels/28096.png', 'data/celeba_hq/local_editing/GT_labels/6645.png', 'data/celeba_hq/local_editing/GT_labels/2057.png', 'data/celeba_hq/local_editing/GT_labels/26801.png', 'data/celeba_hq/local_editing/GT_labels/2784.png', 'data/celeba_hq/local_editing/GT_labels/24583.png', 'data/celeba_hq/local_editing/GT_labels/27105.png', 'data/celeba_hq/local_editing/GT_labels/16929.png', 'data/celeba_hq/local_editing/GT_labels/3855.png', 'data/celeba_hq/local_editing/GT_labels/2136.png', 'data/celeba_hq/local_editing/GT_labels/3057.png', 'data/celeba_hq/local_editing/GT_labels/19044.png', 'data/celeba_hq/local_editing/GT_labels/8012.png', 'data/celeba_hq/local_editing/GT_labels/3704.png', 'data/celeba_hq/local_editing/GT_labels/15330.png', 'data/celeba_hq/local_editing/GT_labels/23080.png', 'data/celeba_hq/local_editing/GT_labels/13816.png', 'data/celeba_hq/local_editing/GT_labels/1817.png', 'data/celeba_hq/local_editing/GT_labels/814.png', 'data/celeba_hq/local_editing/GT_labels/19118.png', 'data/celeba_hq/local_editing/GT_labels/3058.png', 'data/celeba_hq/local_editing/GT_labels/10843.png', 'data/celeba_hq/local_editing/GT_labels/8628.png', 'data/celeba_hq/local_editing/GT_labels/1430.png', 'data/celeba_hq/local_editing/GT_labels/2052.png', 'data/celeba_hq/local_editing/GT_labels/2751.png', 'data/celeba_hq/local_editing/GT_labels/25366.png', 'data/celeba_hq/local_editing/GT_labels/29915.png', 'data/celeba_hq/local_editing/GT_labels/596.png', 'data/celeba_hq/local_editing/GT_labels/24690.png', 'data/celeba_hq/local_editing/GT_labels/21673.png', 'data/celeba_hq/local_editing/GT_labels/18338.png', 'data/celeba_hq/local_editing/GT_labels/15269.png', 'data/celeba_hq/local_editing/GT_labels/22091.png', 'data/celeba_hq/local_editing/GT_labels/8254.png', 'data/celeba_hq/local_editing/GT_labels/5451.png', 'data/celeba_hq/local_editing/GT_labels/10444.png', 'data/celeba_hq/local_editing/GT_labels/13749.png', 'data/celeba_hq/local_editing/GT_labels/11712.png', 'data/celeba_hq/local_editing/GT_labels/9306.png', 'data/celeba_hq/local_editing/GT_labels/29901.png', 'data/celeba_hq/local_editing/GT_labels/415.png', 'data/celeba_hq/local_editing/GT_labels/25385.png', 'data/celeba_hq/local_editing/GT_labels/22670.png', 'data/celeba_hq/local_editing/GT_labels/25950.png', 'data/celeba_hq/local_editing/GT_labels/21679.png', 'data/celeba_hq/local_editing/GT_labels/497.png', 'data/celeba_hq/local_editing/GT_labels/17217.png', 'data/celeba_hq/local_editing/GT_labels/24136.png', 'data/celeba_hq/local_editing/GT_labels/10893.png', 'data/celeba_hq/local_editing/GT_labels/20951.png', 'data/celeba_hq/local_editing/GT_labels/25587.png', 'data/celeba_hq/local_editing/GT_labels/6462.png', 'data/celeba_hq/local_editing/GT_labels/23237.png', 'data/celeba_hq/local_editing/GT_labels/23197.png', 'data/celeba_hq/local_editing/GT_labels/20178.png', 'data/celeba_hq/local_editing/GT_labels/2368.png', 'data/celeba_hq/local_editing/GT_labels/6105.png', 'data/celeba_hq/local_editing/GT_labels/26405.png', 'data/celeba_hq/local_editing/GT_labels/24622.png', 'data/celeba_hq/local_editing/GT_labels/10733.png', 'data/celeba_hq/local_editing/GT_labels/2488.png', 'data/celeba_hq/local_editing/GT_labels/15457.png', 'data/celeba_hq/local_editing/GT_labels/19944.png', 'data/celeba_hq/local_editing/GT_labels/6180.png', 'data/celeba_hq/local_editing/GT_labels/27938.png', 'data/celeba_hq/local_editing/GT_labels/11035.png', 'data/celeba_hq/local_editing/GT_labels/21306.png', 'data/celeba_hq/local_editing/GT_labels/29951.png', 'data/celeba_hq/local_editing/GT_labels/14580.png', 'data/celeba_hq/local_editing/GT_labels/4152.png', 'data/celeba_hq/local_editing/GT_labels/20122.png', 'data/celeba_hq/local_editing/GT_labels/4140.png', 'data/celeba_hq/local_editing/GT_labels/9757.png', 'data/celeba_hq/local_editing/GT_labels/21802.png', 'data/celeba_hq/local_editing/GT_labels/8990.png', 'data/celeba_hq/local_editing/GT_labels/19017.png', 'data/celeba_hq/local_editing/GT_labels/29032.png', 'data/celeba_hq/local_editing/GT_labels/13491.png', 'data/celeba_hq/local_editing/GT_labels/16054.png', 'data/celeba_hq/local_editing/GT_labels/12439.png', 'data/celeba_hq/local_editing/GT_labels/7256.png', 'data/celeba_hq/local_editing/GT_labels/22378.png', 'data/celeba_hq/local_editing/GT_labels/20499.png', 'data/celeba_hq/local_editing/GT_labels/19854.png', 'data/celeba_hq/local_editing/GT_labels/24771.png', 'data/celeba_hq/local_editing/GT_labels/5582.png', 'data/celeba_hq/local_editing/GT_labels/17814.png', 'data/celeba_hq/local_editing/GT_labels/24334.png', 'data/celeba_hq/local_editing/GT_labels/18306.png', 'data/celeba_hq/local_editing/GT_labels/17823.png', 'data/celeba_hq/local_editing/GT_labels/12649.png', 'data/celeba_hq/local_editing/GT_labels/7974.png', 'data/celeba_hq/local_editing/GT_labels/996.png', 'data/celeba_hq/local_editing/GT_labels/24627.png', 'data/celeba_hq/local_editing/GT_labels/20456.png', 'data/celeba_hq/local_editing/GT_labels/5180.png', 'data/celeba_hq/local_editing/GT_labels/29802.png', 'data/celeba_hq/local_editing/GT_labels/21357.png', 'data/celeba_hq/local_editing/GT_labels/19016.png', 'data/celeba_hq/local_editing/GT_labels/10450.png', 'data/celeba_hq/local_editing/GT_labels/22576.png', 'data/celeba_hq/local_editing/GT_labels/16158.png', 'data/celeba_hq/local_editing/GT_labels/15491.png', 'data/celeba_hq/local_editing/GT_labels/26914.png', 'data/celeba_hq/local_editing/GT_labels/10110.png', 'data/celeba_hq/local_editing/GT_labels/5523.png', 'data/celeba_hq/local_editing/GT_labels/20713.png', 'data/celeba_hq/local_editing/GT_labels/6285.png', 'data/celeba_hq/local_editing/GT_labels/8255.png', 'data/celeba_hq/local_editing/GT_labels/20345.png', 'data/celeba_hq/local_editing/GT_labels/12493.png', 'data/celeba_hq/local_editing/GT_labels/25430.png', 'data/celeba_hq/local_editing/GT_labels/19371.png', 'data/celeba_hq/local_editing/GT_labels/13810.png', 'data/celeba_hq/local_editing/GT_labels/9246.png', 'data/celeba_hq/local_editing/GT_labels/5814.png', 'data/celeba_hq/local_editing/GT_labels/7681.png', 'data/celeba_hq/local_editing/GT_labels/19636.png', 'data/celeba_hq/local_editing/GT_labels/20590.png', 'data/celeba_hq/local_editing/GT_labels/20150.png', 'data/celeba_hq/local_editing/GT_labels/22997.png', 'data/celeba_hq/local_editing/GT_labels/12926.png', 'data/celeba_hq/local_editing/GT_labels/21563.png', 'data/celeba_hq/local_editing/GT_labels/29556.png', 'data/celeba_hq/local_editing/GT_labels/12754.png', 'data/celeba_hq/local_editing/GT_labels/4746.png', 'data/celeba_hq/local_editing/GT_labels/25054.png', 'data/celeba_hq/local_editing/GT_labels/20442.png', 'data/celeba_hq/local_editing/GT_labels/1999.png', 'data/celeba_hq/local_editing/GT_labels/10392.png', 'data/celeba_hq/local_editing/GT_labels/16859.png', 'data/celeba_hq/local_editing/GT_labels/23863.png', 'data/celeba_hq/local_editing/GT_labels/29836.png', 'data/celeba_hq/local_editing/GT_labels/671.png', 'data/celeba_hq/local_editing/GT_labels/26964.png', 'data/celeba_hq/local_editing/GT_labels/20856.png', 'data/celeba_hq/local_editing/GT_labels/19699.png', 'data/celeba_hq/local_editing/GT_labels/8931.png', 'data/celeba_hq/local_editing/GT_labels/16432.png', 'data/celeba_hq/local_editing/GT_labels/16773.png', 'data/celeba_hq/local_editing/GT_labels/2422.png', 'data/celeba_hq/local_editing/GT_labels/17561.png', 'data/celeba_hq/local_editing/GT_labels/7062.png', 'data/celeba_hq/local_editing/GT_labels/17515.png', 'data/celeba_hq/local_editing/GT_labels/14680.png', 'data/celeba_hq/local_editing/GT_labels/9853.png', 'data/celeba_hq/local_editing/GT_labels/11293.png']
# print(len(a))
# b = [77, 135, 362, 226, 183, 182, 20, 333, 147, 64, 129, 36, 95, 207, 239, 260, 157, 81, 123, 76, 8, 170, 10, 140, 388, 122, 146, 177, 54, 109, 336, 120, 167, 165, 80, 332, 339, 409, 224, 82, 199, 128, 15, 51, 100, 364, 11, 73, 279, 3, 181, 444, 243, 112, 7, 387, 141, 50, 94, 89, 209, 185, 391, 105, 57, 394, 196, 347, 17, 108, 432, 38, 193, 111, 281, 269, 22, 227, 275, 13, 172, 101, 298, 230, 49, 151, 132, 262, 130, 97, 116, 90, 242, 60, 87, 41, 159, 368, 455, 246, 273, 32, 58, 134, 429, 149, 92, 380, 115, 253, 24, 195, 354, 257, 9, 65, 300, 152, 126, 16, 23, 107, 53, 208, 296, 0, 306, 220, 287, 264, 21, 136, 14, 29, 375, 382, 56, 190, 240, 62, 263, 407, 252, 69, 308, 265, 197, 44, 270, 68, 75, 249, 55, 327, 174, 232, 70, 39, 206, 114, 291, 43, 33, 184, 277, 154, 66, 350, 316, 139, 280, 238, 18, 63, 40, 12, 93, 4, 379, 189, 148, 293, 59, 150, 52, 103, 201, 397, 45, 67, 286, 28, 86, 304, 231, 235, 365, 104, 83, 74, 85, 340, 25, 125, 155, 179, 27, 346, 278, 35, 169, 282, 213, 313, 412, 331, 124, 113, 34, 42, 61, 258, 5, 219, 202, 99, 285, 6, 37, 251, 19, 106, 110, 91, 160, 176, 1, 31, 218, 26, 48, 222, 352, 2, 241, 163, 442, 221, 233, 46]
# print(len(b))
#mask_path_base = f"data/celeba_hq/local_editing"
#with open(
#        f"{mask_path_base}/celeba_hq_test_GT_sorted_pair (copy).pkl",
#        "rb",
#) as f:
#    sorted_similarity = pickle.load(f)
# for item in sorted_similarity:
#     print(item)
#for item in sorted_similarity["eye"]:
#    print(item)

