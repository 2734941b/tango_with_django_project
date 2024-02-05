from django import forms
from rango.models import Page, Category
from django.contrib.auth.models import User
from rango.models import UserProfile

max_len_title=128
max_len_url=200

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=max_len_title,
                            help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=max_len_title,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=max_len_url,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        url = cleaned_data.get('url')
        category_titles = [cat.name for cat in Category.objects.order_by('-likes')]

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        if title == "":
            title = 'Untitled'
            cleaned_data['title'] = title
        
        if title in category_titles:
            end = title.split(" ")[-1]
            if end.isnumeric():
                title = " ".join(title.split(" ") + str(int(end) + 1))
            else:
                title = title + " 1"
            cleaned_data['title'] = title
            
        return cleaned_data
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)