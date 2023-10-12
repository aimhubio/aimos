#############
Observability
#############

Overview
========
AimOS comes with a low-code pythonic interface for building a rich observability layer.

Anything that's logged can be visualized and connected with other things hat's been logged.

AimOS observability Pythonic SDK allows to truly connect the dots in the AI Systems. From ML experiments to production to LangChain traces to AI System Monitoring.

.. image:: https://docs-blobs.s3.us-east-2.amazonaws.com/v4-images/guides/aim-apps-edit-mode.png
    :width: 100%
    :align: center
    :alt: AimOS apps edit mode

UI Components
=============
AimOS comes with a wide array of UI components bound to the logs and easily rendered through python..
These components range from search to tables and select boxes.
All seemlessly bound to the logged AimOS data.

.. image:: https://docs-blobs.s3.us-east-2.amazonaws.com/v4-images/guides/aim-docs-app.png
    :width: 100%
    :align: center
    :alt: AimOS docs app

|
UI Components can be found in the default Docs App.


Boards
======
The AimOS Boards are the fundamental building block of any kind of aimos-based observability layer.
They are the main UI component that allows to visualize the logged data.
Boards are composed of UI components and data retrieval.
Boards can be reused between themselves. Each page is also a board.

