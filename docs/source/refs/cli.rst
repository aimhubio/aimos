===========
 AimOS CLI
===========

AimOS provides command-line interface for launching AimOS UI and tracking servers,
managing AimOS repositories, logged data and AimOS apps.

Below is a brief summary table of AimOS CLI commands:

=========== ===========
Command     Description
=========== ===========
init        Initializes or re-initializes an AimOS repository at a given directory.
server      Starts the AimOS remote tracking server for real-time logging.
ui          Launches the AimOS web-based UI for interactive data exploration.
packages    Command group for managing AimOS packages/apps.
apps        Command group for managing AimOS packages/apps. Alias for **aim packages**
containers  Command group for managing containers within an AimOS repository.
migrate     Migrates the data format of a specified AimOS repository.
version     Prints version of installed AimOS and exists.
=========== ===========

----

API Reference for AimOS Command Line Interface
=============================================

The following section describes AimOS CLI commands in detail.

.. currentmodule:: aimcore.cli
.. automodule:: aimcore.cli

.. click:: aimcore.cli.cli:cli_entry_point
  :prog: aimos
  :nested: full
  :commands: init, server, ui, packages, containers, migrate, version
