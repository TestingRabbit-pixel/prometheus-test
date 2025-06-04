from setuptools import setup, find_packages

setup(
    name='prometheus_test',
    version='0.1.0',
    packages=find_packages(include=['prometheus_test', 'src']),
    install_requires=[
        'pytest',
    ],
)