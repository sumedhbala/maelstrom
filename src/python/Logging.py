import Locks
import sys


def log_stderr(msg):
    with Locks.stderr:
        sys.stderr.write(msg)
        sys.stderr.flush()


def log_stdout(msg):
    with Locks.stdout:
        sys.stdout.write(msg)
        sys.stdout.flush()
