from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

filename = 'test'
full_filename = 'test.py'
extentions = [Extension(filename, [full_filename])]

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules = cythonize(extentions, language_level=3)
)