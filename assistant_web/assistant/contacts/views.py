from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .forms import ContactForm
from .models import Contact


@login_required
def contact_list(request):
    """
    The contact_list function is responsible for rendering the contact_list.html template,
    which displays all of the contacts in a user's address book.

    :param request: Pass the request object to the view
    :return: A rendered template
    :doc-author: Trelent
    """
    contacts = Contact.objects.filter(user=request.user).order_by("name", "thurname")
    return render(request, "contacts/contact_list.html", {"contacts": contacts})


@login_required
def add_contact(request):
    """
    The add_contact function is a view that allows users to add contacts.
        It takes in the request and returns a rendered template with the form.
        If the form is valid, it saves it to the database and redirects to contact_list.

    :param request: Get the current request
    :return: The rendered template of the form if it is not valid
    :doc-author: Trelent
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect("contacts:contact_list")
    else:
        form = ContactForm()
    return render(request, "contacts/add_contact.html", {"form": form})


@login_required
def edit_contact(request, contact_id):
    """
    The edit_contact function is used to edit an existing contact.
        It takes a request and a contact_id as arguments, and returns the rendered template for editing contacts.


    :param request: Get the current request
    :param contact_id: Get the contact object from the database
    :return: A render function
    :doc-author: Trelent
    """
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect("contacts:contact_list")
    else:
        form = ContactForm(instance=contact)

    return render(
        request, "contacts/edit_contact.html", {"form": form, "contact": contact}
    )


@login_required
def delete_contact(request, contact_id):
    """
    The delete_contact function is used to delete a contact from the database.
        It takes in a request and contact_id as parameters, and returns either
        an HTML page or redirects to another page depending on the method of the request.


    :param request: Get the request object that is sent to the server
    :param contact_id: Get the contact object from the database
    :return: A render() function, which is the page that will be displayed to the user
    :doc-author: Trelent
    """
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    if request.method == "POST":
        contact.delete()
        return redirect("contacts:contact_list")
    return render(request, "contacts/delete_contact.html", {"contact": contact})


@login_required
def search_contacts(request):
    """
    The search_contacts function is a view that allows users to search for contacts by name, email or phone number.
    The function takes in the request object and returns a rendered template with the results of the query.

    :param request: Get the current request object
    :return: The rendered contact_list
    :doc-author: Trelent
    """
    query = request.GET.get("q")
    if query:
        contacts = Contact.objects.filter(
            Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query),
            user=request.user,
        ).order_by("name", "thurname")
    else:
        contacts = Contact.objects.filter(user=request.user).order_by(
            "name", "thurname"
        )
    return render(
        request, "contacts/contact_list.html", {"contacts": contacts, "query": query}
    )


@login_required
def upcoming_birthdays(request):
    """
    The upcoming_birthdays function takes a request and returns a list of contacts whose birthdays are within the next 7 days.
    The function first gets today's date, then it gets all the contacts that have birthdates and belong to the current user.
    It then loops through each contact, getting their birthday this year (or next year if their birthday has already passed).
    Then it calculates how many days until their birthday is from today's date. If there are less than or equal to 7 days left until
    their birthday, they get added to our result list.

    :param request: Pass the request object to the view
    :return: The contacts that have a birthday in the next 7 days
    :doc-author: Trelent
    """
    today = date.today()
    contacts = Contact.objects.filter(birthdate__isnull=False, user=request.user)

    result = []
    for contact in contacts:
        date_of_birth = contact.birthdate
        date_this_year = date_of_birth.replace(year=today.year)
        if date_this_year < today:
            date_this_year = date_this_year.replace(year=today.year + 1)
        days_to_birthday = (date_this_year - today).days
        if days_to_birthday <= 7:
            result.append(contact)
    return render(request, "contacts/upcoming_birthdays.html", {"contacts": result})
