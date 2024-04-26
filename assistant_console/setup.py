"""Package Configuration"""

from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fd:
    long_description = fd.read()

setup(
    name="pa_quadro",
    version="1.1.19",
    description="Personal assistant for managing contacts and notes",
    long_description=long_description,
    url="https://github.com/Matajur/personal_assistant",
    author="Project Team Quadro",
    author_email="project_team.quadro@gmail.com",
    license="Apache License 2.0",
    packages=find_namespace_packages(),
    install_requires=['setuptools>=69.2.0'],
    entry_points={"console_scripts": ["qbot = pa_quadro.main:main"]},
    classifiers=["Programming Language :: Python :: 3"],
    include_package_data=True,
    package_data={"": ["*.txt"]}
)
