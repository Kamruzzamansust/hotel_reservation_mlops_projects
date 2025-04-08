from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="MLOPS-PROJECT-1",
    version="0.1",
    author="Kamruzzaman",
    packages=find_packages(), # find pacakges . that means folder contains __init__.py file
    install_requires = requirements,
)

# now in terminal run pip install -e. it will autometically detect setup.py filein our project directory and autometically runs it and start building dependencies