import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="url_shortener",
    version="0.0.1",

    description="URL Shortener",
    long_description=long_description,
    long_description_content_type="text/markdown",

    install_requires=[
        "aws-cdk.core",
        "aws-cdk.aws-dynamodb",
        "aws-cdk.aws-lambda",
        "aws-cdk.aws-certificatemanager",
        "aws-cdk.aws-apigateway",
        "aws-cdk.aws-route53-targets",
        "boto3"
    ],

    python_requires=">=3.6"
)
