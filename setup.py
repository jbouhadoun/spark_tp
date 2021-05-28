from setuptools import setup, find_packages
setup(
    name="Job",
    version="0.0.1",
    # package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[
        "docutils>=0.3"
        ],
    extras_require = {
        'dev': [
            "pylint==2.4.4"
            ],
        'test': [
            "pytest==5.3.1"
            ]
        },
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst"],
        # And include any *.msg files found in the "job" package, too:
        "job": ["*.msg"],
        },
    # metadata to display on PyPI
    author="",
    author_email="",
    description="This is a template Package used to submit PySpark job",
    long_description_content_type="text/markdown",
    url="https://",# Git url    
    classifiers = [
        "Programming Language :: Python :: 3.6"
        ],
)