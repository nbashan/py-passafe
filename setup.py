import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="pypassafe",
    version="0.0.1",
    license="MIT",
    description="py-passafe - library for password management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nbashan/py-passafe.git",
    classifieres=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(include=["pypassafe"]),
    python_requires=">=3.8",
    install_requires=[],
)
