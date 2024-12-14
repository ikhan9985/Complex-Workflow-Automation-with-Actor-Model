from setuptools import setup, find_packages

setup(
    name="orchestrator",
    version="0.1",
    packages=find_packages(),
    install_requires=["pykka", "grain1", "grain2"],
)