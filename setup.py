#!/usr/bin/env python3

import os
from setuptools import find_packages, setup
from setuptools.command.install import install
from pathlib import Path

repo_root = Path(__file__).parent
install_requires = (repo_root / "requirements.txt").read_text().splitlines()


class submodule(install):
    def run(self):
        install.run(self)
        os.system("git submodule init; git submodule update")


setup(
    name="asr_abc",
    version="0.1",
    python_requires=">=3.6.0",
    description="An easy introduction of automatic speech recognition",
    author="Liyong Guo",
    license="Apache-2.0 License",
    packages=find_packages(),
    install_requires=install_requires,
    cmdclass={
        "install": submodule,
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering :: Speech Recognition",
        "Typing :: Typed",
    ],
)
