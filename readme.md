
# Circle-Maker

Circle-Maker is a python app that create images contains circle.

## Features

- ... TODO

## Installation

You can install "Circle-Maker" locally via **[pip](https://pypi.org/project/pip/)**::

```shell
pip install -e .
```

## Usage

```shell script
python circlemaker.py -d 89 -hue 89 -path test.png
   ```
where:

- `-d` - diameter of the circle
- `-hue` - Hue component of the HSV color (Saturation and Value of the color are always 100%)
- `-path` - output path of the generated image

## Issues

If you encounter any problems, please **[file an issue](https://github.com/MohamedRaslan/Circle-Maker/issues)** along with a detailed description.

## Contributing

Contributions are very welcome.

## Development

To start development, and run test:

run your python environment then run the following commands:

```shell
# Update pip, wheel and setuptools
python -m pip install -U pip wheel setuptools

# Instal all the needed dependencies
pip install -e .[dev]

# Run test
pytest
```

You can check the generated report on the terminal or on the `_autogen` folder
