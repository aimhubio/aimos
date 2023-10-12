from aimstack.base import Run, Metric
from aimos import Repo

repo = Repo('.', read_only=False)

# Initialize a new run
run = Run(repo=repo)

# Log run parameters
run["hparams"] = {
    "learning_rate": 0.001,
    "batch_size": 32,
}

# Init a metric
metric = Metric(run, name='loss', context={'subset': 'training'})

for i in range(1000):
    metric.track(i, epoch=1)
