from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    CATEGORY_CHOICES = [
        ("image", "Image"),
        ("document", "Document"),
        ("video", "Video"),
        ("audio", "Audio"),
        ("archive", "Archive"),
        ("other", "Other"),
    ]

    file = models.FileField(upload_to="files/")  # the file itself to be saved
    upload_date = models.DateTimeField(auto_now_add=True)  # download date
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES
    )  # file category
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # the user who uploaded the file
    display_name = models.CharField(
        max_length=255, blank=True, null=True
    )  # the name of the file to be displayed

    def __str__(self):
        """
        The __str__ function is used to return a string representation of the object.
        This is what you see when you print an object, or use str(object).


        :param self: Represent the instance of the class
        :return: The filename
        :doc-author: Trelent
        """
        return self.get_display_filename()

    def get_display_filename(self):
        """
        The get_display_filename function returns the display name of a file, if it has one.
        If not, it returns the filename without its extension or prefix.

        :param self: Represent the instance of the object itself
        :return: The name of the file without the extension and prefix &quot;_xxxxxx&quot;
        :doc-author: Trelent
        """
        if self.display_name:
            return self.display_name
        # Cut off the prefix and file extension
        name_without_extension = self.file.name.rsplit(".", 1)[0]
        displayed_name = name_without_extension[:-7]  # Cut off the prefix "_хххххх"
        # return displayed_name or "Unnamed File"
        return name_without_extension or "Unnamed File"

    @staticmethod
    def determine_category(filename):
        """
        The determine_category function takes a filename as an argument and returns the category of that file.

        :param filename: Determine the file extension
        :return: A string
        :doc-author: Trelent
        """
        # Category definition based on file extension
        IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "bmp", "gif", "svg", "tiff", "webp"]
        DOCUMENT_EXTENSIONS = [
            "pdf",
            "doc",
            "docx",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
            "odt",
            "ods",
            "txt",
        ]
        VIDEO_EXTENSIONS = ["mp4", "mkv", "flv", "avi", "mov", "wmv"]
        AUDIO_EXTENSIONS = ["mp3", "wav", "ogg", "m4a", "aac", "flac"]
        ARCHIVE_EXTENSIONS = ["zip", "rar", "7z", "tar", "gz"]

        extension = filename.split(".")[-1].lower()

        if extension in IMAGE_EXTENSIONS:
            return "image"
        elif extension in DOCUMENT_EXTENSIONS:
            return "document"
        elif extension in VIDEO_EXTENSIONS:
            return "video"
        elif extension in AUDIO_EXTENSIONS:
            return "audio"
        elif extension in ARCHIVE_EXTENSIONS:
            return "archive"
        else:
            return "other"
