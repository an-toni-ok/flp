# Optimization

This is the optimization used within the flp application.

## Requirements

The requirements can be installed by running the command.

```bash
pip install -r requirements.txt
```

## Usage

### Importing

The optimization can be used by importing it as follows in a script on the same level 

The optimization can be imported in a python script/program thats in the same directory as the optimization package (the directory containing this directory). To import it use the following statement:

```python
from optimization import run_optimization
```

When using the docker containers of this repository this package will be automatically placed at the path backend/server/optimization. In the celery tasks it should therefore be imported with the following statement:

```python
from server.optimization import run_optimization
```

### Executing

To run the optimization, the following code should be used, where output will contain the optimization output and input_file is the path to a JSON file containing the input data.


```python
output = run_optimization(input_file)
```

The input and output data is described in the section [Input and Output data](#input-and-output-data).

## Input and Output data

The input data is required to follow the declaration in [input.json](./input.json) and the output data follows the declaration in [output.json](./output.json).

[input_example](./input_example.json) is an example files of input data.
