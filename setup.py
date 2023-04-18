from setuptools import setup, find_packages

import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="bannotator",
    version="0.1.0",
    author="Xingjian Zhang",
    description="A GUI application to annotator animal behavior videos",
    packages=find_packages(),
    project_urls={"Source Code": "https://github.com/hsingchien/Bannotator"},
    entry_points={"console_scripts": ["annotate-behavior=bannotator.bannotator:main"]},
    python_requires="==3.9",
)