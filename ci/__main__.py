#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import click
import subprocess

DEFAULT_PYTHON_VERSION = "3.6"
PYTHON_VERSIONS = ["3.6"]

ADDITIONAL_CORE_DEPS = [
    'mock>=2.0.0-3',
    'scipy>=1.2.1',
]


@click.group()
def cli():
    pass


python_version_option = click.option(
    '--python-version',
    default=DEFAULT_PYTHON_VERSION,
    type=click.Choice(PYTHON_VERSIONS),
    show_default=True,
    help="Python version for the environment")


@cli.command(name="install", help="Installs the code and its dependencies")
@python_version_option
def install(python_version):
    env_name = get_env_name(python_version)
    returncode = subprocess.call([
        "edm", "install", "-e", env_name,
        "--yes"] + ADDITIONAL_CORE_DEPS)

    if returncode:
        raise click.ClickException("Error while installing EDM dependencies.")

    returncode = edm_run(env_name, ["pip", "install", "-e", "."])
    if returncode:
        raise click.ClickException("Error while installing the local package.")


@cli.command(help="Run the tests")
@python_version_option
@click.option(
    "--verbose/--quiet",
    default=True,
    help="Run tests in verbose mode? [default: --verbose]",
)
def test(python_version, verbose):
    env_name = get_env_name(python_version)

    verbosity_args = ["--verbose"] if verbose else []

    returncode = edm_run(
        env_name, ["python", "-m", "unittest", "discover"] + verbosity_args
    )

    if returncode:
        raise click.ClickException("There were test failures.")


@cli.command(help="Run flake")
@python_version_option
def flake8(python_version):
    env_name = get_env_name(python_version)

    returncode = edm_run(env_name, ["flake8", "."])
    if returncode:
        raise click.ClickException(
            "Flake8 exited with exit status {}".format(returncode)
        )


@cli.command(help="Runs the coverage")
@python_version_option
def coverage(python_version):
    env_name = get_env_name(python_version)

    returncode = edm_run(
        env_name, ["coverage", "run", "-m", "unittest", "discover"]
    )
    if returncode:
        raise click.ClickException("There were test failures.")

    returncode = edm_run(env_name, ["pip", "install", "codecov"])
    if not returncode:
        returncode = edm_run(env_name, ["codecov"])

    if returncode:
        raise click.ClickException(
            "There were errors while installing and running codecov."
        )


@cli.command(help="Builds the documentation")
@python_version_option
def docs(python_version):
    env_name = get_env_name(python_version)

    returncode = edm_run(env_name, ["make", "html"], cwd="doc")
    if returncode:
        raise click.ClickException(
            "There were errors while building the documentation."
        )


def get_env_name(python_version):
    return "force-py{}".format(remove_dot(python_version))


def remove_dot(python_version):
    return "".join(python_version.split('.'))


def edm_run(env_name, cmd, cwd=None):
    return subprocess.call(["edm", "run", "-e", env_name, "--"] + cmd, cwd=cwd)


if __name__ == "__main__":
    cli()
