# [FootHub-FC](https://foothubfc.herokuapp.com)


watch today's latest international football highlights from every league around the world. 

⚽⚽⚽⚽⚽⚽⚽⚽


**This project is built with Django 2.2.6**

You can view a working version of this app
[here](https://foothubfc.herokuapp.com/)


Setting up FootHubFC to work in Django is very easy. You need to
make changes to requirements.txt, settings.py, and any app code that
you want cached. These changes are covered in detail below.


![Deploy](https://www.herokucdn.com/deploy/button.png)

## Building

It is best to use the python `virtualenv` tool to build locally:


```sh
$ virtualenv-2.7 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ DEVELOPMENT=1 python manage.py runserver
```

Then visit `http://localhost:8000` to view the app. 




## requirements.txt

Run the following
commands to install the necessary pips:

```sh
$ pip install -r requirements.txt
```







