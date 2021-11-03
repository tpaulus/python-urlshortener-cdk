# python-urlshortener-cdk
A Python Based URL Shorter deployed to AWS via CDK.

Based on the [url-shortner](https://github.com/aws-samples/aws-cdk-examples/tree/master/python/url-shortener) example from the 
[aws-cdk-samples](https://github.com/aws-samples/aws-cdk-examples) repo.

### Shortening Logic
There are 3 different URL shorteners defined in `lambda/shortner.py` which increase in complexity. All of these shorteners implement the
Abstract Class `AbstractShortner` which defines the base interface for a URL Shortner with functions to shorten a long URL into a slug and 
expand a slug into a long URL.  

The first shortener uses a UUID generator to generate a random string of letters and numbers, which is a fine solution. However, the second
shortener builds on this and uses an alphabet of non-ambiguous, lowercase characters to improve readability and increase input speed for
users. The third shortener uses a custom Amazon DynamoDB Dictionary to add stateful storage, which will be necessary when we deploy this code
to Lambda where we cannot rely on the memory of the function to be persisted.


## AWS Deployment
### Setup

Create and source a Python virtualenv on MacOS and Linux, and install python dependencies:

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Install the latest version of the AWS CDK CLI:

```shell
npm i -g aws-cdk
```

### Configuration
Configure the account id, Region, Hosted Zone Name, and Hosted Zone ID at the top of `app.py` to the values correct for your account.

### Deployment

If this is the first time you are running CDK in this account, you will need to bootstrap your account, which can be done via:
```shell
cdk bootstrap aws://ACCOUNT-ID/REGION
```

At this point, you should be able to deploy the stack in this app using:
```shell
cdk deploy
```

If you want to clean everything up after you are done:
```shell
cdk destroy
```