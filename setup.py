# !/usr/bin/env python
# _*_ coding: utf-8 _*_

"""
构建工具
    使用方式：
        python setup.py install

"""

from setuptools import setup, find_packages

setup(
    name="netease_music",
    version="2.0",
    author="humingk",
    keywords=["netease", "music", "comment"],
    packages=find_packages(exclude=("test.*",)),
    package_data={
        "": ["*.conf"],         # include all *.conf files
    },
    install_requires=[
        "pybloom_live>=2.3.0",  # pybloom-live, fork from pybloom
        "requests>=2.18.0",     # requests, http for humans
    ]
)