# Prerequisites
* Python
* git
* Internet Access

Run all the code in the given order, in one session, to maintain the context in ```cmd```
# Django Assistant
This project is an asssistant that runs on the django framework.
There is no security built in to this project. This means that if this project is available to the World Wide Web or another device, it may put your device at serious risk.
# Windows Setup
## Create and Activate Python Virtual Environment
Run ```py -m venv <venv name>```.
Then run ```<venv name>/Scripts/activate```.
## Clone the Django project
Clone the repository. ```git clone https://github.com/cvaz1306/assistant_django.git```
Then ```cd assistant_django``` to move into the cloned directory. Install the required packages: ```pip install -r requirements.txt```.
## Run the server
To run the development server, run ```py manage.py runserver``` or ```py manage.py runserver <optional:ip address:port>``` to run on a specific IP address and port, for instance ```py manage.py runserver 127.0.0.1:8080```
