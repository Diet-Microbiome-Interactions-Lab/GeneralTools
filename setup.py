import glob
print([script for script in glob.glob('GT_Bin/*')])
import os
import sys
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


init_py_path = os.path.normpath(os.path.dirname(
    os.path.abspath(__file__))) + '/GeneralTools/__init__.py'
# Grab the version
version_string = [i.strip() for i in open(init_py_path).readlines()
                  if i.strip().startswith('mypackage_version')][0]
mypack_version = version_string.split("'")[1].split('-')[0]


# Ensure the user is using python version >= 3
try:
    if sys.version_info.major != 3:
        sys.stderr.write(
            f"Your python version is not >= 3. You version is {sys.version_info.major}.")
        sys.exit(-1)
except Exception:
    sys.stderr.write("Failed to determine what python version is being used.")

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


# Set up the package.
setup(
    name="DaneGeneralTools",
    version=mypack_version,
    author="Dane Deemer",
    author_email="ddeemer@purdue.edu",

    description="General bioinformatics tools",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/ddeemerpurdue",

    scripts=[script for script in glob.glob('bin/*')],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'bio',
        'matplotlib',
        'numpy',
        'pandas',
        'pyyaml==6.*',
        'python-json-logger==2.0.7',
    ],
    python_requires='>=3.6',
    entry_points={'console_scripts': ['fileflux=GeneralTools.FileClasses.main:cli']}
)
