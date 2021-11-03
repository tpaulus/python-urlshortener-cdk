from aws_cdk.core import App, Construct, Duration, Stack, Environment
from aws_cdk import aws_dynamodb, aws_lambda, aws_apigateway, aws_certificatemanager, aws_route53, aws_route53_targets

ACCOUNT = "111111111111"
REGION = "us-west-2"

ZONE_NAME = "yourdomain.com"
ZONE_ID = "Z11FE11Z11DV1"


# our main application stack
class UrlShortenerStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwarg) -> None:
        super().__init__(scope, id, env=Environment(account=ACCOUNT, region=REGION), **kwarg)

        # define the table that maps short codes to URLs.
        table = aws_dynamodb.Table(self, "Table",
                                   partition_key=aws_dynamodb.Attribute(
                                       name="id",
                                       type=aws_dynamodb.AttributeType.STRING),
                                   billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST)

        # define the API gateway request handler. all API requests will go to the same function.
        handler = aws_lambda.Function(self, "UrlShortenerFunction",
                                      code=aws_lambda.Code.asset("./lambda"),
                                      handler="handler.main",
                                      timeout=Duration.minutes(1),
                                      runtime=aws_lambda.Runtime.PYTHON_3_9)

        # pass the table name to the handler through an environment variable and grant
        # the handler read/write permissions on the table.
        handler.add_environment('TABLE_NAME', table.table_name)
        table.grant_read_write_data(handler)

        # define the API endpoint and associate the handler
        api = aws_apigateway.LambdaRestApi(self, "UrlShortenerApi",
                                           handler=handler)

        # map go.paulusto.people.aws.dev to this api gateway endpoint
        # the domain name is a shared resource that can be accessed through the API
        # NOTE: you can comment this out if you want to bypass the domain name mapping
        self.map_subdomain('go', api)

    def map_subdomain(self, subdomain: str, api: aws_apigateway.RestApi):
        """
        :param subdomain: The sub-domain (e.g. "www")
        :param api: The API gateway endpoint
        :return: The base url (e.g. "https://paulusto.people.aws.dev")
        """

        domain_name = subdomain + '.' + ZONE_NAME
        url = 'https://' + domain_name

        hosted_zone = aws_route53.HostedZone.from_hosted_zone_attributes(self, 'HostedZone',
                                                                         hosted_zone_id=ZONE_ID,
                                                                         zone_name=ZONE_NAME)

        cert = aws_certificatemanager.DnsValidatedCertificate(self, 'DomainCertificate',
                                                              hosted_zone=hosted_zone,
                                                              domain_name=domain_name)

        # add the domain name to the api and the A record to our hosted zone
        domain = api.add_domain_name('Domain', certificate=cert, domain_name=domain_name)

        aws_route53.ARecord(
            self, 'UrlShortenerDomain',
            record_name=subdomain,
            zone=hosted_zone,
            target=aws_route53.RecordTarget.from_alias(aws_route53_targets.ApiGatewayDomain(domain)))

        return url


app = App()
UrlShortenerStack(app, "urlshort-app")

app.synth()
