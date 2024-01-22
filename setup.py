#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent


PACKAGE_VERSION = "0.1.0"
PACKAGE_NAME = "Circle-Maker"
PACKAGE_AUTHOR = "MohamedRaslan"
PACKAGE_AUTHOR_EMAIL = "MohamedRaslanG@gmail.com"
PACKAGE_REPO_URL = "https://github.com/MohamedRaslan/Circle-Maker"
PACKAGE_DESCRIPTION = "Circle-Maker is a command line application that generates a circle on a 400x400px canvas with a 1px border around it."

with open("readme.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

LONG_DESC_TYPE = "text/markdown"


PKG_REQUIREMENTS = [
    "Pillow == 10.2.0",
]

DEV_REQUIREMENTS = [
    "opencv-python==4.6.0.66",
    "pytest==7.1.2",
    "pytest-dependency==0.5.1",
    "pytest-echo==1.7.1",
    "pytest-cov==3.0.0",
    "pytest-emoji==0.2.0",
    "pytest-html==3.1.1",
    "pytest-icdiff==0.5",
    "pytest-it==0.1.4",
    "pytest-md==0.2.0",
    "pytest-xdist==2.5.0",
]


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author=PACKAGE_AUTHOR,
    author_email=PACKAGE_AUTHOR_EMAIL,
    url=PACKAGE_REPO_URL,
    description=PACKAGE_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    python_requires=">=3.7",
    packages=find_packages(
        where="src",
        include=[
            "*",
        ],
        exclude=[
            "additional",
        ],
    ),
    package_dir={"": "src"},
    install_requires=PKG_REQUIREMENTS,
    extras_require={"dev": DEV_REQUIREMENTS},
    include_package_data=True,
    classifiers=[
        # Complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Utilities",
    ],
    project_urls={
        "Issue Tracker": "https://github.com/MohamedRaslan/Circle-Maker/issues",
    },
    keywords=["circlemaker", "Circle-Maker"],
)
