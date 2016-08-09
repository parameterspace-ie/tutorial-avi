.. _reference-tutorial:

=========================
AVI Development Tutorial
=========================

In this tutorial we will build an AVI from scratch. 
The AVI will start off very simply, then move on to using the Django Rest Framework, then finish by introducing a custom HTML view.
The analysis within the AVI will be quite basic and will not evolve during the tutorial.

For every phase of the tutorial, all the code will be available on GitHub in a branch corresponding to the tutorial phase.
The GitHub link will be provided at the start of that phase.

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

---------------------------------
Phase 1: Create the AVI skeleton
---------------------------------

In this phase of the tutorial, we are going to make the files that the AVI needs to startup.
The code that you should expect to have at the end of this tutorial is available at https://github.com/parameterspace-ie/tutorial-avi/tree/skeleton

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

---------------------------
Phase 2: Lets add analysis
---------------------------

In this phase of the tutorial, we are going to add a pipeline for the AVI to run. 
We are then going to create a model so we can store and add parameters to the pipeline.

The code that you should expect to have at the end of this tutorial is available at https://github.com/parameterspace-ie/tutorial-avi/tree/skeleton


tasks.py
^^^^^^^^

All pipelines must be available in ``tasks.py``. We are going to create a basic analysis pipeline which uses a basic implementation of the Fibonacci sequence to do some work.

Add the following to ``tasks.py``::
    
    import os
    from django.conf import settings
    # Class used for creating pipeline tasks
    from pipeline.classes import (
        AviTask,
        AviParameter, AviLocalTarget,
    )


    def fib(n):
        if n == 1:
            return 1
        elif n == 0:   
            return 0            
        else:                      
            return fib(n-1) + fib(n-2)


    class CalcFib(AviTask):
        fib_num = AviParameter()

        def output(self):
            return AviLocalTarget(os.path.join(
                settings.OUTPUT_PATH, 
                "fib_%s.txt" % self.fib_num
            ))

        def run(self):
            fib_result = fib(self.fib_num)
            with open(self.output().path, 'wb') as out:
                print fib_result
                out.write("%s number in fib sequence is %s" % (self.fib_num, fib_result))


This forms a very basic pipeline task with no dependencies. 
If we wanted to create a more complex pipeline, we could add a ``requires()`` method to specify a dependency.
The example AVIs provide several examples of pipelines with dependencies.
The pipeline is built on Luigi, and the `Luigi documentation`_ can be used as a resource for pipeline development.

models.py
^^^^^^^^^

We will now create a model to store the parameters for the pipeline. The pipeline will read these parameters, and the AVI interface will set them.

Add the following to ``models.py`` to create the `TutorialModel`::

    from django.db import models
    from pipeline.models import AviJob


    class TutorialModel(AviJob):
        fib_num = models.IntegerField()
        pipeline_task = "CalcFib"

        def get_absolute_url(self):
            return "%i/" % self.pk

The model has two parameters, ``fib_num`` and ``pipeline_task``.
``fib_num`` must match the parameter required by the pipeline we created in ``tasks.py``. 
The ``pipeline_task`` parameter maps this model to the pipeline task we have made earlier. 
Because this model extends ``AviJob``, it initiates the pipeline task when this model is saved.

There are additional parameters provided by the AviJob class which can be overwritten to adjust how the pipeline is executed. 
For example, the RAM to be allocated to the pipeline can be specified.

**Note:**
Now that we have added a model to represent some data, we have to synchronize our AVI database so that it has the necessary tables to store the models.

This is explained in the next section *Update the AVI*.

views.py
^^^^^^^^

Once we have created the model, and the tasks, we need a way to create an instance of the ``TutorialModel`` to initiate the pipeline.

Add the following import and function to ``views.py``::

    from avi.models import TutorialModel
    ...
    def create(request, fib):
        tutmod, created = TutorialModel.objects.get_or_create(
            fib_num=fib
        )
        context = {
            "tutmod": tutmod,
            "fib": fib
        }
        return render(request, 'avi/create.html', context)

Note that we are taking in a parameter in the function, and using that to populate the model.
We are also using a new template to render a response.
We could use the ``create()`` function rather than ``get_or_create()`` but in this case, it allows us to retrieve a model instance if it already exists. 
We will use this to pass an existing model instance if it exists, and display its job status using the ``create.html`` template. 
In the context we also pass in the created model instance, we will use this in the template.

templates/avi/create.html
^^^^^^^^^^^^^^^^^^^^^^^^^

