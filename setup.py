from setuptools import setup, find_packages


setup(
    name="py4lab",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["py4lab = PFTL.start:main"]
    },
    install_requires=[
        "matplotlib",
        "pyyaml",
        "pyserial",
        "PyQt5",
        "numpy",
        "pyqtgraph",
    ]
)
