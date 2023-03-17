import os
import json

from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from utils import *
from config import Config
from svg import SVG
from bezier import PolyBezier
from coeff import Coefficient_calculator
from complex_vector import ComplexVector

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
    save_image(file)
    file_path = os.path.join(Config.IMAGE_PATH, file.filename)
    if get_extension(file.filename) != "svg":
        svg_path = convert_to_svg(file_path)
    else:
        svg_path = file_path
    paths = parse_svg(svg_path)
    poly_beziers = compile_polybeziers(paths)
    num_bez = get_num_bez(poly_beziers)
    sets_of_coeffs = get_sets_coeffs(poly_beziers, Config.NUM_VECTORS, Config.BY_DIST)
    sets_of_compVectors = get_sets_compVec(sets_of_coeffs)
    frames = get_frames(sets_of_compVectors, num_bez)
    print("COMPLETE")
    return json.dumps(frames)


def save_image(file):
    with open(os.path.join("images", file.filename), "wb") as f:
        f.write(file.file.read())


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


def get_num_bez(polybeziers):
    num = 0
    for polybezier in polybeziers:
        num += len(polybezier)
    return num


def get_sets_coeffs(polys: list, num: int, by_dist: bool = False) -> list:
    sets_of_coeffs = []
    for poly in polys:
        calc = Coefficient_calculator(poly, num, by_dist)
        sets_of_coeffs.append(calc.main())
    return sets_of_coeffs


def get_sets_compVec(sets_of_coeffs: list) -> list:
    sets_of_compVecs = []
    for coeffs in sets_of_coeffs:
        sets_of_compVecs.append(create_compVectors(coeffs))
    return sets_of_compVecs


def create_compVectors(coefficients):
    index = len(coefficients) // 2 - (len(coefficients) % 2 == 0)
    compVectors = []
    for i in range(len(coefficients)):
        key = list(coefficients.keys())[index]
        coeff = coefficients[key]
        compVector = ComplexVector(coeff, key)
        compVectors.append(compVector)
        index += (-1) ** (i % 2 != 0) * (i + 1)
    return compVectors


def get_frames(sets_of_compVec, num_bez):
    frames = []
    time_lim = 1
    for t in arange(0, time_lim, Config.DT):
        frames.append(compile_frame(sets_of_compVec, t))
    return frames


def compile_frame(sets_of_compVec: list, t) -> list:
    frame = []
    for set_of_compVec in sets_of_compVec:
        vectors_and_magnitudes = []
        for compVec in set_of_compVec:
            f_of_t = compVec.func(t)
            vectors = [f_of_t.real, f_of_t.imag]
            magnitude = abs(f_of_t)
            vectors_and_magnitudes.append([vectors, magnitude])
        frame.append(vectors_and_magnitudes)
    return frame


if __name__ == "__main__":
    uvicorn.run("server:app", port=3000)
