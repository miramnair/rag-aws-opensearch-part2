import json
import boto3
import logging
import cfnresponse
import os


# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def send_response_cfn(event, context, responseStatus):
    responseData = {}
    responseData['Data'] = {}
    cfnresponse.send(event, context, responseStatus, responseData, "CustomResourcePhysicalID")

# Lambda function to delete all objects in an S3 bucket
def delete_s3_lambda_handler(event, context):
    logger.info("event: {}".format(event))
    try:
        bucket = event['ResourceProperties']['BucketName']
        logger.info("bucket: {}, event['RequestType']: {}".format(bucket, event['RequestType']))
        if event['RequestType'] == 'Delete':
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(bucket)
            for obj in bucket.objects.filter():
                logger.info("delete obj: {}".format(obj))
                s3.Object(bucket.name, obj.key).delete()

        send_response_cfn(event, context, cfnresponse.SUCCESS)
    except Exception as e:
        logger.info("Exception: {}".format(e))
        send_response_cfn(event, context, cfnresponse.FAILED)





