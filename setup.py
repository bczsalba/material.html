from setuptools import setup, find_packages

setup(
    name="material.html",
    version="0.0.0",
    packages=["material"],
    package_data={"material": ["template.css", "index.js"]},
    license="MIT",
    description="Generate MaterialUI websites using Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    url="https://github.com/bczsalba/material.html",
    author="BcZsalba",
    author_email="bczsalba@gmail.com",
    entry_points={
        "console_scripts": [
            "mathml = material.cli:main",
        ]
    },
)
