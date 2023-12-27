module "lambda_python" {
  source            = "../modules/terraform-aws-lambda-python/"

  aws_profile       = "default"
  aws_region        = "us-west-2"

  pip_path          = ".venv/bin/pip"

  lambda_name       = "dcm_to_png"
  lambda_api_name   = "dcm_to_png_api"
  lambda_iam_name   = "dcm_to_png_iam"

  api_stage_name    = "dev"
  api_resource_path = "demo"
  api_http_method   = "POST"
}
