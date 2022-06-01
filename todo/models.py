from django.db import models

# Create your models here.

"""
Working with databases in Django involves working with models.
 We create a database model (e.g. todo, book, blog post, movie) and Django turns these models into a database table for us.
"""

from django.db import models 
"""
Django imports a module models to help us build database models which ‘ model ’ the characteristics of the data in the database.
 In our case, we created a todo model to store the title, memo, time of creation, time of completion and user who created the todo.
"""
from django.contrib.auth.models import User
class Todo(models.Model):
    """
    class Todo inherits from the Model class. 
    The Model class allows us to interact with the database, create a table, retrieve and make changes to data in the database.
    """
    title = models.CharField(max_length=100) 
    memo = models.TextField(blank=True)

    """
    We then have the properties of the model. 
    Notice that the properties have types like CharField, TextField, DateTimeField. Django provides many other model fields to support common types like dates, integers, emails, etc.
    """

    #set to current time
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    #user who posted this
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self): return self.title #We also include a __str__ method so that the title of a todo will display in the admin later on.

"""
Whenever we create a new model or make changes to it in models.py, we need to update Django in a two-step
process. First, in /todoapp/todobackend/, we create a migration file with the makemigrations command:

python3 manage.py makemigrations

This generates the SQL commands (migrations) for preinstalled apps in our INSTALLED_APPS setting. 

The SQL commands are not yet executed but are just a record of all changes to our models. 
The migrations are stored in an auto-generated folder migrations 

Second, we build the actual database with the following:
python3 manage.py migrate


The migrate command creates an initial database based on Django ’ s default settings and executes the SQL commands in the migrations file. 
Notice there is a db.sqlite3 file in the project folder. The file represents our SQLite database. 
It is created the first time we run migrate. migrate syncs the database with the current state of any database models in the project and listed in INSTALLED_APPS. 
It is thus essential that after we update a model, we need to run migrate.


In summary, each time you make changes to a model file, you have to run:
 python3 manage.py makemigrations 
 python3 manage.py migrate
"""
