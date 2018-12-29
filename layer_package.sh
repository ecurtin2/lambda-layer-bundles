set -e

# Needs environment 
# $LAYER_NAME
# $REQUIREMENTS
# $S3_BUCKET
# PY_DIR

ZIP_FILE=$LAYER_NAME.zip
echo "$REQUIREMENTS" > requirements.txt


echo 'Installing into local directory...'
mkdir -p $PY_DIR
pip install -r requirements.txt --no-deps -t $PY_DIR

echo 'The sizes of the unprocessed deployment package:'
du -h -d 2 $PY_DIR | sort -h

cd build
set +e

# Remove .pyc if they exist
find . -name "*.pyc" -type f -delete

# Removing tests/
find -type d -name tests -exec rm -rf {} \;
find -type d -name test -exec rm -rf {} \;

# Removing doc/
find -type d -name doc -exec rm -rf {} \;
find -type d -name docs -exec rm -rf {} \;


# Remove debug symbols from shared libs
find . -type f -name "*.so" | xargs strip

set -e

echo 'Compile python files to .pyc'
python -m compileall . -b -q

echo 'Removing .py files'
find . -name "*.py" -type f -delete


echo 'Zipping...'
zip -r  -q ../$ZIP_FILE .
cd ..

echo 'The sizes of the unzipped deployment package after processing:'
du -h -d 2 $PY_DIR | sort -h

echo 'The sizes of the zipped deployment package:'
du -h $ZIP_FILE

DESCRIPTION=`cat requirements.txt`

S3_PATH=s3://$S3_BUCKET/$LAYER_NAME 
echo Uploading to $S3_PATH ...
#aws s3 cp $ZIP_FILE $S3_PATH/bundle.zip
#aws s3 cp requirements.txt $S3_PATH/requirements.txt

echo Bundle uploaded to https://$S3_PATH/bundle.zip
echo The contents of requirements.txt are:
cat requirements.txt

