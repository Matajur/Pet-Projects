from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    tags = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Tag_1, Tag_2, Tag_3"}),
    )

    class Meta:
        model = Note
        fields = ["text", "tags"]

    def clean_tags(self):
        """
        The clean_tags function takes the tags field from the form and splits it into a list of strings.
        It then iterates through each string in that list, adding a comma to any string that doesn't already have one.
        Finally, it joins all but the last item in the list with spaces between them and adds back on to this joined string
        the last item in tag_list without its trailing comma.

        :param self: Access the instance of the class
        :return: A string with all the tags separated by a space
        :doc-author: Trelent
        """
        tags = self.cleaned_data["tags"]

        tag_list = [tag.strip() for tag in tags.split()]

        for index, tag in enumerate(tag_list):
            if "," not in tag:
                tag_list[index] = f"{tag},"

        cleaned_tags = " ".join(tag_list[:-1])
        cleaned_tags += f' {tag_list[-1].strip(",")}'
        return cleaned_tags
