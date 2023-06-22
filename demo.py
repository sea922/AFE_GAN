"""
StyleMapGAN
Copyright (c) 2021-present NAVER Corp.

This work is licensed under the Creative Commons Attribution-NonCommercial
4.0 International License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

import flask
from flask import Flask, render_template, request, redirect, url_for
from flask_ngrok import run_with_ngrok # new
from pyngrok import ngrok # for public server
import numpy as np
import base64
import os
import secrets
import argparse
from PIL import Image

######
import torch
from torch import nn
from training.model import Generator, Encoder
import torch.nn.functional as F
import torchvision.transforms.functional as TF
from torchvision import transforms
import io

# Set authentication
NGROK_AUTH_TOKEN = '22DeddP7TNdpTacy8yQ6eYWg4S4_7k42ykiuKoME4BP2x3XS1'
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

app = Flask(
    __name__,
    template_folder="demo/templates",
    static_url_path="/demo/static",
    static_folder="demo/static",
)
run_with_ngrok(app)

app.config["MAX_CONTENT_LENGTH"] = 10000000  # allow 10 MB post

# for 1 gpu only.
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.g_ema = Generator(
            train_args.size,
            train_args.mapping_layer_num,
            train_args.latent_channel_size,
            train_args.latent_spatial_size,
            lr_mul=train_args.lr_mul,
            channel_multiplier=train_args.channel_multiplier,
            normalize_mode=train_args.normalize_mode,
            small_generator=train_args.small_generator,
        )
        self.e_ema = Encoder(
            train_args.size,
            train_args.latent_channel_size,
            train_args.latent_spatial_size,
            channel_multiplier=train_args.channel_multiplier,
        )
        self.device = device

    def forward(self, original_image, references, mask):

        combined = torch.cat([original_image, references], dim=0)

        ws = self.e_ema(combined)
        original_stylemap, reference_stylemaps = torch.split(
            ws, [1, len(ws) - 1], dim=0
        )

        mixed = self.g_ema(
            [original_stylemap, reference_stylemaps],
            input_is_stylecode=True,
            mix_space=mixspace,
            mask=mask,
        )[0]
        return mixed

@app.route("/")
def index():
    image_paths = []
    global mixspace
    mixspace = "w_plus"
    return render_template(
        "index.html",
        canvas_size=train_args.size,
        base_path=base_path,
        image_paths=list(os.listdir(base_path)),
    )

@app.route("/interpolation")
def index1():
    image_paths = []
    global mixspace
    mixspace = "demo1"
    return render_template(
        "index1.html",
        canvas_size=train_args.size,
        base_path=base_path,
        image_paths=list(os.listdir(base_path)),
    )

def hex2val(hex):
    if len(hex) != 7:
        raise Exception("invalid hex")
    val = int(hex[1:], 16)
    return np.array([val >> 16, (val >> 8) & 255, val & 255])

@torch.no_grad()
def my_morphed_images(
    original, references, region, masks, shift_values, interpolation=8, save_dir=None
):
    original_image = Image.open(base_path + original)
    reference_images = []

    for ref in references:
        reference_images.append(
            TF.to_tensor(
                Image.open(base_path + ref).resize((train_args.size, train_args.size))
            )
        )

    original_image = TF.to_tensor(original_image).unsqueeze(0)
    original_image = F.interpolate(
        original_image, size=(train_args.size, train_args.size)
    )
    original_image = (original_image - 0.5) * 2

    reference_images = torch.stack(reference_images)
    reference_images = F.interpolate(
        reference_images, size=(train_args.size, train_args.size)
    )
    reference_images = (reference_images - 0.5) * 2

    mask1 = Image.open(mask_path + original)
    mask1 = mask1.resize((train_args.size, train_args.size), Image.NEAREST)
    mask1 = transforms.ToTensor()(mask1)
    mask1 = mask1.squeeze()
    mask1 *= 255
    mask1 = mask1.long()
    assert mask1.shape == (train_args.size, train_args.size)
    mask11 = -torch.ones(mask1.shape).to(device)
    for label_i in parts_index[region]:
        mask11[(mask1 == label_i) == True] = 1
    mask11 = mask11.unsqueeze(0)
    mask2 = Image.open(mask_path + ref)
    if mixspace == "demo1":
        mask2 = Image.open(mask_path + original)
    mask2 = mask2.resize((train_args.size, train_args.size), Image.NEAREST)
    mask2 = transforms.ToTensor()(mask2)
    mask2 = mask2.squeeze()
    mask2 *= 255
    mask2 = mask2.long()
    assert mask2.shape == (train_args.size, train_args.size)
    mask22 = -torch.ones(mask2.shape).to(device)
    for label_i in parts_index[region]:
        mask22[(mask2 == label_i) == True] = 1
    mask22 = mask22.unsqueeze(0)

    original_image, reference_images = (
        original_image.to(device),
        reference_images.to(device),
    )
    if mixspace == "demo1":
        args.interpolation_step = 16
        mask11 = mask11.unsqueeze(0)
        mask22 = mask22.unsqueeze(0)
        maskaa = [mask11, mask22, args.interpolation_step]
    else:
        maskaa = mask11 + mask22
        maskaa = maskaa.float()

    mixed = model(original_image, reference_images, maskaa).cpu()
    mixed = np.asarray(
        np.clip(mixed * 127.5 + 127.5, 0.0, 255.0), dtype=np.uint8
    ).transpose(
        (0, 2, 3, 1)
    )  # 0~255

    return mixed

@app.route("/post", methods=["POST"])
def post():
    if request.method == "POST":
        user_id = request.json["id"]
        original = request.json["original"]
        references = request.json["references"]
        region = str(request.json["region"])
        colors = [hex2val(hex) for hex in request.json["colors"]]
        data_reference_bin = []
        shift_values = request.json["shift_original"]
        save_dir = f"demo/static/generated/{user_id}"
        masks = references[0]

        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        for i, d_ref in enumerate(request.json["data_reference"]):
            data_reference_bin.append(base64.b64decode(d_ref))

            with open(f"{save_dir}/classmap_reference_{i}.png", "wb") as f:
                f.write(bytearray(data_reference_bin[i]))

        generated_images = my_morphed_images(
            original,
            references,
            region,
            masks,
            shift_values,
            interpolation=args.interpolation_step,
            save_dir=save_dir,
        )
        paths = []

        for i in range(args.interpolation_step):
            path = f"{save_dir}/{i}.png"
            Image.fromarray(generated_images[i]).save(path)
            paths.append(path + "?{}".format(secrets.token_urlsafe(16)))

        return flask.jsonify(result=paths)
    else:
        return redirect(url_for("index"))


if __name__ == "__main__":
    parts_index = {
        "background": [0],
        "skin": [1],
        "eyebrow": [2, 3],
        "eye": [4, 5, 6],
        "ear": [7, 8, 9],
        "nose": [10],
        "lip": [11, 12, 13],
        "neck": [14, 15],
        "cloth": [16],
        "hair": [17],
    }
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        type=str,
        default="celeba_hq",
        choices=["celeba_hq", "afhq", "lsun/church_outdoor", "lsun/car"],
    )
    parser.add_argument("--interpolation_step", type=int, default=1)
    parser.add_argument("--ckpt", type=str, default="expr/checkpoints/celeba_hq_256_8x8.pt")
    parser.add_argument(
        "--MAX_CONTENT_LENGTH", type=int, default=10000000
    )  # allow maximum 10 MB POST
    args = parser.parse_args()

    device = "cuda"
    base_path = f"demo/static/components/img/{args.dataset}/"
    mask_path = f"/mnt/xjzhang/face-parsing.PyTorch/res/test_res/"
    ckpt = torch.load(args.ckpt)

    train_args = ckpt["train_args"]
    print("train_args: ", train_args)

    model = Model().to(device)
    model.g_ema.load_state_dict(ckpt["g_ema"])
    model.e_ema.load_state_dict(ckpt["e_ema"])
    model.eval()

    app.debug = True
    app.run()
