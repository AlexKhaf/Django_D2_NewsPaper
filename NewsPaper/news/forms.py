from django.forms import ModelForm
from .models import Post
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm

class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'topic','postAuthor', 'category', "contents"]

class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get_or_create(name='common')[0]
        basic_group.user_set.add(user)
        return user