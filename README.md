# Carbon Calculation#

Package calculate carbon adj

### Run Local as package ###

* Try and running the setup.py file within your terminal and see if it installs the package correctly.
  ```shell script
    python setup.py install
  ```
  and then run command what is in setup.py console_scripts
```shell script
    yb_carbon_calculation
  ```

### Run Local as script ###

```shell script
    python carbon_analitic.py 
  ```


### Run package in docker ###

Create a docker container on local machine.

 ```shell script
    docker build -t yb_carbon_calculation .
 ```

where yb_carbon_calculation - name of docker image


Run command 

 ```shell script
    docker run yb_carbon_calculation yb_carbon_calculation

 ```

### Run test ###

Run command in project folder src/tests

 ```shell script
    pytest 

 ```
