#!/usr/bin/env python3

from setuptools import setup

setup(
    name="findlike",
    version="0.1",
    author="Bruno Arine",
    author_email="bruno.arine@runbox.com",
    packages=["findlike"],
    url="http://www.github.com/brunoarine/findlike",
    license="LICENSE.txt",
    description="findlike is a package to retrieve similar documents",
    long_description=open("README.org").read(),
    package_data={'': ['*.txt', 'findlike/*.txt']},
    entry_points="""
        [console_scripts]
        findlike=findlike.cli:cli
    """,
    include_package_data=True,
    install_requires=[
    ],
)
