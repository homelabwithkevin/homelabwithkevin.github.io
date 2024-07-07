from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3deploy,
    CfnOutput,
    aws_certificatemanager
)
import aws_cdk as cdk

from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "homelabwithkevin.com")
        distribution = cloudfront.Distribution(self, "hlb-prod",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            default_root_object="index.html",
            geo_restriction=cloudfront.GeoRestriction.allowlist("US"),
            domain_names=["homelabwithkevin.com"],
            certificate=aws_certificatemanager.Certificate.from_certificate_arn(self, "hlb", "arn:aws:acm:us-east-1:654654599343:certificate/65ddc75e-6863-4f23-9c45-ed885672e654")
        )

        s3deploy.BucketDeployment(self, "DeployWithInvalidation",
            sources=[s3deploy.Source.asset("../public")],
            destination_bucket=bucket,
            distribution=distribution
        )

        CfnOutput(self, "DistributionUrl", value=distribution.distribution_domain_name)