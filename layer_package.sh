#
# layer-package.sh
#
# This requires pipenv installed and a version
# of the python compatible with the layer runtime.
#
# Make sure to run this on an environment compatible
# with aws lambda, I currently run it on an amazonlinux 
# EC2 AMI.
#
# TODO: parameterize the installed dependencies and maybe 
#       the layer name.
#

LAYER_NAME=datascience-python37
ZIP_FILE=$LAYER_NAME.zip
S3_BUCKET=broadspire-lambda-layers

# Change if you know what you're doing.
# Might want to just change python version and keep
# the rest the same.
PY_DIR='build/python/lib/python3.7/site-packages'

echo 'Creating pipenv virtual environment...'
pipenv --python 3.7
pipenv shell

###############################################################
#
# Change install command to be whatever
#
################################################################

echo 'Installing dependencies into pipenv...'
pipenv install sklearn pandas xgboost altair

#################################################################

echo 'Installing into local directory...'
mkdir -p $PY_DIR
pipenv lock -r > requirements.txt
pip install -r requirements.txt --no-deps -t $PY_DIR

cd build

echo 'Remove .pyc if they exist'
find . -name "*.pyc" -type f -delete

echo 'Removing tests/'
find -type d -name tests -exec rm -rf {} \;
find -type d -name test -exec rm -rf {} \;

echo 'Removing doc/'
find -type d -name doc -exec rm -rf {} \;
find -type d -name docs -exec rm -rf {} \;

echo 'Compile python files to .pyc'
python3 -m compileall . -b -q

echo 'Removing .py  files'
find . -name "*.py" -type f -delete

echo 'zipping up requirements...'
zip -r ../$ZIP_FILE .
cd ..

echo 'Uploading to s3...'
aws s3 cp $ZIP_FILE s3://$S3_BUCKET

echo 'Creating lambda layer from zip...'
DESCRIPTION=`cat requirements.txt`

aws lambda publish-layer-version --layer-name $LAYER_NAME	--compatible-runtimes python3.7 --zip-file fileb://$ZIP_FILE --description "$DESCRIPTION"
