# lambda-layer-bundles
Premade packages to run on aws lambda layers

## How to use

Simply upload the zip to an S3 bucket, and create the AWS lambda layer by pointing it to the zip file. 


## Python

Note: Didn't bother with numpy and scipy since AWS released their own. 

Y = Yes it is here
N = Tried but failed to create
empty = Did not try to make

List of Packages I tried but couldn't get to fit into the unzipped deployment size:

  - Tensorflow (269MB)
  - PyTorch (259MB)


## Creating new layers

Build the docker image, optionally changing the python runtime in dockerfile.

`docker build -t <YOUR_TAG>`

edit the requirements.txt and build.sh with the parameters you want and your docker tag.
Then simply

`bash build.sh`

The files will be uploaded to an S3 bucket of your choice. To turn them into a layer, 
simply use the AWS console to create a layer from an existing location in s3. This way the
50MB compressed limit is sidestepped, and the only thing that matters is the unzipped
limit of 250MB. 

## Contributing

Further improvements always welcome! If you decide to add more functionality consider submitting a PR :)

## Roadmap

Not necesarily in a particular order:
  - Build on docker image instead of EC2
    - Companion Dev / Deploy Machine Learning Docker image / layer (build model locally on image, deploy to layer)
  - Add conda support instead of pipenv
  - runtimes other than python?
  - Publicly available premade layers in one central place
  - Ensure compatibility between as many layers as possible, so they may be combined. 
  - Lambda function to build lambda layers?