Put the following in ``templates/avi/create.html``::

    <p>We have created a TutorialModel instance, with fib={{fib}}</p>
    <p>The PrimaryKey of the model instance is {{tutmod.pk}}.</p>
    <p>The job status is {{tutmod.request.pipeline_state.state}}</p>

Note that in this response we show the primary key of the new model instance, we also show the status of the job using the associated pipeline_state model. For more details on the internal structure of the pipeline models and their available fields, refer to the AVI Framework documentation. 

urls.py
^^^^^^^

Since we have created a new view function, we need to map a URL to it. Remember that the view function also expected an additional parameter `fib`. We are going to build that in to the url structure, so that we can navigate to ``/10`` to run this view with ``fib`` set to ``10``.

Modify  ``urls.py`` so that the **urlpatterns** are as follows::
    
    urlpatterns = patterns(
        '',
        url(r'^$', views.index, name='index'),
        url(r'^(?P<fib>[0-9]+)$', views.create, name='create'),
    )


--------------
Update the AVI
--------------

We now have an analysis pipeline, and a model to provide its arguments. 
When writing updates to the front-end, the AVI updates automatically. 
However, the back-end needs to have the worker process restarted so that the pipeline is loaded up.
Because we have added a model to our AVI, we also need to prepare the database. 

In this step, we are going to open Bash inside of the container, access the Supervisor command line interface, synchronize the database and restart the worker. 
Alternatively, you could restart the whole container once its ID is known by running ``docker restart <id>``.

Access the AVI
^^^^^^^^^^^^^^

First we need to get the container ID, so that we can access it. 
This is the same ID that was returned when we ran the ``docker run`` command from earlier.
To determine the container ID, we run ``docker ps`` to list all running containers.
You should see a single container in a list, including its "CONTAINER ID" and "NAMES".

To access the AVI, run ``docker exec -it <container id> bash`` which will run bash interactively within the container.

Access Supervisor
^^^^^^^^^^^^^^^^^^

Once inside the container, you can run ``ps -ef`` to see all processes being run.

#. Run ``supervisorctl`` to access supervisor, you should get a supervisor prompt once this command is run.
#. Run ``status`` to view all supervisor processes and their status. 

Synchronize the database
^^^^^^^^^^^^^^^^^^^^^^^^

While in the supervisor prompt (it should look like ``supervisor> ``) run::
    
    start prepare_avi

This job will synchronize the database with our AVI models. This job is run automatically when the AVI starts up; so if you like you can restart the AVI instead of logging in.

Restart the worker
^^^^^^^^^^^^^^^^^^

While in the supervisor prompt (it should look like ``supervisor> ``) run::

    restart worker-avi
    status


This will restart the worker, causing it to reload the contents of ``tasks.py``
Running status afterwards will show us the status of the jobs, at which point we verify the ``worker-avi`` process is in a RUNNING state after the restart. 

View the changes
^^^^^^^^^^^^^^^^

Now that we have created a pipeline, and a model, and a view to create an instance of the model, lets look at the results.

#. Lets navigate to http://localhost:10000/avi and we will see the usual page
#. Navigate to http://localhost:10000/avi/10 and we will see a different response using our ``create.html`` template.
#. For the URL given, we should expect the following response::
    
    We have created a TutorialModel instance, with fib=10
    The PrimaryKey of the model instance is 28.
    The job status is PENDING

Although this response doesn't seem like much, a lot has happened in the background.

#. A new model has been created, which when it got saved created a new job request for the worker.
#. The worker then immediately retrieved the job request, retrieved the pipeline arguments from the model, and started running its pipeline
#. The progress of the job was then automatically stored in the job model.
#. Once complete, the result should have been saved to the output directory (see the last line of our pipeline)

So now, if we refresh the page http://localhost:10000/avi/10 the status should have updated to "SUCCESS" from "PENDING"
If that is the case, if you navigate to ``~/my_first_avi/data/output`` we should see a ``fib_10.txt`` which contains the result!

Congratulations, you now have a functioning AVI that users can interact with, and your first analysis pipeline.

-------------------------------
Using the Django Rest Framework
-------------------------------

At this point we have a functioning AVI. But the interface is a bit dull and a bit limited (what if we wanted a second parameter in our pipeline?)

So in this step of the tutorial, we are going to improve our interface (without any additional HTML) by adding views using the Django Rest Framework.

.. _Luigi documentation: http://luigi.readthedocs.io/en/latest/example_top_artists.html
