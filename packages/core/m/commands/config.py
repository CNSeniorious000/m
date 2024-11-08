from ast import literal_eval
from contextlib import suppress

from m.utils.console import console
from rich import print_json
from typer import Exit, Typer
from typer.params import Argument, Option

from ..config.load import load_config, read_json_config, write_json_config
from ..utils.helpers import UNSET, wrap_raw_config
from ..utils.path import global_store, local_store

app = Typer()


@app.command(help="Manage configuration.")
def config(
    item: str = Argument("", help="The item to retrieve from the config. Leave empty to retrieve the entire config."),
    value: str = Argument("", help="The value to set the item to. Leave empty to retrieve the item."),
    local: bool = Option(True, "--global", "-g", flag_value=False, help="Persistent config in User's home directory instead of this python venv.", show_default=False),
):
    store = local_store if local else global_store
    config = wrap_raw_config(read_json_config(store)) if item else load_config()  # merge unless the verb is set

    match (item, value):
        case ("", ""):
            print_json(data=dict(config))
        case (item, ""):
            for item in item.split("."):
                if isinstance(config, dict):
                    config = config[item]
                elif isinstance(config, list):
                    config = config[int(item)]
                else:
                    break

            if config is not UNSET:
                print_json(data=config)

        case (item, value):
            new_config: dict = dict(config) if isinstance(config, dict) else {}

            obj = new_config
            parts = item.split(".")
            for part in parts[:-1]:
                if isinstance(obj, dict):
                    obj = obj.setdefault(part, {})
                elif isinstance(obj, list):
                    obj = obj[int(part)]
                else:
                    raise ValueError(f"Invalid config path: {item} on {part}: {obj}")

            with suppress(TypeError, ValueError, SyntaxError):
                value = literal_eval(value)

            if not isinstance(obj, dict):
                console.print(f"Mutating on `{obj}` is not supported yet.", style="red")
                raise Exit(1)

            obj[parts[-1]] = value

            write_json_config(store, new_config)  # type: ignore