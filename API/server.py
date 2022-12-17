from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from io import BytesIO
from PIL import Image
import os
import json


from utils import *
from config import Config
from svg import SVG
from bezier import PolyBezier
from coeff import Coefficient_calculator


app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/image")
async def process_image(file: UploadFile):
    save(file)
    if get_extension(file.filename) != "svg":
        file_path = convert_to_svg(os.path.join(Config.IMAGE_PATH, file.filename))
    else:
        file_path = file.filename
    paths = parse_svg(file_path)
    poly_beziers = compile_polybeziers(paths)
    sets_of_coeffs = get_sets_coeffs(poly_beziers, Config.NUM_VECTORS, Config.BY_DIST)
    return json.dumps(sets_of_coeffs)


def save(file):
    data = BytesIO(file.file.read())
    image = Image.open(data)
    image.save(f"images/{file.filename}")


def convert_to_svg(file_path: str) -> str:
    filename = get_filename(file_path)
    pnm = f"{filename}.pnm"
    os.system(f"convert {file_path} -background white -alpha remove -alpha off {pnm}")
    filename = get_filename(file_path)
    svg = f"{filename}.svg"
    os.system(f"potrace --flat {pnm} -s -o {svg}")
    os.remove(pnm)
    return svg


def parse_svg(file_path):
    data = get_file_content(file_path)
    paths = SVG(data).parse_path()
    return paths


def compile_polybeziers(paths: list) -> list:
    polys = []
    for path in paths:
        poly = PolyBezier(path)
        polys.append(poly)
    return polys


def get_sets_coeffs(polys: list, num: int, by_dist: bool = False) -> list:
    sets_of_coeffs = []
    for poly in polys:
        calc = Coefficient_calculator(poly, num, by_dist)
        sets_of_coeffs.append(calc.main())
    return sets_of_coeffs



if __name__ == "__main__":
    uvicorn.run("server:app", port=3000)
