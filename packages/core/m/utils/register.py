from typer import Typer


def get_commands():
    from importlib import import_module
    from pkgutil import iter_modules

    commands = import_module("m.commands")

    for info in iter_modules(commands.__path__):
        module = import_module(f"m.commands.{info.name}")
        app = getattr(module, "app")
        if isinstance(app, Typer):
            if not app.info.name:
                app.info.name = info.name
            yield app
        elif app is None:
            print(f"{info.name} is not a command")
        else:
            raise TypeError(f"{app} is not a Typer app")
