import boto3 from botocore.client
import Configimport StringIOimport zipfileimport mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:176749210898:deploy-markmolesworth-topic')

    try:
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        website_bucket = s3.Bucket('www.markmolesworth.com')
        build_bucket = s3.Bucket('build.markmolesworth.com')
        website_zip = StringIO.StringIO()
        build_bucket.download_fileobj('markmolesworth.zip', website_zip)
    
        with zipfile.ZipFile(website_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                website_bucket.upload_fileobj(obj, nm,
                    ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                website_bucket.Object(nm).Acl().put(ACL='public-read')
            topic.publish(Subject="markmolesworth deployment successfull", Message="markmolesworth deployment successfull")
        
    print("markmolesworth deployment successfull.")
    return 'markmolesworth.com deployed successfully.'

except:
    topic.publish(Subject="markmolesworth deployment failed.", Message="markmolesworth deployment failed.")
    raise
