# setup.py
from setuptools import setup, find_packages

setup(
    name="olx_api",
    version="0.1.0",
    description="A Python wrapper for the OLX API",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/olx_api",  # if available
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)