from aimstack.base import Run as BaseRun
from aimos import Property


class TrainingRun(BaseRun):
    experiment = Property(default='default')
