# Behavior Annotator

![Alt text](https://github.com/hsingchien/Bannotator/blob/main/src/bannotator/resources/bg_readme.png?raw=true)

# Table of contents

- [Installation](#installation)
- [Usage](#usage)
  - [GUI](#GUI)
  - [Video](#video)
  - [Annotation](#annotation)
  - [KeyPress Functions](#keypress-functions)
- [Contributing](#contributing)
- [Acknowledgement](#acknowledgement)
- [License](#license)

# Installation
```bash
pip install bannotator
```
Open GUI
```bash
annotate-behavior
```

# Usage

### GUI

![Alt text](https://github.com/hsingchien/Bannotator/blob/main/src/bannotator/resources/app_illustration.png?raw=true)

The GUI layout has 5 major areas.

- Video display area, where you can add multiple videos.
- Stream area shows the enlarged portion of the color coded streams.
- Stream overviews provide the bird's-eye view of the full annotation and the current progress.
- Behavior table dock where ID, name, keystroke and color are shown in the Behaviors tab; number of epochs and percentage of the time are shown in the Stats tab.
- Epoch tables where epochs are shown in the All Epochs tab, epochs of selected behaviors are shown in the Behavior Epochs tab.

### Video

- Annotator supports major video formats and the Norpix Streampix seq files. Only uncompressed seq (RAW) or compressed seq in JPEG format are currently supported.

- Annotator is capable of displaying multiple videos simultaneously, therefore is great for experiments with multiple video streams. If videos have different number of frames, the 1st added video is treated as the main video and the other videos are stretched to the length of the video 1.

- Annotator provides several different video layouts. Side by side, Stacked or Grid (this option becomes available when number of videos reaches 4).

- Video can be played at various speed.

### Annotation

The annotator is compatible with the format of annotation txt file of [Piotr's MATLAB toolbox](https://github.com/pdollar/toolbox). If you are a user of the behavior annotator of this toolbox, you can view/edit your existing annotation files as well as keep using your configuration files to create new annotations. The output annotation txt files are also back compatible with Piotr's annotator.

If you do not have configuration files to start with, you can create an new annotation from scratch using `New annotaion` dialog in the `Annotation` menu. To enable this option you need to add a video first so that the annotator knows the length of the annotation.

![Alt text](https://github.com/hsingchien/Bannotator/blob/main/src/bannotator/resources/new_annotation_dialog.png?raw=true)

First, set the number of streams. In the text editor, input behavior - keystroke pair in each line, parsed by '-' or space. The dialog actively checks the input to ensure the behavior-keystroke pairs are unique. Once created, all the streams will be initialized with the first behavior in your list. Usually the first behavior label is reserved for the blank label of name "other" or "blank", which will be assigned grey color.

Once the new streams are created, go through the video and label the events. Press keystroke to label the current frame as well as the rest of the Epoch.

`Epoch` is the fundamental unit of the annotation. An `Annotation` contains `Streams` which contains a series of `Epoch`. Each `Stream` also contains several `Behavior` objects each one of which stores name, color, keystroke and ID of a user defined behavior. `Behavior` objects also collects all the `Epochs` of this kind in its stream.

### KeyPress Functions

<kbd>Space</kbd> : Play/Pause video

<kbd>&#8593;</kbd> / <kbd>&#8595;</kbd> : Increase/Decrease playing speed

<kbd>&#8592;</kbd> / <kbd>&#8594;</kbd> : Previous/Next frame

<kbd>1</kbd> - <kbd>0</kbd> : Change the current stream to stream 1 - 10

<kbd>`</kbd> : Rotate current stream through all streams

<kbd>-</kbd>/<kbd>+</kbd> : Move to previous/next epoch of current stream

<kbd>CTRL</kbd><kbd>-</kbd>/<kbd>CTRL</kbd><kbd>+</kbd> : Move to previous/next epoch of selected behavior

# Contributing

Your contributions are always welcome! Contribution guideline will be available soon.

# Acknowledgement

This project is inspired by [Piotr's MATLAB toolbox](https://github.com/pdollar/toolbox).

Seq file reading is inspired by [PIMS](https://github.com/soft-matter/pims).

Random color generator [distinctipy](https://github.com/alan-turing-institute/distinctipy)

The project is built with [PySide6](https://doc.qt.io/qtforpython-6/index.html#).

# License

The MIT License (MIT) 2017 - [Xingjian Zhang](https://github.com/hsingchien/).
