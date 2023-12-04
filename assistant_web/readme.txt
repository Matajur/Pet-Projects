Personal Assistant

1.0.0

README

Thank you for using Personal Assistant!

Installing Personal Assistant from Project Team 3
=================================================
1.  Download the open source application from https://github.com/Matajur/teamwork_2
2.  Install Python v3.10 or later
3.  Install Docker v4.10 or later
4.  Install DBeaver v23.2 or later or any other SQL database client
5.  Open the application root directory on the console
6.  Input -> pip install poetry
7.  Input -> poetry shell
8.  Input -> poetry install
9.  Input -> cd assistant
10. Create your own on-premise or web based PostgreSQL database using hosts like ElephantSQL (see db host provider instructions):
    In case of the on-premise db Input -> docker run --name <your_container_name> -p 5432:5432 -e POSTGRES_PASSWORD=<your_connection_password> -d postgres
11. Add the .env file to the 'assistant' folder using .env.example as a template (make sure .env is added to .gitignore and .dockerignore)
12. Configure the .env file according to the database name, user, password and host
13. Create your own email host to send confirmation emails (see email host provider's instructions)
14. Configure the .env file according to your email host
15. Create your own cloud file storage (see cloud service provider instructions)
16. Customize the .env file according to your cloud storage
17. Create your own secret key in the .env file
18. Get the News API key and paste it into the .env file
19. Input -> python manage.py migrate
20. For testing on localhost Input -> python manage.py runserver
21. After completing local testing Input -> cd ..
22. Create your own account on the web platform to deploy the application and install its client:
    In the case of the Fly.io web platform to install the client Input -> powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
23. Input -> fly launch
24. Add fly.toml to .gitignore and .dockerignore and paste the contents of the .env file into the [env] section of the fly.toml
25. Input -> fly deploy
26. To see the deployed application in the browser Input -> fly open
27. Enjoy! https://lively-butterfly-4696.fly.dev/

Sincerely yours,
Project Team 3
