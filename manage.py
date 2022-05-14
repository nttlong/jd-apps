#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    import web.settings
    config_path = str(web.settings.BASE_DIR.absolute().joinpath("config.yaml"))
    if not config_path:
        print("no config argumetn found, please call with config= <path to yaml setting>")
    else:
        import ReEngine
        ReEngine.init(config_path)
        assert isinstance(ReEngine.info,dict)
        port =ReEngine.info.get("PORT",None)

        if not port:
            raise Exception("'PORT' was not found in '{}'".format(config_path))
        assert isinstance(port,int),"'PORT' in '{}' must be a number".format(config_path)
        args =[
            sys.argv[0],
            "runserver",
            "0.0.0.0:{}".format(port)
        ]
        ReEngine.apply_settings()
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
