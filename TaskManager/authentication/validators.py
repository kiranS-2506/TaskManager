from rest_framework import serializers


class UserRegisterValidators(serializers.Serializer):

    username = serializers.CharField(
        required=True, allow_null=False, allow_blank=False,error_messages={
            'required':'Username is a required field.',
            'null':'Username cannot be null.',
            'blank':'Username cannot be blank.',
        })
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False,
        error_messages={
            'required': 'Email is a required field.',
            'null':'Email cannot be null.',
            'blank':'Email cannot be blank.',})
    
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False,min_length=6,
        error_messages={
            'required':'Password is a required field.',
            'null':'Password cannot be null.',
            'blank':'Password cannot be blank.',
            'min_length':'Password must be at least 6 characters.',
        }
    )


class LoginValidator(serializers.Serializer):
    username = serializers.CharField(
        required=True, allow_null=False, allow_blank=False,
        error_messages={
            'required':'Username is a required field.',
            'null':'Username cannot be null.',
            'blank':'Username cannot be blank.',
        }
    )
    password = serializers.CharField(
        required=True, allow_null=False, allow_blank=False,
        error_messages={
            'required':'Password is a required field.',
            'null':'Password cannot be null.',
            'blank':'Password cannot be blank.',
        }
    )