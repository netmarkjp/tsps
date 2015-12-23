#!/usr/bin/env python
# coding: utf-8

from logging import DEBUG
from logging import INFO
from logging import StreamHandler
from logging import getLogger
from multiprocessing import Pool
import click
import datetime
import dateutil.parser
import hashlib
import os
import piexif
import re
import shutil

logger = getLogger(__name__)


def find_jpeg_files(root_dir):
    jpeg_ext_pattern = re.compile(".*\.jpe?g$", flags=re.IGNORECASE)
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if jpeg_ext_pattern.match(file):
                yield os.path.join(root, file)


def process_store(jpeg_file, to_dir):
    try:
        exif_dict = piexif.load(jpeg_file)
        if exif_dict and exif_dict.get("Exif") and exif_dict.get("Exif").get(piexif.ExifIFD.DateTimeOriginal):
            exif_datetime_original = exif_dict["Exif"][
                piexif.ExifIFD.DateTimeOriginal]
            try:
                datetime_original = datetime.datetime.strptime(
                    exif_datetime_original, "%Y:%m:%d %H:%M:%S")
            except:
                datetime_original = dateutil.parser.parse(
                    exif_datetime_original)
        else:
            datetime_original = datetime.datetime.fromtimestamp(
                os.stat(jpeg_file).st_mtime)

        YYmm, YYmmdd, YYmmdd_HHMMSS = get_datetime_str(datetime_original)

        md5sum = md5(jpeg_file)

        new_filename = "%s-%s.jpg" % (YYmmdd_HHMMSS, md5sum)

        new_filepath = os.path.join(to_dir, YYmm, YYmmdd, new_filename)
        if os.path.exists(new_filepath):
            logger.info("%s already exist. orig=%s", new_filepath, jpeg_file)
            return

        logger.info("%s -> %s", jpeg_file, new_filepath)
        new_dirpath = os.path.join(to_dir, YYmm, YYmmdd)
        if not os.path.exists(new_dirpath):
            os.makedirs(new_dirpath, mode=0755)
        shutil.copy2(jpeg_file, new_filepath)
    except Exception as e:
        logger.error("%s jpeg_file=%s", e, jpeg_file)


def get_datetime_str(datetime_original):
    YYmm = datetime.datetime.strftime(datetime_original, "%Y%m")
    YYmmdd = datetime.datetime.strftime(datetime_original, "%Y%m%d")
    YYmmdd_HHMMSS = datetime.datetime.strftime(
        datetime_original, "%Y%m%d_%H%M%S")
    return (YYmm, YYmmdd, YYmmdd_HHMMSS)


def md5(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()


def set_debug():
    for handler in logger.handlers:
        logger.removeHandler(handler)
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)


@click.command()
@click.option("-f", "--from_dir", required=True)
@click.option("-t", "--to_dir", required=True)
@click.option("-d", "--debug", is_flag=True, default=False)
@click.option("-p", "--processes", default=20)
def tsps(from_dir, to_dir, debug, processes):
    if debug:
        set_debug()
    pool = Pool(processes=processes)
    for jpeg_file in find_jpeg_files(from_dir):
        logger.debug("=> %s", jpeg_file)
        pool.apply_async(process_store, (jpeg_file, to_dir))
    pool.close()
    pool.join()

if __name__ == "__main__":
    handler = StreamHandler()
    handler.setLevel(INFO)
    logger.setLevel(INFO)
    logger.addHandler(handler)
    tsps()
