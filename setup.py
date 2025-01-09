from setuptools import setup, find_packages

setup(
    name="fandango-fuzzer",  # This is the name of your package
    version="0.1.0",  # Make sure to update the version with each release
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here, e.g. 'requests', 'numpy', etc.
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
