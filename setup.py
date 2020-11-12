from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open('ixbrlparse/version.py').read())

setup(
    name="ixbrlparse",
    packages=find_packages(),
    version=__version__,
    author="David Kane",
    author_email="david@dkane.net",
    description="A python module for getting useful data out of ixbrl files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drkane/ixbrl-parse",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',
        'lxml',
        'word2number',
    ],
)
