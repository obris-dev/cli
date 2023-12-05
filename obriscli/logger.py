import sys
import json

import attrs


class Logger:

    @classmethod
    def log_json(cls, message, error=False):
        dumped_msg = json.dumps(message, default=attrs.asdict, indent=4)
        cls.log(f"{dumped_msg}\n", error=error)

    @staticmethod
    def log(message, error=False):
        if error:
            sys.stderr.write(message)
        else:
            sys.stdout.write(message)
