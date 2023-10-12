###########
Quick start
###########

Start in 3 steps
=================

1. Install AimOS
.. code-block:: console
  
    pip install aimos

2. Initialize AimOS in your project

.. code-block:: python

  from aimstack.base import Run, Metric

  # Create a run
  run = Run()

  run['hparams'] = {
      'lr': 0.001,
      'batch_size': 32
  }

  # Create a metric
  metric = Metric(run, name='loss', context={'epoch': 1})

  for i in range(1000):
        metric.track(i, epoch=1)

3. Run AimOS Server

.. code-block:: console
  
  aimos server

4. Run AimOS UI

.. code-block:: console
  
  aimos ui

Log your first project with AimOS
===============================

AimOS saves the logs into a `Repo`. Repo is a collection of `Container` objects.
ML training `Run` is kind of a `Container`. 

Container is a set of `Sequence` objects interconnected by config dictionaries.

`Sequence` is a sequence of `Record` objects.

`Metric` is a Sequence of `Number` objects.

Hyperparameters and environment variables are examples of a config dictionary.

Default AimOS installation includes the `aimstack.base` app which contains all the primitives for logging.

Here is how to add AimOS to your project and start logging straight away.

Logger configuration
--------------------
In this example, we use the default Run.

.. code-block:: python

  from aimstack.base import Run  

  # Create a run
  aim_run = Run(repo='/path/to/repo/.aim')

It's also possible to run AimOS remotely, in that case the repo will be the destination of the remote aimos deployment.

Configure and log the run
-------------------------

Once Run is initialized, you can configure it with parameters and log the run.

.. code-block:: python

  # Set run parameters
  aim_run['hparams'] = {
      'lr': 0.001,
      'batch_size': 32
  }

  # create a metric 
  my_metric = Metric(aim_run, name='my-metric', context={'env': 'aim-test'})

  my_metric.track(0.0002)
  my_metric.track(0.0003)
  my_metric.track(0.0004)

You can create as many metrics and other sequences as your project requires.
Fundamentally AimOS provides all the tools to log everything from everywhere.

Integration with ML frameworks
==============================

The AimOS experiment tracker app is well-integrated with major ML frameworks and libraries.

Those integrations are apps and are part of default AimOS installation.

.. code-block:: python

  from aimstack.pytorch_lightning_tracker.loggers import BaseLogger as AimLogger

Pytorch Lightning example
-------------------------

Pytorch lighting provides trainer objects to simplify the training process of pytorch model. 
One of the parameters is called logger. 
We can use the logger function defined by aim to simplify the process of tracking experiments. 
This process is divided into 2 steps:

Step 1. Create AimLogger object

.. code-block::  python

  # track experimental data by using AimOS   aim_logger = AimLogger(
      experiment='aim_on_pt_lightning',
      train_metric_prefix='train_',
      val_metric_prefix='val_',
  )

Step 2. Pass the aim_logger object as the logger argument

.. code-block:: python

  # track experimental data by using AimOS
  trainer = Trainer(gpus=1, progress_bar_refresh_rate=20, max_epochs=5, logger=aim_logger)
