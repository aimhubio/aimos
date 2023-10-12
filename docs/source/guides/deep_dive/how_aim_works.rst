#############
How AimOS works
#############

Overview
========
AimOS has three main layers - Storage, SDK and core with the components of cli, logging server and web ui.
All of these together enable AimOS to log large quantities of data and view them through apps and explorers.

.. image:: https://docs-blobs.s3.us-east-2.amazonaws.com/v4-images/guides/aim-structure.png
    :width: 80%
    :align: center
    :alt: AimOS structure
 
Using AimOS
==============

The main usage of AimOS is through its logging apps - default or user-built.
The logging apps either contain the type of data to be logged or you can just use the primitive types.

Once you have installed AimOS and the apps you need, here are the steps to make

- Integrate AimOS logger to your code
- Start AimOS server (if not already running)
- Start AimOS UI
- Run your code
- Go to AimOS UI and you will see the data logged.

.. image:: https://docs-blobs.s3.us-east-2.amazonaws.com/v4-images/guides/aim-logs-overview.png
    :width: 100%
    :align: center
    :alt: AimOS logs overview

Behind the scenes
=================

Server
----------
When logging with AimOS, all the logs are sent to the AimOS Server which is responsible to storing the logs in the storage.
AimOS Server uses AimOS SDK as well as AimOS Storage to do its job.

SDK
-------
The AimOS SDK provides the main API and abstractions for AimOS. AimOS SDK also contains the components that enable the apps.
SDK is the library that gets installed when you install AimOS. It is used across the board by all the rest of the AimOS components.

AimOS SDK is responsible for connecting with the AimOS Storage as well as the main AimOS abstractions everything else is built on.

CLI
---
The AimOS CLI is a command line interface to managing AimOS. It is used to start the AimOS Server, AimOS UI and manipulate with other AimOS components.
AimOS CLI is one of the primary AimOS components.

After logging
-------------
Once the data is logged, it is available to be queried via SDK or observed via AimOS UI.
The Web Server is responsible for serving the serialized logged data to the UI.
Web Server is started when the `aimos ui` CLI command is invoked.

Web UI
------
AimOS web UI is where the apps are displayed and the data is visualized.
It has three main features

- Apps
- Explorers 
- Reports

All of these apps use the logged data through the AimOS UI SDK or through explorers.

AimOS UI SDK
----------
AimOS UI SDK is a pythonic interface that allows to query the logged data and use it in the AimOS UI as part of the apps via wide variety of visualization components.

.. image:: https://docs-blobs.s3.us-east-2.amazonaws.com/v4-images/guides/aim-apps-edit-mode.png
    :width: 100%
    :align: center
    :alt: AimOS apps edit mode