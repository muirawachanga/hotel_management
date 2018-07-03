from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='hotel_management',
    version=version,
    description='App for managing hotel',
    author='Terester',
    author_email='wachangasteve@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
