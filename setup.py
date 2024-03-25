from setuptools import setup

from pypotage import shared


setup(
    name=shared.__proyect__,
    version=shared.__version__,
    author=shared.__author__,
    url=shared.__url__,
    description=shared.__description__,
    license=shared.__license__,
    packages=[shared.__proyect__],
    install_requires=[] # None ;)
)
