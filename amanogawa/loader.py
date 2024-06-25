from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from dataclasses import dataclass
import devtools as dev
import ftplib
import io
import re
import sys
import codecs
import rich

from rich.progress import Progress

from lxml import etree

from pathlib import Path
import polars as pl


HERE = Path(__file__)
SRCDIR = HERE.parent
ROOTDIR = SRCDIR.parent
DATADIR = Path(ROOTDIR, "data")


def load():
    with ftplib.FTP("ftp.edrdg.org") as ftp:
        welcome = ftp.getwelcome()
        print(welcome)
        login = ftp.login(
            passwd="crumja4@gmail.com",
        )
        print(login)

        cwd = ftp.cwd("/pub/Nihongo")
        print(cwd)

        nlst = ftp.nlst()
        dev.debug(nlst)

        with open(Path(DATADIR, "edicthdr.txt"), "wb") as fp:
            res = ftp.retrbinary("RETR edicthdr.txt", fp.write)
            print(res)


def match_field(element):
    data = {}
    for child in element:
        data[child.tag] = child.text
    return data


def match_root(root):
    for child in root:
        element = {}

        for field in child:
            if field.tag == "ent_seq":
                element["ent_seq"] = field.text
            if field.tag == "k_ele":
                kanji = match_field(field)
                for key, value in kanji.items():
                    element[key] = value
            if field.tag == "r_ele":
                reading = match_field(field)
                for key, value in reading.items():
                    element[key] = value
            if field.tag == "sense":
                sense = match_field(field)
                for key, value in sense.items():
                    element[key] = value

        yield element


def read_xml(file: Path, dtd: Path | None = None):
    is_valid = False

    with open(file, "rb") as xmlfile:
        root = etree.XML(xmlfile.read(), etree.XMLParser())

        if dtd is not None:
            dtd_def = etree.DTD(dtd)
            is_valid = dtd_def.validate(root)
        if is_valid:
            with Progress() as progress:
                task = progress.add_task("Parsing...", total=299739)

                data = []
                for element in match_root(root):
                    progress.update(task, advance=1)
                    data.append(element)

                df = pl.DataFrame(data)
                df.write_csv(Path(DATADIR, "jmdict2.csv"))


if __name__ == '__main__':
    read_xml(Path(DATADIR, "JMdict_e.xml"), Path(DATADIR, "jmdict.did"))
