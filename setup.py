from setuptools import setup, find_packages

setup(
    name="repository_mongodb",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "pymongo>=4.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-asyncio>=0.21.0",
        ],
    },
    python_requires=">=3.8",
    author="Ryan Zheng",
    author_email="ryan.zheng.work@gmail.com",
    description="A small library to simplify MongoDB usage with repository pattern",
    long_description=open("README.MD").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ryan-zheng-teki/repository_mongodb",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    package_data={
        "repository_mongodb": ["py.typed"],
    },
)