# setup.py

from setuptools import setup, find_packages

setup(
    name='pysniffer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Dhananjay Haridas',
    author_email='main.dhananjayharidas@gmail.com',
    description='A decorator for profiling Python functions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DhananjayanOnline/pysniffer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
