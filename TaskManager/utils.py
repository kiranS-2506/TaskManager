from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


#this function for standard success response message
def success_response(message, data=None):
    return {
        'success': True,
        'message': message,
        'data':    data,
    }

#this function for standard Error response message
def error_response(message, errors=None):
    return {
        'success': False,
        'message': message,
        'errors':  errors,
    }



#this function for gereate the JWT tokens
def get_tokens_for_user(User: User):
 
    token = RefreshToken.for_user(User)
    token["full_name"] = User.username
    token["email"] = User.email
    return {
        'refresh': str(token),
        'access': str(token.access_token),
        'expiry_time': (token.access_token['exp'] * 1000)
    }


#this class for Pgination
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'next_page': self.get_next_link(),
            'prev_page': self.get_previous_link(),
            'count': self.page.paginator.count,
            'rows_per_page':self.get_page_size(self.request),
            'results': data
        })
    
#For Data filed Errors
class SerializerError(Exception):
    def __init__(self, data):
        error_messages = []
        for field, error in data.items():
            error_message = str(error[0])
            error_messages.append(error_message)
        self.data = error_messages[0]
    def __str__(self):
        return self.data
