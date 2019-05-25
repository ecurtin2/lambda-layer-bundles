from base64 import b64encode
import compileall
from pathlib import Path
from pprint import pprint
from shutil import make_archive, rmtree
from subprocess import run
from typing import List
from zipfile import ZipFile

import boto3
import click


def pip_install(requirements: str, build_dir: str):
    """Use pip to install requirements.txt to build dir
    
    Parameters
    -----------
    requirements
        Path to a pip requirements.txt file
    build_dir
        Path in which the requirements are to be installed.
    
    """
    print(f"Installing dependencies to {build_dir}")
    run(["pip", "install", "-r", requirements, "-t", build_dir])


def size_recursive_mb(path: Path) -> float:
    size_bytes = sum(p.stat().st_size for p in path.rglob("*"))
    return size_bytes / 10 ** 6


def shrink(directory: str):
    """Shrink a python package directory"""
    # Remove .pyc if they exist

    path = Path(directory)
    print(f"Shrinking deployment package: {path}")
    print(f"Original size of package: {size_recursive_mb(path):.3f} MB")

    for f in path.glob("**/*.pyc"):
        f.unlink()

    # Removing tests/
    for d in ["tests", "test", "doc", "docs"]:
        try:
            rmtree(d)
        except FileNotFoundError:
            pass

    # Remove debug symbols from shared libs
    for f in path.glob("**/*.so"):
        run(["strip", str(f)])

    # Compile python files to .pyc
    compileall.compile_dir(path, legacy=True, quiet=2)

    # Remove .py
    for f in path.glob("**/*.py"):
        f.unlink()

    print(f"Shrunken size of package: {size_recursive_mb(path):.3f} MB")


def upload_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    Parameters
    -----------
    file_name 
        File to upload
    bucket 
        Bucket to upload to
    object_name
        S3 object name. If not specified then file_name is used
    
    Returns
    --------
    True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client("s3")

    # If fails, it will throw clientException
    s3_client.upload_file(file_name, bucket, object_name)


def publish_layer(
    zipfile: bytes, name: str, description: str, compatible_runtimes: List[str]
):
    print("Uploading layer to AWS lambda")
    print(f"Name: {name}")
    print(f"Description: {description}")
    print(f"Compatible Runtimes: {compatible_runtimes}")

    lamduh = boto3.client("lambda")
    response = lamduh.publish_layer_version(
        LayerName=name, Description=description, Content={"ZipFile": zipfile}
    )

    keys = [
        "LayerArn",
        "LayerVersionArn",
        "Description",
        "CreatedDate",
        "Version",
        "CompatibleRuntimes",
    ]
    info = {k: v for k, v in response.items() if k in keys}
    info["CodeSize"] = response["Content"]["CodeSize"]

    print("Lambda Layer successfully published:")
    pprint(info)


@click.command()
@click.option("--name", required=True, help="Name of the resulting layer.")
@click.option("--desc", required=True, help="Description for lambda layer")
@click.option(
    "--requirements",
    required=False,
    default="requirements.txt",
    help="Path to requirements.txt file.",
)
@click.option(
    "--py_version", required=False, default="3.7", help="Python version to use"
)
@click.option("--s3_bucket", required=False, help="S3 bucket path for package storage.")
def main(name, requirements, s3_bucket, desc, py_version):
    build_dir = Path("tmp/build")

    try:
        pip_install(requirements, build_dir)
        shrink(build_dir)
        print("Zipping...")
        make_archive(name, "zip", build_dir)
        with open(name + ".zip", "rb") as f:
            archive = f.read()

        publish_layer(archive, name, desc, compatible_runtimes=[f"python{py_version}"])
    except:
        print("Uh oh, something went wrong!")
    finally:
        print(f"Cleaning build directory {build_dir}...")
        rmtree(build_dir)
        print(f"Build directory {build_dir} cleaned")


if __name__ == "__main__":
    main()
