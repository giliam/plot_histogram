import os
import argparse

from pdf2image import convert_from_path, convert_from_bytes

basedir = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="the file to convert")
args = parser.parse_args()
print("Works on", args.filename)

file_stem = args.filename[::-1].split(".", 1)[1][::-1]

pages = convert_from_path(args.filename, 500)

for i, page in enumerate(pages):
    print(f"Saving {file_stem}_{i:03d}.jpg")
    page.save(f"{file_stem}_{i:03d}.jpg", "JPEG")
