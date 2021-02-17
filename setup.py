from setuptools import setup


setup(
    name="dicttotreeview",
    version = "1.3",
    author="Elena Grammel",
    author_email="EGrammel@baumer.com",
    url="https://gitlab-doc.baumernet.org/dicttotreeview/21-docstrings/",
    description="From python dictionary to GUI view.",
    packages=["dicttotreeview"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
            "deepdiff==5.0.2",
            "numpy",
            "PyQt5",
        ],
)

