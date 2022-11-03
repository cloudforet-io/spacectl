import io
import boto3
import pandas as pd

from spaceone.core import utils
from spacectl.lib.apply.task import BaseTask
from spacectl.lib.apply.task import execute_wrapper


class Task(BaseTask):

    def __init__(self, task_info, *args, **kwargs):
        super().__init__(task_info, *args, **kwargs)
        self.s3 = None
        self._validate()
        self._create_session()

    @execute_wrapper
    def execute(self):
        output = self.spec.get('output', 'csv')

        with io.StringIO() as io_buffer:
            if output == 'csv':
                df = pd.DataFrame(self.spec['data'])
                df.to_csv(io_buffer, index=False)
            else:
                io_buffer.write(utils.dump_json({'data': self.spec['data']}, 4))

            response = self.s3.put_object(
                Bucket=self.spec['bucket'], Key=self.spec['path'], Body=io_buffer.getvalue()
            )

            status = response.get('ResponseMetadata', {}).get('HTTPStatusCode')

            if status != 200:
                raise Exception(f'The put_object command in S3 failed. (status = {status})')

    def _create_session(self):
        if 'role_arn' in self.spec:
            session = boto3.Session(aws_access_key_id=self.spec['aws_access_key_id'],
                                    aws_secret_access_key=self.spec['aws_secret_access_key'])

            sts = session.client('sts')
            sts.get_caller_identity()

            assume_role_request = {
                'RoleArn': self.spec['role_arn'],
                'RoleSessionName': utils.generate_id('AssumeRoleSession')
            }

            if 'external_id' in self.spec:
                assume_role_request['ExternalId'] = self.spec['external_id']

            assume_role_object = sts.assume_role(**assume_role_request)
            credentials = assume_role_object['Credentials']
            self.s3 = boto3.client('s3', aws_access_key_id=credentials['AccessKeyId'],
                                   aws_secret_access_key=credentials['SecretAccessKey'],
                                   aws_session_token=credentials['SessionToken'])

        else:
            self.s3 = boto3.client('s3', aws_access_key_id=self.spec['aws_access_key_id'],
                                   aws_secret_access_key=self.spec['aws_secret_access_key'])

    def _validate(self):
        if 'aws_access_key_id' not in self.spec:
            raise ValueError(f'Required key: aws_access_key_id\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'aws_secret_access_key' not in self.spec:
            raise ValueError(f'Required key: aws_secret_access_key\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'bucket' not in self.spec:
            raise ValueError(f'Required key: bucket\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')
