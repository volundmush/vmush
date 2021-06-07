import os
import sys
from setuptools import setup, find_packages

os.chdir(os.path.dirname(os.path.realpath(__file__)))

OS_WINDOWS = os.name == "nt"


def get_requirements():
    """
    To update the requirements for vmush, edit the requirements.txt file.
    """
    with open("requirements.txt", "r") as f:
        req_lines = f.readlines()
    reqs = []
    for line in req_lines:
        # Avoid adding comments.
        line = line.split("#")[0].strip()
        if line:
            reqs.append(line)
    return reqs


def get_scripts():
    """
    Determine which executable scripts should be added. For Windows,
    this means creating a .bat file.
    """
    if OS_WINDOWS:
        batpath = os.path.join("bin", "windows", "vmush.bat")
        scriptpath = os.path.join(sys.prefix, "Scripts", "vmush_launcher.py")
        with open(batpath, "w") as batfile:
            batfile.write('@"%s" "%s" %%*' % (sys.executable, scriptpath))
        return [batpath, os.path.join("bin", "windows", "vmush_launcher.py")]
    else:
        return [os.path.join("bin", "unix", "vmush")]


from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# setup the package
setup(
    name="vmush",
    version="0.0.1",
    author="Volund",
    maintainer="Volund",
    url="https://github.com/volundmush/vmush",
    description="",
    license="???",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=get_requirements(),
    packages=["vmush"],
    zip_safe=False,
    scripts=get_scripts(),
    classifiers=[

    ],
    python_requires=">=3.7",
    project_urls={
        "Source": "https://github.com/volundmush/vmush",
        "Issue tracker": "https://github.com/volundmush/vmush/issues",
        "Patreon": "https://www.patreon.com/volund",
    },
)
