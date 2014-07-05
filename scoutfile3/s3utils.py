__author__ = 'andrei'


from storages.backends.s3boto import S3BotoStorage
MediaS3BotoStorage = lambda: S3BotoStorage(location='media')

ProtectedS3BotoStorage = lambda: S3BotoStorage(
  acl='private',
  querystring_auth=True,
  querystring_expire=120, # 10 minutes, try to ensure people won't/can't share
)