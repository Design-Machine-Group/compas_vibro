# COMPAS VIBRO

<!-- ![build](https://github.com/compas-dev/compas/workflows/build/badge.svg) -->
[![GitHub - License](https://img.shields.io/github/license/compas-dev/compas.svg)](https://github.com/Design-Machine-Group/compas_vibro)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/COMPAS.svg)](https://github.com/Design-Machine-Group/compas_vibro)
<!-- [![PyPI - Latest Release](https://img.shields.io/pypi/v/COMPAS.svg)](https://pypi.python.org/project/COMPAS) -->
<!-- [![Conda - Latest Release](https://anaconda.org/conda-forge/compas/badges/version.svg)](https://anaconda.org/conda-forge/compas) -->
<!-- [![DOI](https://zenodo.org/badge/104857648.svg)](https://zenodo.org/badge/latestdoi/104857648) -->

Vibroacoustic modeling of building components via numerical models. 

## Installation

To use `compas_vibro` you need to install COMPAS, and have at least one of the supported analysis backends available on your system. Currently, `compas_vibro` supports ANSYS and OpenSEES to various degrees. 

By installing COMPAS all required Python packages for `compas_vibro` will be installed as well. To install COMPAS, see the Getting Started instructions in the [COMPAS docs] (https://compas.dev/compas/latest/).

`compas_vibro` can be installed using pip from a local source repo, or directly from GitHub. 

Make sure to install `compas_vibro` in the same environment as COMPAS!


### From Local Source

To install `compas_vibro` from a local source repo, clone the repo onto your computer using your Favourite Git client, or using the command line.

Then navigate to the root of the `compas_vibro` repo and install using pip:

```bash
cd compas_fea
pip install -e .
```

### From GitHub

To install directly from the GitHub repo, just do
```bash
$ pip install git+https://github.com/Design-Machine-Group/compas_vibro.git#egg=compas_vibro
```

### Verify

To check the installation, open an interactive Python prompt and import the package.

```bash
>>> import compas
>>> import compas_vibro
```

## License

`compas_vibro` is [released under the MIT license](https://compas.dev/compas/latest/license.html).


