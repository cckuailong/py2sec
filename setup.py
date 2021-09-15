from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

install_requires = [
    'cython',
    'pathlib'
]

tests_require = [
]

setup(
    name="py2sec",
    version="0.1.0",
    author="cckuailong",
    author_email="346813862@qq.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms="all",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    packages=find_packages(where=".", exclude=["tests*"]),
    project_urls={
        "Source": "https://github.com/cckuailong/py2sec",
    },
    setup_requires=install_requires,
    tests_require=tests_require,
    include_package_data=True,
    entry_points={
        'console_scripts': ['py2sec=py2sec.py2sec:main']
    }
)
