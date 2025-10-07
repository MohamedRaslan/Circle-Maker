

[![GitHub stars](https://img.shields.io/github/stars/MohamedRaslan/Circle-Maker)](https://github.com/MohamedRaslan/Circle-Maker/stargazers) [![GitHub forks](https://img.shields.io/github/forks/MohamedRaslan/Circle-Maker)](https://github.com/MohamedRaslan/Circle-Maker/network) [![GitHub issues](https://img.shields.io/github/issues/MohamedRaslan/Circle-Maker)](https://github.com/MohamedRaslan/Circle-Maker/issues) [![GitHub Release Date](https://img.shields.io/github/release-date/mohamedraslan/Circle-Maker)](https://github.com/MohamedRaslan/Circle-Maker/releases) [![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/mohamedraslan/Circle-Maker)](https://github.com/MohamedRaslan/Circle-Maker)

# Circle-Maker

Circle-Maker is a command-line application that generates a circle on a 400x400px canvas with a 1px border around it.


## Features

Circle-Maker is a command-line application that generates a circle on a 400x400px canvas with a 1px border
around it. Size and color of the circle can be set via command line arguments, the thickness of the border is fixed and
cannot be changed, however color of the border is random and changes on every application launch.

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

To start development and run tests:

Run your Python environment, then run the following commands:

```shell
# Update pip, wheel, and setuptools
python -m pip install -U pip wheel setuptools

# Install all the needed dependencies
pip install -e .[dev]

# Run test
pytest
```

You can check the generated report on the terminal or on the `_autogen` folder


## Assumptions and Limitations
Listed below are a list of my Assumptions/statements and enhancements:

- Statements: I didn't use or found a ready to use tool to make me able to detect circles in the image, so I tried to create a way to detect this using CV2 "Disclaimer: despite that all of the code in this repo is done by me and me only a lot of the work came by searching google for a detecting circles, trial & error, troubleshooting and tuning .. so it's not an elegant solution, but work very well with the current situation of the `Circle-Maker` app".

- Assumptions: The circle detector will work very well under the following assumptions, "but note that some circle detection methods may be able to work outside the following assumption or with few modifications":
  - The circle will have only one color
  - The circle center is always the center of the image
  - The scope of testing is the circle, so I can ignore the border of the image.

- Limitations: There are some limitations with my circle detectors. "There are three implemented methods of detecting the circle, each method lists its limitation under it, and only the best oneis  used for detection," but generally
  - Circles with a diameter less than 5px can't be detected properly, so unfortunately, I ignored them and treated them as not existing.

- Enhancements: In the `circlemaker.py` in the `src` folder, to make the circle does not overlap with the image border
  - The `-d` - diameter of the circle should be within [0 (400-2)] "[0 398]", not [0 399] as the border takes 1px on each side, so the border takes about 2 pixels.


