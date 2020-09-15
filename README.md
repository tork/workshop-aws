# workshop-aws

## setup
### install docker
help yourself

### install pipenv
https://pipenv.pypa.io/en/latest/#install-pipenv-today

### install serverless
https://www.serverless.com/framework/docs/getting-started/

### install serverless-python-requirements
```
sls plugin install -n serverless-python-requirements
```

## deploy
```
sls deploy
```

...however!

when deploying, first set up your credentials. for instance [using env vars](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)
```
AWS_ACCESS_KEY_ID=<your_acces_key_id> AWS_SECRET_ACCESS_KEY=<your_secret_access_key> sls deploy
```
or
```
export AWS_ACCESS_KEY_ID=<your_acces_key_id>
export AWS_SECRET_ACCESS_KEY=<your_secret_access_key>
sls deploy
```

you can create credentials in the aws console, if you haven't already


## task 1
perform a deploy, familiarize yourself with the lambda in aws console.
try calling the lambda using aws console (hint: create a test event)
it should fail.

## task 2
output to s3 by creating a bucket called `workshop-aws-output` _or something similar_.
update handler.py#24 (`_s3_upload(image_out, 'workshop-aws-output', key)`) so it matches the bucket name you chose.
deploy and verify that test calls produces objects in the bucket.

## task 3
lambdas can be triggered by events in a bucket.
in `serverless.yml`, uncomment the s3-config: `functions.workshop-aws.events.s3`.
deploy and verify that serverless has created a bucket by name `aws-workshop-input`.
put a png-file into the input-bucket, verify that the result is written to output bucket.

## task 4
lambdas can be triggered by http events.
in `serverless.yml`, uncomment the s3-config: `functions.workshop-aws.events.http`.
nb: this will expose a get-endpoint publicly.
figure out how you can adjust the lambda to support http events.
hint: you'll want to use url-encoding
