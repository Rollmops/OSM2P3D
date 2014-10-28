from setuptools import setup, find_packages, Extension
import glob

setup(name="osm2p3d",
      version="0.1.0",
      author="Erik Tuerke",
      packages = find_packages(),
      data_files=[('imposm/parser/pbf',['imposm/parser/pbf/OSMPBF.pyd'])],
      zip_safe=True
      )