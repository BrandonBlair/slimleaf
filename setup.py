from setuptools import setup, find_packages

setup(
    name='slimleaf',
    version="1.0.0",
    summary="A sensible approach to fast, scalable, robust UI automation suites in Python",
    description="README.md",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "Appium-Python-Client",
        "lxml",
        "cssselect",
        "pymysql",
    ]
)
