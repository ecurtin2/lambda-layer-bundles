# lambda-layer-bundles
Premade packages to run on aws lambda layers

## How to use

Simply upload the zip to an S3 bucket, and create the AWS lambda layer by pointing it to the zip file. 


## Python

Note: Didn't bother with numpy and scipy since AWS released their own. 

Y = Yes it is here
N = Tried but failed to create
empty = Did not try to make

Library   | 2.7 | 3.6 | 3.7 |
--------- | --- | --- | --- |
Altair    |     |     |  Y  |
Pandas    |     |     |  Y  |


## Creating new layers

Right now layers are built using the layer_package.sh on an amazon EC2 instance. 


## Contributing

Further improvements always welcome! If you decide to add more functionality consider submitting a PR :)
