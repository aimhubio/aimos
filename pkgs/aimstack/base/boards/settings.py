from experiment_tracker import TrainingRun
from base import Metric
import re
import copy


c_hash = session_state.get('container_hash')

search_signal = "search"

if c_hash is None:
    ui.header('Settings')
    form = ui.form("Search", signal=search_signal)
    query = form.text_input(value="")

run = TrainingRun.find(c_hash)

row1, row2 = ui.rows(2)
col1, col2 = row1.columns(2)

# col1.subheader("Archive Run")
# col1.text("Archived runs will not appear in search both on Dashboard and Explore.")

# archive_run = col2.switch(
#     checked=False,
#     size='lg'
# )


# col1, col2 = row2.columns(2)

# col1.subheader("Delete Run")
# col1.text("Once you delete a run, there is no going back. Please be certain.")

# col2.link("Delete", "/delete", True)
