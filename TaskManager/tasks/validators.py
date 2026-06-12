from rest_framework import serializers

class TaskValidator(serializers.Serializer):

    title = serializers.CharField(required=True, allow_blank=False,error_messages={
            'required': 'Task title is required.',
            'blank': 'Task title cannot be blank.'
        }
    )
    description = serializers.CharField(required=False,allow_blank=True, allow_null=True)
    status = serializers.BooleanField( required=False,default=False)