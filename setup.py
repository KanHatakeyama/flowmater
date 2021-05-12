from setuptools import setup, find_packages
import sys

sys.path.append('./flowmater')

setup(name='flowmater',
        version='2021.5.12',
        description='PolySMILES',
        long_description="README",
        author='Kan Hatakeyama',
        license=license,
        packages = find_packages(),
    )