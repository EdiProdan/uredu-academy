aws cloudformation deploy \
  --template-file "cicd/codepipeline.yml" \
  --stack-name "uredu-academy-final-codepipeline" \
  --capabilities CAPABILITY_NAMED_IAM

aws cloudformation deploy \
  --template-file "cicd/glue.yml" \
  --stack-name "uredu-academy-final-glue" \
  --capabilities CAPABILITY_NAMED_IAM

aws cloudformation deploy \
  --template-file "cicd/s3.yml" \
  --stack-name "uredu-academy-final-s3" \
  --capabilities CAPABILITY_NAMED_IAM

aws cloudformation deploy \
  --template-file "cicd/lambda.yml" \
  --stack-name "uredu-academy-final-lambda" \
  --parameter-overrides \
      S3BucketScriptsName="uredu-academy-final-scripts" \
      LambdaName="uredu-academy-final-lambda" \
      LambdaRoleName="uredu-academy-final-lambda-role" \
      LambdaUploadUNIXT=$LambdaUploadUNIXT \
  --capabilities CAPABILITY_NAMED_IAM

aws cloudformation deploy \
  --template-file "cicd/secretsmanager.yml" \
  --stack-name "uredu-academy-final-secretsmanager" \
  --parameter-overrides \
      SecretsManagerName="uredu-academy-final-key" \
  --capabilities CAPABILITY_NAMED_IAM