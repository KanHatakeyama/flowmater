from setuptools import setup, find_packages
import sys

sys.path.append('./flowmater')

setup(name='flowmater',
        version='2021.6.19',
        description='PolySMILES',
        long_description="README",
        author='Kan Hatakeyama',
        license="MIT",
        packages = find_packages(),
    )