# UML

In this directory the UML diagrams used in the documentation are stored in text format. To generate the diagrams from the files PlantUML is used.

The PlantUML files are in the [src](./src/) directory and the generated images in the [images](./images/) folder.

## Contents

- [UML](#uml)
  - [Contents](#contents)
  - [Setup](#setup)
  - [Live preview](#live-preview)
  - [Image generation](#image-generation)


## Setup

Installation instructions for IDE integrations can be found on [this webpage](https://plantuml.com/de-dark/starting) in the section **PlantUML Integration Capabilities**, but there's also a [setup guide](https://gist.github.com/GAM3RG33K/cc59290e8fe68d61c7ab2540f8471fd3).

Installing and setting up plantuml is not strictly necessary, there are websites like [this one](https://www.planttext.com/) that can di the same.

## Live preview

If you're editing the plantuml diagrams in VSCode, you can activate a live preview of the currently selected diagram by pressing `Alt + D` (VSCode).

## Image generation

**VSCode**

To generate an image from the plantuml file in VSCode, you can press the key combination `CTRL + SHIFT + P` to open up. Now search for `PlantUML: Export Current Diagram` and select the option. Select the desired output format and it will be generated for you.

**Other**

If you're not using VSCode you can follow [this guide](https://gist.github.com/GAM3RG33K/cc59290e8fe68d61c7ab2540f8471fd3) for instructions on using plantuml from the command line to generate images.
