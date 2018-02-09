import boto3 from botocore.client
import Configimport StringIOimport zipfileimport mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:176749210898:deploy-markmolesworth-topic')

    locatin = {
        "bucketName": 'build.markmolesworth.com',
        "objectKey": 'markmolesworth.zip'
    }
    
    try:
        job = event.get("CodePipeline.job")
        
        if job:
            for artifact in job["data"]["artifacts"]:
                if artifact["name"] = "MyAppBuild":
                location = artifact["location"]["s3Location"]
        
        print("Building markmolesworth from " + str(location))
        
        
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        website_bucket = s3.Bucket('www.markmolesworth.com')
        build_bucket = s3.Bucket(location["bucketName"])
        website_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location["objectKey"], website_zip)
    
        with zipfile.ZipFile(website_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                website_bucket.upload_fileobj(obj, nm,
                    ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                website_bucket.Object(nm).Acl().put(ACL='public-read')
            topic.publish(Subject="markmolesworth deployment successfull", Message="markmolesworth deployment successfull")
        
    print("markmolesworth deployment successfull.")
    if job:
        codepipeline = boto3.client("codepipeline")
        codepipeline.put_job_success_result(jobId=job["id"])
        
    return 'markmolesworth.com deployed successfully.' 

except:
    topic.publish(Subject="markmolesworth deployment failed.", Message="markmolesworth deployment failed.")
    raise


