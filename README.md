# Weaving Analyser Test



This project consists of a simple weaving analyser application, leveraging a firmware interface to simulate a real environment. The program gets images (from simulated camera controllers) and surface velocity (from simulated velocity controllers), and sends them to a server for data analysis. The specification is available [here](https://github.com/Caio-Nogueira/Weaving-test/blob/main/README.md).


## Usage

There is no need to install additional dependencies that did not exist in the template. As such, to run the application, make sure to run the server first with the following command (in the root of the directory):

```shell
python3 server/server.py
```



With the server up and running, you can run the application:

```shell
python3 weaving_analyser/application.py
```



Finally, to run all unit tests, use the following command:

```shell
python3 -m unittest discover -s tests -p '*_test.py'
```

## Directory Structure

This is the general structure of the directory. The `/tests` contains unit tests. The code is located under the `/weaving_analyser` directory. 

```lua
weaving-test-master/
|-- tests/
|   |-- api_handler_test.py
|   |-- camera_handler_test.py
|   |-- velocity_handler_test.py
|   |-- weaving_analyser_test.py
|
|-- weaving_analyser/
|   |-- application.py
|   |-- analyser.py
|   |-- camera_handler.py
|   |-- config.py
|   |-- velocity_handler.py
|   |-- errors/
|   |   |-- pictures_not_collected_error.py
|
|-- README.md
|-- Specification.md
|-- ...


```
