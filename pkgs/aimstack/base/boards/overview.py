from experiment_tracker import TrainingRun
from base import Metric
from base import ImageSequence
from base import AudioSequence
from base import TextSequence
import re
import copy


c_hash = session_state.get("container_hash")

search_signal = "search"

if c_hash is None:
    ui.header("Overview")
    form = ui.form("Search", signal=search_signal)
    query = form.text_input(value="")

run = TrainingRun.find(c_hash)


@memoize
def flatten(dictionary, parent_key="", separator="."):
    flattened = {}
    for key, value in dictionary.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened.update(flatten(value, new_key, separator=separator))
        else:
            flattened[new_key] = value
    return flattened


@memoize
def merge_dicts(dict1, dict2):
    merged_dict = dict1.copy()
    merged_dict.update(dict2)
    return merged_dict


if run:
    (row,) = ui.rows(1)

    col1, col2 = row.columns(2)

    with col1:
        # --------------------------------------- run parameters ---------------------------------------
        run_parameters = copy.deepcopy(run)
        if "__system_params" in run_parameters:
            run_parameters.pop("__system_params")
        if "hash" in run_parameters:
            run_parameters.pop("hash")
        for key in run_parameters.keys():
            match = re.match("is_([a-zA-Z0-9_]+)_run", key)
            if match:
                pkg_key = match.group()
                break

        if pkg_key in run_parameters:
            run_parameters.pop(pkg_key)

        if run_parameters:
            ui.subheader("Run Parameters")
            run_parameters_search_signal = "search"

            run_params_form = ui.form("Search", signal=run_parameters_search_signal)

            run_params_query = run_params_form.text_input(value="")

            flatten_run_parameters = flatten(run_parameters)
            params_name = []
            params_values = []
            for key, value in flatten_run_parameters.items():
                pattern = re.compile(
                    f".*{re.escape(run_params_query)}.*", re.IGNORECASE
                )
                match = re.search(pattern, key)
                if match:
                    params_name.append(key)
                    params_values.append(value)

            if params_name and params_values:
                ui.table(
                    {
                        "name": params_name,
                        "value": params_values,
                    }
                )

        # --------------------------------------- metrics ---------------------------------------

        metrics = Metric.filter(f'c.hash=="{c_hash}"')
        metrics_processed = [merge_dicts(m, flatten(m)) for m in metrics]

        if metrics_processed:
            ui.subheader("Metrics")
            metrics_search_signal = "search"

            metrics_form = ui.form("Search", signal=metrics_search_signal)

            metrics_query = metrics_form.text_input(value="")

            params_name = []
            params_values = []
            params_context = []
            for metric in metrics_processed:
                pattern = re.compile(f".*{re.escape(metrics_query)}.*", re.IGNORECASE)
                match = re.search(pattern, metric["name"])
                if match:
                    params_name.append(metric["name"])
                    params_values.append(metric["values"][-1])
                    params_context.append(str(metric["context"]))

            if params_name and params_values and params_context:
                ui.table(
                    {
                        "name": params_name,
                        "last value": params_values,
                        "context": params_context,
                    }
                )

        # # --------------------------------------- system metrics ---------------------------------------

        # ui.subheader('System Metrics')
        # system_metrics_search_signal = "search"

        # system_metrics_form = ui.form('Search', signal=metrics_search_signal)

        # system_metrics_query = system_metrics_form.text_input(value='')

        # system_metrics_parameters = copy.deepcopy(run)
        # system_metrics_parameters = system_metrics_parameters.pop("__system_params")

        # flatten_run_parameters = flatten_dict(system_metrics_parameters)

        # params_name = []
        # params_values = []
        # for key, value in flatten_run_parameters.items():
        #     pattern = re.compile(f".*{re.escape(system_metrics_query)}.*", re.IGNORECASE)
        #     match = re.search(pattern, key)
        #     if match:
        #         params_name.append(key)
        #         params_values.append(value)
        # ui.table({
        #     'name': params_name,
        #     'value': params_values,
        # })

        # --------------------------------------- cli arguments ---------------------------------------

        ui.subheader("CLI Arguments")

        cli_arguments_parameters = copy.deepcopy(run)
        cli_arguments_parameters = cli_arguments_parameters.get("__system_params").get(
            "arguments"
        )
        ui.code(" ".join(cli_arguments_parameters))

        # --------------------------------------- environment variables ---------------------------------------
        environment_variables_parameters = copy.deepcopy(run)
        environment_variables_parameters = environment_variables_parameters.pop(
            "__system_params"
        ).get("env_variables")

        if environment_variables_parameters:
            ui.subheader("Environment Variables")
            env_variables_search_signal = "search"

            env_variables_form = ui.form("Search", signal=env_variables_search_signal)

            env_variables_query = env_variables_form.text_input(value="")

            params_name = []
            params_values = []
            for key, value in environment_variables_parameters.items():
                pattern = re.compile(
                    f".*{re.escape(env_variables_query)}.*", re.IGNORECASE
                )
                match = re.search(pattern, key)
                if match:
                    params_name.append(key)
                    params_values.append(value)

            if params_name and params_values:
                ui.table(
                    {
                        "environment variable": params_name,
                        "value": params_values,
                    }
                )

        # --------------------------------------- packages ---------------------------------------

        packages_parameters = copy.deepcopy(run)
        packages_parameters = packages_parameters.pop("__system_params").get("packages")

        if packages_parameters:
            ui.subheader("Packages")
            packages_search_signal = "search"

            packages_form = ui.form("Search", signal=packages_search_signal)

            packages_query = packages_form.text_input(value="")

            params_name = []
            params_values = []
            for key, value in packages_parameters.items():
                pattern = re.compile(f".*{re.escape(packages_query)}.*", re.IGNORECASE)
                match = re.search(pattern, key)
                if match:
                    params_name.append(key)
                    params_values.append(value)

            if params_name and params_values:
                ui.table(
                    {
                        "package": params_name,
                        "version": params_values,
                    }
                )

    col2.subheader("Information")
    col2.text(f"Created at (date)")
    col2.text(f"Created at (time)")
    col2.text(f"Duration")
    col2.text(f"Run hash: f{run.hash}")

    col2.subheader("Tags")

    col2.subheader("Description")
    col2.text(run.description)

    col2.subheader("Insights")

    images = ImageSequence.filter(f'c.hash=="{c_hash}"')
    audios = AudioSequence.filter(f'c.hash=="{c_hash}"')
    texts = TextSequence.filter(f'c.hash=="{c_hash}"')
    col2.table({
        "component": ["Metrics", "Audios", "Texts", "Images",],
        "quantity": [str(len(metrics_processed)), str(len(audios)), str(len(texts)), str(len(images))]
    })

    # row1.text("Notes")
    # row1.text("0")

    # row3.text("System")
    # row3.text("0")

    # row8.text("Figures")
    # row8.text("0")
else:
    text = ui.text("No run found")
