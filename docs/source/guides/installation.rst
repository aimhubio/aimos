#############
 Installation
#############

In this section you will learn how to set up basic AimOS This section shows a simple end-to-end aimos setup. It starts from the installation, shows how to run AimOS UI and explore the
results.
Use this as a starting point to get familiar with the basics of AimOS while getting up and running.

Installing AimOS
==============

AimOS is a python package available for Linux and MacOs for Python versions 3.6+. Install AimOS using `pip3`:

.. code-block:: console

  pip3 install aimos

Verify aim was properly installed

.. code-block:: console
  
  aimos version

You should see the line listing newly installed version of AimOS. For instance:

.. code-block:: none

  AimOS v1.0.0

The installed package includes Python SDK needed for tracking training runs, UI for browsing the results and CLI
for managing UI and results.