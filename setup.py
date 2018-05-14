from setuptools import setup, find_packages

setup(
    name='slimleaf',
    version="1.0.0",
    author="Brandon Blair",
    author_email="cbrandon.blair@gmail.com",
    url="https://github.com/brandonblair/slimleaf",
    description="A sensible approach to fast, scalable, robust UI automation suites in Python",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "Appium-Python-Client",
        "lxml",
        "cssselect",
        "pymysql",
    ]
)
