import subprocess


def apply(task):
    subprocess.run(["/bin/bash", "-c", task.spec["run"]])
