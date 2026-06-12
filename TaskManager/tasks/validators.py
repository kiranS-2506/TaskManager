from rest_framework import serializers
from django.utils import timezone

class TaskValidator(serializers.Serializer):

    title = serializers.CharField(required=True, allow_blank=False,error_messages={
            'required': 'Task title is required.',
            'blank': 'Task title cannot be blank.'
        }
    )
    description = serializers.CharField(required=False,allow_blank=True, allow_null=True)
    status = serializers.BooleanField( required=False,default=False)


    due_date = serializers.DateTimeField(required=False, allow_null=True,input_formats=['%Y-%m-%d', 'iso-8601'],
        error_messages={
            'invalid': 'Invalid date format. Use this format(YYYY-MM-DD).'
        }
    )

    def validate_due_date(self, value):

        if value and value < timezone.now():
            raise serializers.ValidationError("The due date cannot be set in the past.")
        return value