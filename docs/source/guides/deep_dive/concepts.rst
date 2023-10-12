########
Concepts
########

Overview
========

AimOS is built around three main aspects, each focusing on different pillar of the
logging and logs analysis process:

- **Logging**: Log any type of data from any source.
- **Observability**: Create your own UI pages, via AimOS boards, explorers, and reports.
- **Automations**(TODO): Automate processes, actions, and set up alerts on anything you have logged.

Together, they form the foundation of the AimOS operating system for logs, providing a powerful and flexible framework
for building any kind of logging and visualization apps.

**AimOS fundamentally provides the building "Lego" blocks for building, distributing and running any kind of logging, observability and telemetry apps.**


.. mermaid::

  mindmap
    root((AimOS))
      Observability
        Explorers
        Boards
        Reports
      Logging
        Objects
        Sequences
        Collections
      Automations
        Callbacks
        Notifications
        Monitoring


.. toctree::
  :maxdepth: 2
  :caption: ⚡ Concepts
  :hidden:

  ./concepts/logging.rst
  ./concepts/observability.rst
  ./concepts/automations.rst
  ./concepts/apps.rst
  ./concepts/repo.rst