import setuptools


with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="transkribus2arche",
    version="0.1.0",
    author="Peter Andorfer",
    author_email="peter.andorfer@oeaw.ac.at",
    description="Scripts and utitlity functions to ingest Transkribus Data into ARCHE",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/acdh-oeaw/transkribus2arche",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=[
        'acdh-arche-assets==3.2.0'
    ]
)