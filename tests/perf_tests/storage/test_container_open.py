from tests.perf_tests.base import StorageTestBase
from tests.perf_tests.utils import get_baseline, write_baseline
from tests.perf_tests.storage.utils import (
    collect_sequence_containers,
    open_containers_for_read
)


class TestContainerOpenExecutionTime(StorageTestBase):
    def test_container_open(self):
        test_name = 'test_container_open'
        containers_to_open = collect_sequence_containers()
        execution_time = open_containers_for_read(containers_to_open)
        baseline = get_baseline(test_name)
        if baseline:
            self.assertInRange(execution_time, baseline)
        else:
            write_baseline(test_name, execution_time)
