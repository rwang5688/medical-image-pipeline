module "lambda_python" {
  source            = "../terraform-aws-lambda-python/"

  aws_profile       = "default"
  aws_region        = "us-west-2"

  pip_path          = "pip"

  lambda_name       = "mip-de-identify-png"
  lambda_iam_name   = "mip-de-identify-png-iam"

#  lambda_api_name   = "mip-de-identify-png-api"
#  api_stage_name    = "dev"
#  api_resource_path = "demo"
#  api_http_method   = "POST"
}
