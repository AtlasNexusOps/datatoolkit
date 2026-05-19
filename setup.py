from setuptools import setup, find_packages

setup(
    name="atlas-datatoolkit",
    version="0.1.0",
    description="CLI for converting, validating, cleaning and batching data (JSON ↔ CSV ↔ YAML ↔ XML)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Atlas Nexus",
    author_email="dev@atlasnexus.tech",
    url="https://github.com/AtlasNexusTech/datatoolkit",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=["pyyaml>=6.0", "xmltodict>=0.13"],
    entry_points={
        "console_scripts": [
            "datatoolkit=datatoolkit.cli:main",
            "dtk=datatoolkit.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Utilities",
    ],
    keywords="cli data csv json yaml xml convert validate clean",
)
