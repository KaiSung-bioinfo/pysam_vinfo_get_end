import os, glob
from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
import pysam

# Retrieve the pysam dependencies
## Get include path
incl = pysam.get_include()
## Find htslib shared library
htslib_pattern = os.path.join(incl[0], "libchtslib.*")
htslib_files = [ f for f in glob.glob(htslib_pattern)\
                if f.endswith(".so") or f.endswith(".dylib") ]
if not htslib_files:
    raise RuntimeError("Could not find the htslib shared library")
htslib = os.path.basename(htslib_files[0])
## Extract library name without 'lib' prefix and '.so' suffix
htslib_name = htslib[3:htslib.rfind(".")]


# Define the Cython extension module
# We use pysam's API to get the correct include and library paths
extensions = [
    Extension(
        "pysam_vinfo_get_end",
        ["pysam_vinfo_get_end.pyx"],
        include_dirs = incl,
        libraries = [htslib_name],
        library_dirs = incl,
        runtime_library_dirs = incl
    )
]

# The main setup function
setup(
    name = 'pysam_vinfo_get_end',
    version = '0.1.0',
    description = "A Cython module to get the 'END' field from a VCF record's INFO field using pysam.",
    long_description = open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type = "text/markdown",
    author = "Kai Sung",
    author_email = "aleksei@foxmail.com",
    url = "https://github.com/KaiSung-bioinfo/pysam_vinfo_get_end",
    license = "GPLv3",
    # Cythonize the extension modules
    ext_modules = cythonize(
        extensions,
        compiler_directives={'language_level': "3"},
        quiet=True
    ),
    # Build-time and Run-time dependencies
    python_requires = '>=3.8',
    install_requires = ['pysam'],
    # Dependencies needed for the setup.py script itself to run
    setup_requires = [
        'cython',
        'pysam',
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    zip_safe = False,
)
