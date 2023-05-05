from rest_framework import serializers
import json


class BaseSerializer():
    def get_error_response(self):
        error_response = {
            'message': [],
            'data': {
                'errorFields': [],
                'completeError': {}
            },
            'statusCode': 400
        }
        if not self.is_valid():
            errors = json.loads(json.dumps(self.errors))
            error_response['data']['completeError'] = errors

            for error in errors:
                error_messages = errors[error]
                error_response['data']['errorFields'].append(error)
                for error_message in error_messages:
                    error_response['message'].append(
                        error_message if 'generic' == error else f"{error}: {error_message}"
                    )
        return error_response


class Serializer(BaseSerializer, serializers.Serializer):
    pass


class ModelSerializer(BaseSerializer, serializers.ModelSerializer):
    pass