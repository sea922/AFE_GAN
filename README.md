# StyleMapGAN.local_editing

![ubuntu](https://img.shields.io/badge/ubuntu-18.04.5_LTS-green.svg?style=plastic) ![CUDA](https://img.shields.io/badge/CUDA-10.0.130-green.svg?style=plastic) ![CUDA-driver](https://img.shields.io/badge/CUDA_driver-410.72-green.svg?style=plastic) ![cudnn7](https://img.shields.io/badge/cudnn-7.6.3-green.svg?style=plastic) ![Python 3.6.12](https://img.shields.io/badge/python-3.6.12-green.svg?style=plastic) ![pytorch 1.4.0](https://img.shields.io/badge/pytorch-1.4.0-green.svg?style=plastic)

My FYP project. 

## Installation

Clone this repository:

```bash
git clone https://github.com/siidev/AFE_GAN
cd StyleMapGAN_Auto-Recognition/
```

Install the dependencies:
```bash
conda create -y -n stylemapgan python=3.6.12
conda activate stylemapgan
./install.sh
```

## Demo

Run demo in your local machine.

All test images are from [CelebA-HQ](https://arxiv.org/abs/1710.10196).

```bash
python demo.py
```

<b>Use your own images</b>

```bash
cp -R [source folder] demo/components/img/celeba_hq # copy your own images to the demo folder
cd face_parsing
python test.py # mask generation
```

## Generate images

<b>Local editing</b>
Results are saved to `expr/local_editing`. 

```bash
python generate.py --ckpt expr/checkpoints/celeba_hq_256_8x8.pt --mixing_type local_editing --test_lmdb data/celeba_hq/LMDB_test --local_editing_part [part name]
```
<b>Use your own images</b>
```bash
# transforms raw image to LMDB format
python prepare_data.py [raw images path] --out [destination path] --size [TARGET_SIZE] 
```

## Related Projects
This project starts from [StyleMapGAN official code](https://github.com/naver-ai/StyleMapGAN). Face parsing model starts from [face parsing using BiSeNet](https://github.com/zllrunning/face-parsing.PyTorch)。
