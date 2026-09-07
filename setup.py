#!/usr/bin/env python3
#  Copyright (c) 2023 Direkt Embedded Pty Ltd
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Pip setup file used to create a package for robotframework-labjack
"""

import setuptools
import os

current_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_path, 'LabJackLibrary', 'VERSION')) as version_file:
    VERSION = version_file.read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robotframework-labjack",
    version=VERSION,
    description="LabJackLibrary, is a library for Robot Framework and wraps LabJackPython from LabJack Corporation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={'LabJackLibrary': ['VERSION']},
    url="https://www.direktembedded.com",
    license_files=("LICENSE", "NOTICE"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'LabJackPython>=2.1'
    ],
    python_requires='>=3.8',
)

# python -m pip install --user --upgrade setuptools wheel
# python setup.py sdist bdist_wheel
