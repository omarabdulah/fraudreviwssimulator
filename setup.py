from setuptools import setup, find_packages

setup(
    name="fraudreviwssimulator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "faker",
        "transformers",
        "torch",
        "numpy",
        "jinja2",
        "python-dateutil"
    ],
    entry_points={
        "console_scripts": [
            "fraudreviwssimulator = main:main"
        ]
    },
)