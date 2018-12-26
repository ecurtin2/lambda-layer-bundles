LAYER_NAME=numpy-docker-py37
ZIP_FILE=$LAYER_NAME.zip
S3_BUCKET=broadspire-lambda-layers
PY_DIR='build/python/lib/python3.7/site-packages'

echo 'Installing into local directory...'
mkdir -p $PY_DIR
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
python -m compileall . -b -q

find . -name "*.py" -type f -delete

zip -r ../$ZIP_FILE .
cd ..

aws s3 cp $ZIP_FILE s3://$S3_BUCKET
aws lambda publish-layer-version --layer-name $LAYER_NAME --compatible-runtimes python3.7 --zip-file fileb://$ZIP_FILE --description "$DESCRIPTION"
