#!/usr/bin/env python3

# from distutils.command.sdist import sdist
from setuptools import find_packages, setup
from setuptools.command.install import install
import subprocess
from pathlib import Path

repo_root_dir = Path(__file__).parent
install_requires = (repo_root_dir / "requirements.txt").read_text().splitlines()

class submodule(install):
    def run(self):
        # self.spawn(["git submodule init; git submodule update"])
        # self.spawn(['ls', '-l'])
        print("hello***************")
        subprocess.call(["ls", "-l"])
        install.run(self)

setup(
    name="asr_abc",
    version="0.1",
    python_requires=">=3.6.0",
    description="An easy introduction of automatic speech recognition",
    author="Liyong Guo",
    license="Apache-2.0 License",
    packages=find_packages(),
    install_requires=install_requires,
    cmdclass = {
        'install':submodule,
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
