#!/usr/bin/env python

import codecs
import os
from setuptools import find_packages, setup

with open(os.path.join("rudicsreroute","__init__.py"), "r") as fh:
    while True:
        line = fh.readline()
        if line.startswith("__version__"):
            VERSION = line.split("=")[1].strip().replace('"','').replace("'",'')
            break

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf8') as fh:
    long_description = fh.read()


#scripts = ['']

setup(
    name='rudicsreroute',
    version=VERSION,
    description='Port rerouter for rudics connections',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/smerckel/rudicsreroute',
    author='Lucas Merckelbach',
    author_email='lucas.merckelbach@hereon.de',
    license='MIT',
    packages=['rudicsreroute'],
    #packages=find_packages(where='.', exclude=['tests', 'docs'])
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['ocean gliders', 'glider flight', 'oceanography'],
    #install_requires=install_requires,
    include_package_data=True,
    entry_points = {'console_scripts':['rudicsreroute = rudicsreroute.rudicsreroute:main'],
                    'gui_scripts':[]}
)
