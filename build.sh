set -e

REQUIREMENTS=`cat requirements.txt`

docker run\
 -e LAYER_NAME=tensorflow-py36\
 -e REQUIREMENTS="$REQUIREMENTS"\
 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\
 -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
 -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION\
 -e S3_BUCKET=lambda-layer-bundles\
 layers-py36

