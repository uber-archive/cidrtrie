#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="cidrtrie",
    version="0.0.1",
    author="James Brown",
    author_email="jbrown@uber.com",
    license="MIT",
    packages=find_packages(exclude=['tests']),
    test_suite="nose.collector",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ]
)
