# PyWave
## About
PyWave is a personal project I have undertaken to attempt to build a visual audio spectrum completely contained in the command line interface.

It is currently only operational for Windows Vista and Higher.

![Screenshot of script](https://i.postimg.cc/NGJ2dQnQ/image.png_)

Script will make best attempt to utilize a default device that supports "WASAPI". Will otherwise fail
## Installation
External packages needed
- Numpy
- [This forked](https://github.com/intxcc/pyaudio_portaudio) version of PyAudio that includes loopback support (Windows Vista and higher)

## Running
- Install the above packages
- ```python main.py```
