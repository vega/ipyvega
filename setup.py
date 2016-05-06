# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name='vega',
    version='0.2',
    description='An iPython/ Jupyter widget for Vega and Vega-Lite',
    author='Dominik Moritz',
    author_email='domoritz@gmail.com',
    license='BSD-3-Clause',
    url='https://github.com/vega/ipython-vega',
    keywords='data visualization',
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
)
