from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='germination-probability',
      version="0.0.1",
      description="Streamlit website to calculate number of seeds needed based on germination rate and desired number of plants.",
      license="MIT",
      author="Emily Cardwell",
      author_email="emily@emilycardwell.com",
      url="",
      install_requires=requirements,
      packages=find_packages())
