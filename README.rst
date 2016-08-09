This AVI is developed as part of the tutorial in the GAVIP user manual. Each branch corresponds to a different step in the tutorial.

The complete tutorial is included below

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
    
Create the AVI skeleton
^^^^^^^^^^^^^^^^^^^^^^^

We need to create some AVI code before the AVI will start successfully.

urls.py
*******

Lets begin by creating our ``urls.py``. This file maps urls to different functions. 
We will start off very simply, with one view.

Create ``~/my_first_avi/avi/urls.py`` with the following content::

    from avi import views
    from django.conf.urls import patterns, url

    urlpatterns = patterns(
        url(r'^$', views.index, name='index'),
    )

views.py
********

We saw in ``urls.py`` that we imported ``views``, and mapped an empty URL to ``views.index``. 
So lets create this file now, with an index function.

Create ``~/my_first_avi/avi/views.py`` with the following content::
    
    

