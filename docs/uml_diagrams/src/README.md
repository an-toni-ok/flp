# UML Diagrams <!-- omit in toc -->

In this directory source files for UML diagrams can be found.
The source files are created for plantuml, which be used to generate images from it.

## Contents <!-- omit in toc -->

- [Usage](#usage)
- [Conventions](#conventions)
- [Directory contents](#directory-contents)


## Usage

If you're using vscode to generate images from a plantuml file in this directory, the generated image will be placed in the [images](../images/) directory and the name of the generated image will be the one specified in the .plantuml file directly after the `@startuml`.

To give an image the title "Infrastructur_Deployment", your plantuml file should start like this:

```
@startuml Infrastructur_Deployment
```

Check out this [link](https://plantuml.com/) for an introduction to creating UML (or non UML) diagrams with plantuml.

## Conventions

- Use the same name for the .plantuml file and the image so that you don't have to look through every plantuml file to find the corresponding image.
- Do not use Spaces in the names, instead use underscores.
- Capitalize the first word of the name.
- Add a short description of any newly created diagram to the [directory contents](#directory-contents) section.

## Directory contents

| Name | Diagram Type | Content |
| - | - | - | 
| [Backend_Whitebox](./Backend_Whitebox.plantuml) | component | The components of the top-level of the backend. |
| [Frontend_Whitebox](./Frontend_Whitebox.plantuml) | component | The components of the frontend. |
| [Infrastruktur](./Infrastruktur.plantuml) | deployment | The nodes of the complete infrastructure with interactions. |
| [Data_setting_activity](./Data_setting_activity.plantuml) | activity | The process of setting the input data. |
| [Optimization_run_activity](./Optimization_run_activity.plantuml) | activity | The process of running the optimization and getting the result of the optimization. |
| [Process_context](./Process_context.plantuml) | deployment | The application and it's neighbors (the user and the optimization software). |
| [System_Whitebox](./System_Whitebox.plantuml) | component | The components of the top-level of the complete application. |
| [Technical_context](./Technical_context.plantuml) | deployment | The connections between the application parts and it's neighbors (the user and the optimization software). |

