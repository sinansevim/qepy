"""
Sample setup.py file
"""
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name="espresso_machine",
    version='{{VERSION_PLACEHOLDER}}',
    author="Susy Exists",
    author_email="susy@selectron.me",
    description = "Quantum Espresso automation tool",
    url = "https://github.com/susyexstsi/espresso-machine",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[  "numpy",
  "matplotlib",
  "pandas",
  "qcelemental",
  "ase",
  "Flask",
  "qe-tools",
  "scipy",
  "seekpath",
  "untangle",
  "tools_barebone",
  "ipykernel",
  "ipython"],
    keywords=['pypi', 'cicd', 'python'],
    classifiers=[
"Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",]
)