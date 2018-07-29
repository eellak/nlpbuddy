# Installation

This was tested on **Ubuntu 16.04**, python 3.5 and a python virtualenv. 

A virtualenv is not necessary, though very helpful. We assume installation directory is **/opt/demo-app**. If you plan to install on a different directory, make sure you change references to all files mentioned here. 

It installs Django, all spaCy.io models used in this application, and deploys it through uwsgi and nginx (if you follow the deployment steps) or the simple Django server (if used for development). 

So let's create the directory we'll work and clone this repository as **/opt/demo-app/demo**

```
root@server ~ # mkdir /opt/demo-app
root@server ~ # cd /opt/demo-app
root@server /opt/demo-app # git clone https://github.com/eellak/text-analysis demo
root@server /opt/demo-app # cd demo
root@server /opt/demo-app/demo # 
```

Then install a few dependencies

```
root@server /opt/demo-app/demo # apt-get install -y g++
```

Time to install python packages and dependencies

```
root@server /opt/demo-app/demo # pip install setuptools
root@server /opt/demo-app/demo # pip install --upgrade pip
root@server /opt/demo-app/demo # pip install -r requirements.txt 
```

Next install all spaCy models we'll use

```
root@server /opt/demo-app/demo # python3 -m spacy download en
root@server /opt/demo-app/demo # python3 -m spacy download el # as of 28 July 2018 this is not YET possible
root@server /opt/demo-app/demo # python3 -m spacy download de
root@server /opt/demo-app/demo # python3 -m spacy download es
root@server /opt/demo-app/demo # python3 -m spacy download pt
root@server /opt/demo-app/demo # python3 -m spacy download fr
root@server /opt/demo-app/demo # python3 -m spacy download it
root@server /opt/demo-app/demo # python3 -m spacy download nl
```

## Local development
At that stage, edit file **demo/settings.py** and set 
```
ALLOWED_HOSTS = ['localhost']
```

remove line

```
STATIC_ROOT = BASE_DIR + '/static/'
```

and instead add
```
STATICFILES_DIRS = [os.path.join(BASE_DIR,  'static')]
```
Edit file **nlp/urls.py** and make it:

```
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('nlp.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

Now run Django migrations (though we don't have any Django models, this is necessary for the application)

```
root@server /opt/demo-app/demo # python3 manage.py makemigrations
root@server /opt/demo-app/demo # python3 manage.py migrate
```

Ready to go, just start the simple Django server

```
root@server /opt/demo-app/demo #  python3 manage.py runserver
```
and visit http://localhost:8000 , the app should load there!

## Production deployment

For a production deployment through nginx/uwsgi, there are a few more steps to perform:

Install nginx
```
root@server /opt/demo-app/demo #  apt-get install -y nginx
```

Edit file _deploy/text-analysis-domain_ and set a proper **server_name** to point on your URL

Copy this nginx domain file and enable it
```
root@server /opt/demo-app/demo # cp deploy/text-analysis-domain  /etc/nginx/sites-available/
root@server /opt/demo-app/demo # ln -s  /etc/nginx/sites-available/text-analysis-domain  /etc/nginx/sites-enabled/
root@server /opt/demo-app/demo # cp deploy/uwsgi_params  /etc/nginx/
root@server /opt/demo-app/demo # systemctl restart nginx
```

Now run Django migrations (though we don't have any Django models, this is necessary for the application)

```
root@server /opt/demo-app/demo # python3 manage.py makemigrations
root@server /opt/demo-app/demo # python3 manage.py migrate
```

Edit _demo/settings.py_ and set your **URL** (as in nginx) on **ALLOWED_HOSTS** - remove any other entries there

```
root@server /opt/demo-app/demo # vi demo/settings.py
```


Create a service with name uwsgi on systemd, enable and start it

```
root@server /opt/demo-app/demo # cp deploy/uwsgi.service /etc/systemd/system/uwsgi.service 
root@server /opt/demo-app/demo # systemctl enable  uwsgi.service 
root@server /opt/demo-app/demo # systemctl start uwsgi

```

Now if you visit http://URL you should be able to see the application ;)
