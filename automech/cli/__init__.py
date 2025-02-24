import click

from . import _check_log, _run, _subtasks_run_adhoc, _subtasks_setup
from ._subtasks_setup import SUBTASK_DIR


@click.group()
def main():
    """AutoMech CLI"""
    pass


@main.command()
@click.option(
    "-p", "--path", default=".", show_default=True, help="The job run directory"
)
@click.option("-S", "--safemode-off", is_flag=True, help="Turn off safemode?")
def run(path: str = ".", safemode_off: bool = False):
    """Run central workflow
    Central Execution script to launch a MechDriver process which will
    parse all of the user-supplied input files in a specified directory, then
    launches all of the requested electronic structure, transport,
    thermochemistry and kinetics calculations via their associated
    sub-drivers.

    The AutoMech directory must contain an `inp/` subdirectory with the following
    required files: run.dat, theory.dat, models.dat, species.csv, mechanism.dat
    """
    _run.main(path=path, safemode_off=safemode_off)


@main.command()
@click.option(
    "-p", "--path", default=".", show_default=True, help="The path to the log file"
)
def check_log(path: str = "."):
    """Check an AutoMech log file to see if it succeeded

    The path must point either directly to the log file, or to a directory where the log
    file is named "out.log"
    """
    _check_log.main(path=path)


@main.group()
def subtasks():
    """Run AutoMech subtasks in parallel"""
    pass


@subtasks.command()
@click.option(
    "-p", "--path", default=".", show_default=True, help="The job run directory"
)
@click.option(
    "-o",
    "--out-path",
    default=SUBTASK_DIR,
    show_default=True,
    help="The output path of the subtask directories",
)
@click.option(
    "-s",
    "--save-path",
    default=None,
    show_default=True,
    help="The save filesystem prefix",
)
@click.option(
    "-r",
    "--run-path",
    default=None,
    show_default=True,
    help="The run filesystem prefix",
)
def setup(
    path: str = ".",
    out_path: str = SUBTASK_DIR,
    save_path: str | None = None,
    run_path: str | None = None,
):
    """Set-up subtasks from a user-supplied AutoMech directory

    The AutoMech directory must contain an `inp/` subdirectory with the following
    required files: run.dat, theory.dat, models.dat, species.csv, mechanism.dat
    """
    _subtasks_setup.main(
        path=path, out_path=out_path, save_path=save_path, run_path=run_path
    )


@subtasks.command()
@click.option(
    "-p", "--path", default=SUBTASK_DIR, show_default=True, help="The job run directory"
)
@click.option(
    "-n", "--nodes", default=None, show_default=True, help="A comma-separated list of nodes"
)
@click.option(
    "-a",
    "--activation-hook",
    default=None,
    show_default=True,
    help="An activation hook, to be called using `eval`",
)
def run_adhoc(path: str = SUBTASK_DIR, nodes: str | None=None , activation_hook: str | None = None):
    """Run subtasks in parallel on an Ad Hoc SSH Cluster"""
    _subtasks_run_adhoc.main(path=path, nodes=nodes, activation_hook=activation_hook)
