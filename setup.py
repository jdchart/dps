from setuptools import setup
from setuptools import find_packages

long_description= """
# dps
A python package for DPS analysis (dit-par-seconde).
"""

required = [
    "requests", 
    "numpy",
    "moviepy",
    "matplotlib"
]

setup(
    name="dps",
    version="0.0.1",
    description="A python package for DPS analysis (dit-par-seconde).",
    long_description=long_description,
    author="Jacob Hart",
    author_email="jacob.dchart@gmail.com",
    url="https://github.com/jdchart/dps",
    install_requires=required,
    packages=find_packages()
)