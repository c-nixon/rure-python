#!/usr/bin/env python
from __future__ import print_function
import os
from setuptools import setup
from setuptools.command import build_ext

from rust_ext import build_rust_cmdclass, install_lib_including_rust


cur_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cur_dir, 'README.rst')) as buf:
    README = buf.read()
rure_dir = os.getenv('RURE_DIR', cur_dir)

target_dir = os.getenv("CARGO_TARGET_DIR")

files = [os.path.sep.join((root, f))
        for root, dirs, files in os.walk(target_dir)
        for f in files
        if (f in ["librure.so", "librure.a"] and 
            root.split(os.sep)[-1] == "release")]

if not len(files):
    cmdclass={
        'build_rust': build_rust_cmdclass(rure_dir + '/regex/regex-capi/Cargo.toml'),
        'install_lib': install_lib_including_rust
    }
else:
    cmdclass = {}

setup(
    name='rure',
    version='0.1.2',
    author='David Blewett',
    author_email='david@dawninglight.net',
    description=('Python bindings for the Rust `regex` create. '
                 'This implementation uses finite automata and guarantees '
                 'linear time matching on all inputs.'),
    long_description=README,
    license='MIT',
    keywords=['regex', 'rust', 'dfa', 'automata', 'data_structures'],
    url='https://github.com/davidblewett/rure-python',
    setup_requires=[
        'cffi>=1.5.0',
        'rust-ext>=0.1',
        ],
    install_requires=['cffi>=1.5.0', 'six'],
    cmdclass=cmdclass,
    cffi_modules=['rure/_build_ffi.py:ffi'],
    packages=['rure', 'rure.tests'],
    package_dir={'rure': 'rure'},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Text Processing :: Indexing']
)
