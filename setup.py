import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="fcast",
    version="0.1.0",
    description="A collection of python tools used for forecasting flood events and their impact on transportation infrastructure.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Dewberry/fcast",
    author="Dewberry",
    author_email="abrazeau@dewberry.com",
    license="Apache License 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["fcast"],
    include_package_data=True,
    install_requires=[
    "gcsfs",
    "xarray",
    "matplotlib",
    "numpy",
    "pandas",
    "scipy",
    "boto3",
    "requests",
    "beautifulsoup4",
    "fiona",
    "shapely",
    ],
)