module "lambda_python" {
  source            = "../terraform-aws-lambda-python/"

  aws_profile       = "default"
  aws_region        = "us-west-2"

  pip_path          = "pip"

  lambda_name       = "mip-dcm-to-png"
  lambda_iam_name   = "mip-dcm-to-png-iam"

#  lambda_api_name   = "mip-dcm-to-png-api"
#  api_stage_name    = "dev"
#  api_resource_path = "demo"
#  api_http_method   = "POST"
}
