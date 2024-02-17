import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1' 
PACKAGE_NAME = 'odoo_db_restore' 
AUTHOR = 'Alejandro Minor' 
URL = 'https://github.com/alejandrominor' 

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    url=URL,
    packages=find_packages(),
    include_package_data=True
)
