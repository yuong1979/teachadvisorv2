import os
from boto.s3.connection import S3Connection

AWS_ACCESS_KEY_ID = 'AKIAJ2IFSHNL6I6YBS3A'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_NAME = 'testingbucketyu'

conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = conn.get_bucket(BUCKET_NAME)
key = bucket.get_key('secret.txt')
[secret_key, database_pw] = key.get_contents_as_string().splitlines()
os.environ['SECRET_KEY'] = secret_key
os.environ['DATABASE_PW'] = database_pw

print os.environ['SECRET_KEY']
print os.environ['DATABASE_PW']