"""

To get started on our API, we declare Serializers which translate data from the Todo Model instances into JSON objects that is easy to consume over the Internet. 
The JSON objects are outputted at API endpoint urls. Django REST framework shops with a powerful built-in serializer class that we can quickly extend with some code.

"""

#Actually in here we transform the Todo model to JSON 

from dataclasses import field
from rest_framework import serializers  
from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer): #We extend DRF’s ModelSerializer into a TodoSerializer class. ModelSerializer provides an API to create serializers from your models.
    
    created = serializers.ReadOnlyField() 
    completed = serializers.ReadOnlyField()
    """
    Often, an underlying database model will have more fields than what needs to be exposed. 
    DRF’s serializer class’s ability to include/exclude fields in our API is a great feature and makes it straightforward to control this.
    Additionally, we specify that created and completed fields are read only. I.e., they cannot be edited by a user
    """

    class Meta: #Under class Meta, we specify our database model Todo and the fields we want to expose i.e
        model = Todo
        fields = ['id','title','memo','created','completed']

"""
Django REST Framework then magically transforms our model data into JSON, exposing these fields from our Todo model.


Fields not specified here will not be exposed in the API. Remember that ‘id’ is created automatically by Django so we didn’t have to define it in Todo model.
But we will use it in our API.
"""


class TodoToggleCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = ['title','memo','created','completed']