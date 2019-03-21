# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='jwt-auth-micro',
    version='0.1.1',
    description='upload oss file',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    author='ivan',
    url='https://github.com/goupper/jwt-auth-micro',
    author_email='chongwuwy@163.com',
    license='MIT',
    packages=find_packages('jwt-auth-micro'),
    include_package_data=False,
    zip_safe=True,
)
