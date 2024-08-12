from pathlib import Path
from setuptools import setup, find_packages

setup(
    name="comments",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=Path("requirements.txt").open().readlines(),
    py_modules=["comments.cli"],
    entry_points={
        "console_scripts": [
            "comments = comments.cli:cli",
        ],
    },
)
