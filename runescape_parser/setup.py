from setuptools import setup, find_packages

setup(
    name='runescape_parser',
    version='0.1.0',
    author='Joshua Gorin',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    description='Scraper for Analyzing Runescape Market Data.'
)