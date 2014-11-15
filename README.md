Womoobox
=========
Womoobox is a very simple backend for a Firefox app: **[Meuh](https://marketplace.firefox.com/app/meuh)**.

Goal of this backend is to store and display the locations of every Moo generated in the world by the mobile app. 

A Moo can be generated with different types of animals and is represented by different pictures (according to the selected animal) on a [OpenStreet-map](http://openstreetmap.org) layer.

Prerequisites
-------------
Womoobox needs the following packages:

 - Python >= 3.3
 - Django >= 1.7
 - Python-gettext >= 2.1


You'll need a working Django project. If you dont't already have one:
> django-admin startproject myproject
> cd myproject/

Get & configure Womoobox
------------------------
Checkout code from github reposirory
> git clone https

Add the app to your `INSTALLED_APPS` in your project settings: `./myproject/settings.py`
You can also change some settings for womoobox in the app settings file: `./myproject/womoobox/settings.py`

Configure URLs by adding following lines to the myproject/urls.py file:
```
from womoobox.urls import womooboxpatterns

# include Womoobox patterns
urlpatterns += womooboxpatterns
```

Configure database:
> python manage.py migrate

Run app
-------
You can **test** womoobox app by using the django-integrated server:
> python manage.py runserver

This server will serve application on http://127.0.0.1:8000/

Some informations
-----------------
By default, your django project will use a sqlite database backend. You can choose an other djando-supported backend. Please refer to the [official django docs](https://docs.djangoproject.com/en/1.7/ref/databases/).

For production deploiments, please also refer to the [official django docs](https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/).