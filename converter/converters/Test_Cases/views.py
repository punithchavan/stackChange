from django.views.generic import ListView, DetailView
# Assume models.py has 'Post' and 'User' models
from .models import Post, User 

# This is a sample views.py file for the AST parser to analyze.

class PostListView(ListView):
    # The parser will find this line
    model = Post

class PostDetailView(DetailView):
    # And this line
    model = Post
    # It will ignore other attributes
    template_name = 'post_detail.html'

class UserListView(ListView):
    # This view is linked to the User model
    model = User

def api_statistics(request):
    # A plain function view has no 'model' attribute, so it will get a generic controller.
    # ... logic ...
    pass