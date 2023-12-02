import boto3
from vaultUtil import VaultClient

VAULT_URL = "http://127.0.0.1:8200"
ROLE_ID = "40eab551-1752-d210-876c-200497d3abbb"
SECRET_ID = "d5d175e6-d60b-a887-3cc1-f13358deb2de"
SECRET_PATH = "secret/data/aws"

vault_client = VaultClient(VAULT_URL, ROLE_ID, SECRET_ID, SECRET_PATH)
token = vault_client.authenticate_with_approle()

if token:
    secret_data = vault_client.get_secret(token)
    if secret_data:
        print("Secret data:", secret_data)
    else:
        print("Failed to retrieve secret.")
else:
    print("Failed to authenticate with AppRole.")


aws_access_key = secret_data['data']['bw-aws-accesskey-dev']
aws_secret_key = secret_data['data']['bw-aws-secretkey-dev']

region = 'us-east-1'  # Replace with your preferred AWS region

class AWSConnector:
    def __init__(self, aws_access_key, aws_secret_key, client='s3', region='us-east-1'):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.region = region
        self.aws_client = client
        self.session = self.create_session()
        self.aws_client_conn = self.create_aws_client()
        

    def create_session(self):
        """
        Create an AWS session using the provided credentials and region.
        """
        session = boto3.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region
        )
        return session

    def create_aws_client(self):
        """
        Create an AWS client using the AWS session.
        """
        aws_client_conn = self.session.client(self.aws_client)
        return aws_client_conn

# Create an instance of the AWSConnector class
# client='s3'
# aws_connector = AWSConnector(aws_access_key, aws_secret_key, client, region)

# # Access the S3 client through the instance
# s3_client = aws_connector.aws_client_conn

# # Now you can use s3_client to perform S3 operations
# response = s3_client.list_buckets()
# print("S3 Buckets:")
# for bucket in response['Buckets']:
#     print(f"  {bucket['Name']}")