from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

from .forms import RegisterForm


# Create your views here.


class RegisterView(View):
    form_class = RegisterForm
    template_name = "users/signup.html"

    def dispatch(self, request, *args, **kwargs):
        """
        The dispatch function is the first function that gets called when a request
        is made to this view. It's job is to decide what type of request it is, and then
        call the appropriate method for handling that request. For example, if you make an HTTP GET
        request to /accounts/register/, dispatch will call get() because it knows that an HTTP GET
        request should be handled by a get() method.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A redirect to the news:root page if a user is authenticated
        :doc-author: Trelent
        """
        if request.user.is_authenticated:
            return redirect(to="news:root")
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        The get function renders the form to the user.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :return: The form
        :doc-author: Trelent
        """
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        """
        The post function is used to create a new user.
            It takes the request as an argument and returns a redirect to the login page if successful, or renders the signup template with form errors otherwise.

        :param self: Represent the instance of the class
        :param request: Pass the request object to the view
        :return: A render function, which is a response object
        :doc-author: Trelent
        """
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(
                request,
                f"Congratulations {username}. Your account is successfully created",
            )
            return redirect(to="users:login")

        return render(request, self.template_name, {"form": form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    success_message = (
        "An email with instructions to reset your password has been sent to %(email)s."
    )
    subject_template_name = "users/password_reset_subject.txt"
