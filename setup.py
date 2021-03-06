from setuptools import setup, find_packages

def read(filename):
    return [rq.strip() for rq in open(filename).readlines()]

setup(
name='blog-api',
version='0.1.0',
description='Blog API app',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read('requirements.txt'),
    extras_require={
        'dev': read('requirements-dev.txt')
    }
)
