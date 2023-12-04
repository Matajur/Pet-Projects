# Final teamwork of the section "Python WEB"

Personal assistant for entertainment, contact management and cloud storage for user files

## Technical task for creation of the "Personal Assistant" WEB application

The main functionality of the Web application is made on Django

### Task:

Create a "personal assistant" for entertainment, managing contacts and storing files. Communication with the user must take place through the web interface.

### Basic requirements for the "Personal Assistant" project:

1.  Save contacts with names, addresses, phone numbers, email and birthdays to the contact book;
2.  Display a list of contacts whose birthday is a specified number of days from the current date;
3.  Check the correctness of the entered phone number and email when creating or editing a record and notify the user in case of incorrect entry;
4.  Search for contacts among book contacts;
5.  Edit and delete entries from the contact book;
6.  Keep notes with text information;
7.  Search for notes;
8.  Edit and delete notes;
9.  Add "tags" to notes, keywords describing the subject and subject of the record;
10. Search and sort notes by keywords (tags).
11. Upload user files to the cloud service and have access to them. The user must be able to upload any file to the server through the web interface and download it.
12. Sort user files by categories (images, documents, videos, etc.) and display only the selected category (file filter by category).
13. Provide a brief summary of news for the day. To do this, you should choose any area you are interested in (finance, sports, politics, weather) and several information resources on a given topic. Collect information (news headlines, exchange rates, results of sports events, etc.) from the selected resources at the request of the user and display them on the results page. What exactly to collect and how you can determine yourself.

### Requirements for Authentication:

1.  Implement the user authorization mechanism for “Personal Assistant”. The web interface must allow access to its functions only to registered users.
2.  Each registered user must have access only to his data and files.
3.  Implement password recovery mechanisms for the user by email.


### Admission criteria:

1.  The web interface can be implemented on the Django framework.
2.  The project must be stored in a separate repository and be publicly available (GitHub, GitLab or BitBucket).
3.  The project contains detailed instructions for installation and use.
4.  “Personal Assistant” saves information in the database and can be restarted without data loss.
5.  For reliability and productivity, store all information in the PostgreSQL database.
6.  All critical data for accessing the database and configuring the program are stored in variable environments and are not loaded into the repository.
7.  The project fully implements all points of requirements described in the task.
