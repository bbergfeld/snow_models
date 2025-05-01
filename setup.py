#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
-----------------------------------------------------------
Script Name: <setup.py>
Description: <DESCRIPTION>
Author: <Bastian Bergfeld>
Email: <bbergfeld@gmx.net>
Date Created: <Fri Apr 25 12:51:18 2025>
-----------------------------------------------------------
"""

from setuptools import setup, find_packages

setup(
    name="snow_models",
    version="0.1.0",
    description="Parametrization functions and models for snow and avalanche research",
    author="Bastian Bergfeld",
    packages=find_packages(),
	install_requires=[
		"numpy>=1.22",
		"uncertainties>=3.2.3"
	],
    python_requires=">=3.7",
)