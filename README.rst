.. _reference-tutorial:

=========================
AVI Development Tutorial
=========================

In this tutorial we will build an AVI from scratch. 
The AVI will start off very simply, then move on to using the Django Rest Framework, then finish by introducing a custom HTML view.
The analysis within the AVI will be quite basic and will not evolve during the tutorial.

---------
AVI Recap
---------

First, lets recall some details about AVIs

#. AVI's are run via the AVI framework, isolated within a Docker container (AVI Container). 
#. AVI's consist of an interface and one or more pipelines.
#. When developing an AVI, both of these components operate simultaneously in the AVI Container.
#. When an AVI runs, it persists data on a mounted volume 
#. When a user runs the AVI within the platform, they just run the AVI interface.
    
    #. The user then queues jobs within the platform, rather than running them immediately.
    #. GAVIP then handles resource allocation, and runs the pipeline when appropriate.

So, during development, we are going to run both the interface and pipelines simultaneously, within a container.

-----------------
Preparing the AVI
-----------------

For the AVI to work it needs the following

#. The AVI Container (built from the AVI template)
#. The AVI code mounted in to the AVI framework (the framework is provided by the AVI template)
#. A data volume to store logs and results

Download the AVI template
^^^^^^^^^^^^^^^^^^^^^^^^^

To download the AVI template, run ``docker pull repositories.gavip.science/<AVI template>:<version>`` ::

    docker pull repositories.gavip.science/ps_avi_python:0.2.10

The ``ps_avi_python:0.2.10`` AVI template is fine for this tutorial, but if you need a Java runtime or Python 3, you will want to use a different template.

Create the AVI directories
^^^^^^^^^^^^^^^^^^^^^^^^^^

Lets create a directory to store the AVI code, and the AVI data::

    mkdir ~/my_first_avi
    cd ~/my_first_avi
    mkdir data avi # Create the data and code folders
    cd ~/my_first_avi/data
    mkdir input output logs db # Create the data subdirectories

Now we have created a folder for our AVI code ``~/my_first_avi/avi`` and a data directory which will store our database, logs, analysis inputs and outputs ``~/my_first_avi/data``.

-----------------------
Create the AVI skeleton
-----------------------

We need to create some AVI code before the AVI will start successfully.

__init__.py
^^^^^^^^^^^^^^^^^^^^^^^^

Before writing any code, create this file so the AVI framework recognizes our AVI folder as an application.

urls.py
^^^^^^^^^^^^^^^^^^^^^^^^

Lets begin by creating our ``urls.py``. This file maps urls to different functions. 
We will start off very simply, with one view.

Create ``~/my_first_avi/avi/urls.py`` with the following content::

    from avi import views
    from django.conf.urls import patterns, url

    urlpatterns = patterns(
        '',
        url(r'^$', views.index, name='index'),
    )

views.py
^^^^^^^^^^^^^^^^^^^^^^^^

We saw in ``urls.py`` that we imported ``views``, and mapped an empty URL to ``views.index``. 
So lets create this file now, with an index function.

Create ``~/my_first_avi/avi/views.py`` with the following content::
    
    from django.shortcuts import render

    def index(request):
        context = {
            "name": "John Smith"
        }
        return render(request, 'avi/index.html', context)

This index function is creating a context dictionary, and using that to render a HTML response using a template at ``avi/index.html``. We haven't created that template yet, that's the next step.

templates/avi/index.html
^^^^^^^^^^^^^^^^^^^^^^^^

Our view function ``index()`` is rendering a response using a template. We will now create that template, and use the context to alter the response.

Create ``~/my_first_avi/avi/templates/avi/index.html``. Note that the render function takes 'avi/index.html' as a parameter. We could use 'foo/index.html' and use the same parameter in the render function. Put the following in the template::

    Hello {{name}}!


The tutorial up to this point is available at: https://github.com/parameterspace-ie/tutorial-avi/tree/skeleton

-------------------
Start up the AVI
-------------------

Now that we have a skeleton AVI, lets start our AVI and look at the results.

Run the following command to start the AVI. The individual parts of the command are explained below separately::

    docker run -dit \
        -e SETTINGS=settings.standalone \
        -v ~/my_first_avi/data:/data \
        -v ~/my_first_avi/avi:/opt/gavip_avi/avi \
        -p 10000:10000 \
        repositories.gavip.science/ps_avi_python:develop \
        supervisord

:docker run -dit: Docker creates and starts a container in detached mode, with a pseudo-tty, keeping STDIN open if not attached. See docker docs for more: https://docs.docker.com/engine/reference/run/ 
:-e SETTINGS=settings.standalone: We set the SETTINGS environment variable to settings.standalone to start the AVI in standalone mode.
:-v .../data: Mount the data folder into the AVI
:-v .../avi: Mount the avi code folder into the AVI
:-p ...10000: Map port 10000 within the container to port 10000 on this computer (the web interface starts on port 10000 in the container)
:repositories.....develop: Use the ``ps_avi_python:develop`` template for the container
:supervisord: Run supervisord when the container starts (this starts the AVI pipeline workers, and AVI interface web servers)

Now that the AVI has started up, navigate to http://localhost:10000 to view your AVI.
You should get redirected to http://localhost:10000/avi/ and see "Hello John Smith!"
