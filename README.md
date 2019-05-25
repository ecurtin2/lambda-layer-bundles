# lambda-layer-bundles
Premade packages to run on aws lambda layers

## Demo

![Alt Text](https://github.com/ecurtin2/lambda-layer-bundles/blob/master/demo.gif)

## CLI

The docker-compose includes a service that simply runs the CLI.
The requirements are installed by pip, so whatever pip recognizes
will be accepted by the script. To create a layer with numpy+pandas
you would simply run

```
docker-compose run make numpy pandas --name NumPandas --desc "numpy and pandas"
```

To get help, 
```
docker-compose run make --help
```
Which will print (might change if I forget to update readme)
```
Usage: make_layer.py [OPTIONS] [REQUIREMENTS]...

Options:
  --name TEXT  Name of the resulting layer.  [required]
  --desc TEXT  Description for lambda layer  [required]
  --help       Show this message and exit.
```

If no requirements are specified, the script will attempt
to pip install from the `./requirements.txt` file which
is mounted to `/code/requirements.txt` which in the default
docker compose is mounted from the current directory.
So if nothing is changed, this will install the 
requirements.txt from the current directory.