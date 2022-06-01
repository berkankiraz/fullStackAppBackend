from lib2to3.pgen2 import token
from django.shortcuts import render
from rest_framework import generics  , permissions #We import DRF ’ s generics class of views.
from .serializers import TodoSerializer, TodoToggleCompleteSerializer 
from todo.models import Todo


from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser 
from rest_framework.authtoken.models import Token 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

 #Because the POST request is coming from a different domain (the frontend domain) and will not have the token required to pass the CSRF checks (cross site request forgery), we use csrf_exempt for this view.


from django.contrib.auth import authenticate


# Create your views here.


class TodoListCreate(generics.ListCreateAPIView):
    #We then create TodoList that uses generics.ListAPIView. ListAPIView is a built-in generic class which creates a read-only endpoint for model instances.
    #ListAPIView requires two mandatory attributes, serializer_class and queryset. 
    #we specify TodoSerializer which we have earlier emplemented

    serializer_class= TodoSerializer
    #When we specify TodoSerializer as the serializer class, we create a read-only endpoint for todo instances. 

    permission_classes=[permissions.IsAuthenticated]
    #with this, we specify that only authenticated and registered users have permission to call this API. Unauthenticated users are not allowed to acces it. 

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')
        
    """   
    get_queryset returns the queryset of todo objects for the view. In our case, we specify the query set as all todos which match the user.
    Additionally, we order the todos by the created date i.e. we show the latest todo first.
    """

    def perform_create(self, serializer):
        #serializer holds a django model
        serializer.save(user=self.request.user)

    """
    perform_create acts as a hook which is called before the instance is created in the database. 
    Thus, we can specify that we set the user of the todo as the request’s user before creation in the database.

    These hooks are particularly useful for setting attributes that are implicit in the request, but are not part of the request data.
    In our case, we set the todo’s user based on the request user.
    """

class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    """
    Django REST Framework provides the built-in RetrieveUpdateDestroyAPIView to automatically implement the get(), put() and delete() endpoint.

    """

    serializer_class=TodoSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user= self.request.user
        #user can only update, delete own post 

        return Todo.objects.filter(user=user)


class TodoToggleComplete(generics.UpdateAPIView): 
    """
    As its name suggests, TodoToggleComplete toggles a todo from incomplete to complete and vice-versa.
    TodoToggleComplete extends the UpdateAPIView used for update-only endpoints for a single model instance.
    """


    serializer_class=TodoToggleCompleteSerializer
    permission_classes=[permissions.IsAuthenticated] #Only authenticated users can mark a todo as complete.

    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        """
        perform_update is called before the update happens. 
        In it, we ‘invert’ the todo’s completed boolean value. i.e. if its true, set to false, if false, set to true.
        """
        serializer.instance.completed=not(serializer.instance.completed) 
        serializer.save()


@csrf_exempt 
def signup(request):
    if request.method == 'POST': #We first check if a request was performed using the HTTP ‘POST’ method. This is because the sign up form in the front end will use POST request for form submissions.
        try:
            data=JSONParser().parse(request)  # data is a dictionary
            user= User.objects.create_user(
                username= data['username'],
                password= data['password']
            )
            user.save()

            """          
            We then call JSONParse().parse to parse the JSON request content and return a dictionary of data.
            We extract the user filled-in values from the dictionary with data[‘username’] and data[‘password’] and create a
            user with User.objects.create_user. User.objects.create_user creates and returns a user. With user.save(), we save the User object to the database.
            """

            token= Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=201)

            """
            After saving the user to the database, we create the token object with Token.objects.create(user=user).
            If all goes well, we return a JsonResponse object with a dictionary containing the token, and status code of 201
            indicating successful creation.
            """
        
        except IntegrityError:
            return JsonResponse({'error':'username taken. choose another username'},status=400)

            """
            If there is an error, we return a JsonResponse object with a dictionary containing the error and status code of 400 indicating that the request cannot be fulfilled.
            """

"""
Note: when we send the JSON Response, we attach a status code to accompany it. The status code reflects the following:
- 2xx ‘success’ - the request was successfully received, understood and accepted
- 3xx ‘redirection’ – further action needs to be taken to complete the request
- 4xx ‘client error’ – the request contains bad syntax or cannot be fulfilled, typically a bad URL request by
the client
- 5xx ‘server error’ – the server failed to fulfill a valid request
You don’t need to memorize all the status codes. The most common ones are 200 ‘Ok’, 201 ‘created’, 404 ‘not found’, and 500 ‘server error’.

"""

@csrf_exempt
def login(request):
    if request.method== 'POST':
        """
        We check if a request was performed using the HTTP ‘POST’ method because the login form in the front end will use POST requests for form submissions.
        """

        data=JSONParser().parse(request)
        user= authenticate(
            request,
            username= data['username'],
            password = data['password']
        )

        """
        We then call JSONParse().parse to parse the JSON request content and return a dictionary of data.
        We extract the user filled-in values from the dictionary with data[‘username’] and data[‘password’] and pass them into the authenticate method.
        """

        if user is None:
            return JsonResponse({'error':'unable to login. check username and password'}, status=400)
            """
            If no user is found, we return a JsonResponse object with a dictionary containing an error message and status code of 400 indicating that the request cannot be fulfilled.
            """

        else: #return user token
            try:
                token=Token.objects.get(user=user)
            except: #if token not in db create new one
            
                token = Token.objects.create(user=user)
                
            return JsonResponse({'token':str(token)}, status=201)

            """
            Else, it means that the authentication is successful and we found a user. We then retrieve an existing user token with Token.objects.get(user=user) or create a new one if the token is not in the database.
            """
        
        