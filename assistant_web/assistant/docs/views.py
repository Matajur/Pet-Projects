from django.shortcuts import render, redirect
from .forms import UploadFileForm, RenameFileForm
from .models import File
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def user_files(request):
    """
    The user_files function is responsible for handling the user's files.
    It allows users to upload new files, and displays all of their uploaded
    files in a table. The function also handles filtering by file category.

    :param request: Get the request object
    :return: The user_files
    :doc-author: Trelent
    """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.category = File.determine_category(file_instance.file.name)
            file_instance.display_name = (
                file_instance.get_display_filename()
            )  # setting a "display" name
            file_instance.save()
            # To not show the form after loading, let's redirect the user
            return redirect("docs:user_files")

    files = File.objects.filter(user=request.user)
    # Get all the unique categories that belong to the user
    file_categories = files.values_list("category", flat=True).distinct()

    context = {"files": files, "file_categories": file_categories}

    return render(request, "docs/user_files.html", context)


from .forms import RenameFileForm


def rename_file(request):
    """
    The rename_file function is called when the user clicks on a file in the File Manager and then clicks on the &quot;Rename&quot; button.
    The function takes in two parameters:
        1) The ID of the file to be renamed (file_id)
        2) The new name for that file (new_name).  This value is taken from an input field with id=&quot;rename-input&quot;.  It's important to note that this value does not include any path information, just a filename.
    The rename_file function first gets an instance of File using its ID, then sets its display name to new_name and

    :param request: Get the request object from the client
    :return: A jsonresponse object
    :doc-author: Trelent
    """
    if request.method == "POST":
        try:
            file_id = request.POST.get("file_id")
            new_name = request.POST.get("new_name")

            file_instance = File.objects.get(id=file_id)
            file_instance.display_name = new_name
            file_instance.save()

            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})


def delete_file(request):
    """
    The delete_file function is called when the user clicks on the delete button
    on a file in their list of files. It deletes that file from both the database and
    the server.

    :param request: Get the request object
    :return: A jsonresponse object with a status of success or error
    :doc-author: Trelent
    """
    if request.method == "POST":
        try:
            file_id = request.POST.get("file_id")
            file_instance = File.objects.get(id=file_id, user=request.user)
            file_instance.file.delete()  # this will delete the file from the server
            file_instance.delete()  # this will delete the record from the database
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})
