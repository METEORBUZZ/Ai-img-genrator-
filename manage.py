#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # Normalize npm / environment arguments like --port 3000 --host 0.0.0.0 if passed to runserver
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        filtered_args = [sys.argv[0], sys.argv[1]]
        host = '0.0.0.0'
        port = '3000'
        addrport_set = False
        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg in ('--port', '-p') and i + 1 < len(sys.argv):
                port = sys.argv[i + 1]
                i += 2
            elif arg.startswith('--port='):
                port = arg.split('=', 1)[1]
                i += 1
            elif arg in ('--host', '-H') and i + 1 < len(sys.argv):
                host = sys.argv[i + 1]
                i += 2
            elif arg.startswith('--host='):
                host = arg.split('=', 1)[1]
                i += 1
            elif not arg.startswith('-') and ':' in arg:
                # Direct host:port provided
                host, port = arg.split(':', 1)
                addrport_set = True
                i += 1
            elif not arg.startswith('-') and arg.isdigit():
                port = arg
                addrport_set = True
                i += 1
            else:
                filtered_args.append(arg)
                i += 1
        # Insert target addrport
        filtered_args.insert(2, f"{host}:{port}")
        sys.argv = filtered_args

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
