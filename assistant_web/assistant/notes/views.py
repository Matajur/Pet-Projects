from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm


@login_required
def note_list(request):
    """
    The note_list function is a view that displays all notes in the database.
    It also counts how many times each tag appears and sorts them by count.

    :param request: Get the current user
    :return: A template with the notes and tags_count variables
    :doc-author: Trelent
    """
    notes = Note.objects.filter(user=request.user).order_by("tags", "text")
    for note in notes:
        note.tags_list = note.tags.split(",")
    all_tags = set(tag for note in notes for tag in note.tags.split(","))
    tags_count = {
        tag: sum(1 for note in notes if tag in note.tags.split(",")) for tag in all_tags
    }
    sorted_tags_count = {tag: count for tag, count in sorted(tags_count.items())}
    return render(
        request,
        "notes/note_list.html",
        {"notes": notes, "tags_count": sorted_tags_count},
    )


@login_required
def create_note(request):
    """
    The create_note function is a view that allows users to create notes.
        It takes in the request and returns a rendered template with the form for creating notes.
        If the user submits data via POST, it will validate that data and save it to the database.

    :param request: Get the request from the user
    :return: A redirect to the note_list view if the form is valid
    :doc-author: Trelent
    """
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect("notes:note_list")
    else:
        form = NoteForm()
    return render(request, "notes/create_note.html", {"form": form})


@login_required
def edit_note(request, pk):
    """
    The edit_note function takes a request and primary key as arguments.
    It gets the note object from the database using get_object_or_404, which returns an error if it can't find a note with that pk.
    The function then checks whether the request is POST or GET, and if it's POST, saves any changes to the form instance (the edited note).
    If not, it creates an empty form instance for editing.

    :param request: Get the request object
    :param pk: Get the note that we want to delete
    :return: A redirect to the note_list view
    :doc-author: Trelent
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("notes:note_list")
    else:
        form = NoteForm(instance=note)
    return render(request, "notes/edit_note.html", {"form": form, "note": note})


@login_required
def delete_note(request, pk):
    """
    The delete_note function is used to delete a note.
        It takes in the request and pk as parameters, gets the note object or returns 404 if it doesn't exist,
        then checks if the request method is POST. If so, it deletes the note and redirects to notes:note_list.
        Otherwise, it renders a template with &quot;note&quot; as context.

    :param request: Get the request object
    :param pk: Get the note that is going to be deleted
    :return: The delete_note
    :doc-author: Trelent
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":
        note.delete()
        return redirect("notes:note_list")
    return render(request, "notes/delete_note.html", {"note": note})


@login_required
def search_note(request):
    """
    The search_note function takes a request object as an argument.
    The function then gets the query from the request object and checks if it is empty. If it is,
    the user will be redirected to the note_list page. The cleaned_query variable removes any commas or periods
    from the query string and strips any whitespace from both ends of that string. The tags variable splits up
    the cleaned_query into a list of strings based on spaces in between words in that string (e.g., &quot;hello world&quot; would become [&quot;hello&quot;, &quot;world&quot;]). If there are no tags, then we redirect to note

    :param request: Get the request object
    :return: The note_list
    :doc-author: Trelent
    """
    query = request.GET.get("q")
    if not query:
        return redirect("notes:note_list")
    cleaned_query = query.replace(",", "").replace(".", "").strip()

    tags = cleaned_query.split()

    if not tags:
        return redirect("notes:note_list")

    q_objects = Q()
    for tag in tags:
        q_objects |= Q(tags__icontains=tag)

    notes = Note.objects.filter(user=request.user).filter(q_objects)

    for note in notes:
        note.tags_list = note.tags.split(",")

    all_tags = set(tag for note in notes for tag in note.tags.split(","))
    tags_count = {
        tag: sum(1 for note in notes if tag in note.tags.split(",")) for tag in all_tags
    }
    sorted_tags_count = {tag: count for tag, count in sorted(tags_count.items())}
    context = {
        "notes": notes,
        "query": query,
        "tags_count": sorted_tags_count,
    }

    return render(request, "notes/note_list.html", context)
