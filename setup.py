import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LibreView",
    version="0.0.1",
    author="PTST",
    author_email="patrick@steffensen.io",
    description="API interface for LibreView / LibreLinkUp glucose readings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PTST/LibreView_Py",
    packages=setuptools.find_packages(),
    install_requires=["requests >= 2.23.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)