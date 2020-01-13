#!/usr/bin/env python
from setuptools import setup, find_packages
from os import environ

setup(
  name="TankTourneyClient",
  version="0.0.3",
  package_dir={"": "src"},
  packages=find_packages("src"),
  include_package_data=True,
  install_requires=[
    "docopt==0.6.2",
    "pygame==1.9.6",
  ],
)
