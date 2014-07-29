#!/usr/bin/env python

import os
import sys
import usfs

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'usfs'
]

requires = ['fusepy']

with open('README.rst') as f:
    readme = f.read()

setup(
    name='usfs',
    version=usfs.__version__,
    description='USFS Shared FileSystem',
    long_description=readme,
    author='Tristan Fisher',
    author_email='code@tristanfisher.com',
    url='http://github.com/tristanfisher/',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'usfs': 'usfs'},
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ),
)
