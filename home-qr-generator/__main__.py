import argparse
from ast import arg
from math import ceil
import os
import pathlib
import random
import string
from tkinter import CENTER
from typing import List, Tuple
import qrcode
from PIL import Image, ImageDraw, ImageFont
import tqdm


WORDSET = string.ascii_lowercase


def color(s):
    try:
        r, g, b = map(int, s.split(','))
        return r, g, b
    except:
        raise argparse.ArgumentTypeError("Color must be r,g,b")


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("base")
    argparser.add_argument("--length", default=2)
    argparser.add_argument("--maxcols", default=len(WORDSET)//2)
    argparser.add_argument("--prefix", default=WORDSET[0])
    argparser.add_argument("--fill", type=color, default=(0, 0, 0))
    argparser.add_argument("--back", type=color, default=(255, 255, 255))
    argparser.add_argument("--outdir", default="output/")
    argparser.add_argument("--split", default=4)

    args = argparser.parse_args()

    print(args.base, args.length)

    suffixes = construct_random_strs(args.length)

    outdir = pathlib.Path(args.outdir)

    if not outdir.exists():
        os.mkdir(outdir)
    if not outdir.is_dir():
        print(f"{outdir} is not directory")
        exit(1)

    max_width = 0
    max_height = 0

    print(f"generate {len(suffixes)} qr code into {outdir}...")
    for s in tqdm.tqdm(suffixes):
        id = args.prefix + s
        p = outdir.joinpath(f"{id}.png")
        img = create_qr(args.base, id, args.fill, args.back)
        (width, height) = img.size
        if max_width < width:
            max_width = width
        if max_height < height:
            max_height = height
        img.save(p)

    n_rows = (len(suffixes) + args.maxcols - 1) // args.maxcols

    n_rows_per_img = (n_rows + args.split - 1) // args.split

    print(max_width, max_height)

    progress = tqdm.tqdm(total=len(suffixes))
    print(
        f"generate {args.split} {args.maxcols*max_width}x{n_rows_per_img*max_height}px image..."
    )
    for i in range(args.split):
        outfile_path = outdir.joinpath(f"{i}_joined.png")
        output_img: Image.Image = Image.new(
            mode="RGB",
            size=(args.maxcols*max_width, n_rows_per_img*max_height)
        )
        for j in range(n_rows_per_img):
            for k in range(args.maxcols):
                index = (i*n_rows_per_img*args.maxcols) + j*args.maxcols + k
                if not (index < len(suffixes)):
                    break
                id = args.prefix + suffixes[index]
                p = outdir.joinpath(f"{id}.png")
                img = Image.open(p)
                output_img.paste(img, box=(k*max_width, j*max_height))
                progress.update(1)
        output_img.save(outfile_path)


def construct_random_strs(length: int) -> List[str]:
    ret = [""]
    for _ in range(length):
        tmp = []
        for s in ret:
            for c in WORDSET:
                tmp.append(s+c)
        ret = tmp
    random.shuffle(ret)
    return ret


def create_qr(prefix: str, id: str, fill: Tuple[int, int, int], back: Tuple[int, int, int]) -> Image:
    box_size = 5
    qr = qrcode.QRCode(
        error_correction=qrcode.ERROR_CORRECT_M, border=0, box_size=box_size
    )
    qr.add_data(prefix+id, optimize=len(prefix+id))
    qr.make()
    qr_img = qr.make_image(fill_color=fill, back_color=back)
    (w, h) = qr_img.size
    img = Image.new("RGB", (w+box_size*(3+3), h+box_size*(5+1)), (255, 255, 255))
    img.paste(qr_img, (box_size*3, box_size*5))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        font="NotoMono-Regular.ttf", size=box_size*5)
    true_width = w+box_size*(3+3)
    draw.text(
        xy=(true_width/2, box_size*box_size/2),
        text=id,
        anchor='mm',
        font=font,
        fill=(0, 0, 0),
    )
    return img


if __name__ == "__main__":
    main()
