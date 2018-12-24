from setuptools import setup
import os.path

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.7",
]

setup(
    name="osbpy",
    version="3.0.1",
    packages=['osbpy'],
    include_package_data=True,
    install_requires=[
        'matplotlib>=3.0.2',
        'numpy>=1.15.4',
        'scipy>=1.1.0'
    ],
    author="Jiri Olszar",
    author_email="remiliass@gmail.com",
    description="Simple library for osu! storyboarding",
    long_description=open(
        os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    classifiers=classifiers,
    license="MIT",
    keywords="graphics audio rhythm game",
    url="https://github.com/KawaiiWafu/osbpy",
    python_requires=">=3",
)
