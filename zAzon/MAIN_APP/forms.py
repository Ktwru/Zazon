from django import forms


class RegStep1(forms.Form):
    username = forms.CharField(label="Username")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput, min_length=8)
    email = forms.EmailField(label="Email")


class RegStep2(forms.Form):
    name = forms.CharField(label="Name", required=False, max_length=100)
    info = forms.CharField(label="Other info", widget=forms.Textarea, required=False)
    status = forms.CharField(label="Status", widget=forms.Textarea, required=False, max_length=250)


#class NewThread(forms.Form):
 #   thread = models.CharField(max_length=100)
  #  board = models.CharField(max_length=100)
   # login = models.ForeignKey(User, on_delete=models.PROTECT)
    #op_post = models.TextField()
    #thread_date = models.DateTimeField(auto_now=True)