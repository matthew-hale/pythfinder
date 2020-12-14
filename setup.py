import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythfinder",
    version="0.7.1",
    author="Matthew Hale",
    author_email="matthew.hale@protonmail.com",
    description="A pathfinder character sheet python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matthew-hale/pythfinder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
