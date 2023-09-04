# Django Assistant
This project is an asssistant that runs on the django framework.
There is no security built in to this project. This means that if this project is available to the World Wide Web or another device, it may put your device at serious risk.
# Windows Setup
## Create and Activate Python Virtual Environment
Run ```py -m venv <venv name>```.
Then run ```<venv name>/Scripts/activate```.
## Install required Python packages
Then ```pip install django``` to install django.
## Create new Django project
Run ```py -m django startproject Assistant```.
Now move into ```Assistant``` directory: ```cd Assistant```
Clone the repository. ```git clone https://github.com/cvaz1306/assistant_django.git```
## Run the server
Then ```cd assistant_django``` to move into the cloned directory.
To run the development server, run ```py manage.py runserver``` or ```py manage.py runserver <optional:ip address:port>``` to run on a specific IP address and port, for instance ```py manage.py runserver 127.0.0.1:8080```
