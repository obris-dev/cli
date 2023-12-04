#!/usr/bin/env python

import click

from obriscli import ClientFactory, CommandOption, Logger

logger = Logger()


@click.group()
@click.option(
    '--token',
    envvar='OBRIS_TOKEN',
    required=True,
    help="Obris API token. Generate one within the Obris UI (http://obris.io)",
)
@click.option(
    '--base-url',
    envvar='OBRIS_BASE_URL',
    default="https://obris.io",
    help="Base URL for Obris API requests.",
)
@click.pass_context
def cli(ctx, token, base_url):
    ctx.obj = ClientFactory(token, base_url)


# ------------------------------------------------------------------------------
# Application Commands
# ------------------------------------------------------------------------------
@cli.group()
@click.pass_context
def application(ctx):
    ctx.obj = ctx.obj.create_client(CommandOption.APPLICATION)


@application.command()
@click.pass_obj
def list(application_client):
    applications = application_client.list()
    logger.log_json({"applications": applications})


@application.command()
@click.option(
    '--description', "-d", default="",
    help="A helpful description outlining the your application's purpose.",
)
@click.option(
    '--region', "-r", required=True,
    help="The region that hosts your application.",
)
@click.option(
    '--name', "-n", required=True,
    help="Name of your application.",
)
@click.pass_obj
def create(application_client, name, region, description):
    _application = application_client.create(name=name, region=region, description=description)
    logger.log_json({"application": _application})


@application.command()
@click.option(
    '--description', "-d",
    help="An optional description of the application.",
)
@click.option(
    '--name', "-n",
    help="Name of your application.",
)
@click.option(
    '--id', required=True,
    help="The Obris application id.",
)
@click.pass_obj
def update(application_client, id, name, description):
    _application = application_client.update(pk=id, name=name, description=description)
    logger.log_json({"application": _application})


@application.command()
@click.option(
    '--id', required=True,
    help="The ID of the application you want to delete.",
)
@click.pass_obj
def delete(application_client, id):
    application_client.delete(id=id)


# ------------------------------------------------------------------------------
# Repository Commands
# ------------------------------------------------------------------------------
@cli.group()
@click.pass_context
def repo(ctx):
    ctx.obj = ctx.obj.create_client(CommandOption.REPO)


@repo.command()
@click.pass_obj
def list(repo_client):
    repos = repo_client.list()
    logger.log_json({"repos": repos})


if __name__ == "__main__":
    cli()
