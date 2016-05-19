# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name='vega',
    version='0.3.0',
    description='An IPython/ Jupyter widget for Vega and Vega-Lite',
    author='Dominik Moritz',
    author_email='domoritz@gmail.com',
    license='BSD-3-Clause',
    url='https://github.com/vega/ipyvega',
    keywords=['data visualization', 'vega', 'vega-lite'],
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    include_package_data=True,
)
