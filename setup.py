#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = \
''' blah '''


setup(
    name='fcctx_caller_agreement',
    version='0.1.0.0',
    author='Bernie Pope',
    author_email='bjpope@unimelb.edu.au',
    packages=['fcctx_caller_agreement'],
    package_dir={'fcctx_caller_agreement': 'fcctx_caller_agreement'},
    entry_points={
        'console_scripts': ['callagree = fcctx_caller_agreement.callagree:main']
    },
    url='https://github.com/bjpop/fcctx_caller_agreement',
    license='LICENSE',
    description=('blah'),
    long_description=(LONG_DESCRIPTION),
    install_requires=["networkx", "intervaltree"],
)
