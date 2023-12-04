#!/usr/bin/env python

import click

from time import sleep
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
    ctx.obj = ctx.obj.create_client(CommandOption.CLOUD_APPLICATION)


@application.command()
@click.option(
    '--has-credentials', "-c", type=bool, default=None,
    help="Filter application list to those linked or not to cloud provider.",
)
@click.pass_obj
def list(application_client, has_credentials):
    applications = application_client.list(has_credentials=has_credentials)
    logger.log_json({"applications": applications})


@application.command()
@click.option(
    '--description', "-d", default="",
    help="A helpful description outlining the your application's purpose.",
)
@click.option(
    '--region',
    "-r",
    type=click.Choice(['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']),
    required=True,
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
    help="Obris application id with has_credentials=False.",
)
@click.pass_obj
def link(application_client, id):
    target_id = id

    target_application = application_client.get_one(pk=target_id)
    if target_application.has_credentials:
        logger.log("Application already linked. Exiting...\n")
        return

    logger.log(f"Linking application id={target_application.id} name={target_application.name}...  "
               f"Redirecting to AWS to complete the process.\n")
    sleep(1)

    application_client.start_link(pk=target_application.id)

    link_success = application_client.poll_link(pk=target_application.id)
    if not link_success:
        exit(1)





@application.command()
@click.option(
    '--id', required=True,
    help="The ID of the application you want to delete.",
)
@click.pass_obj
def delete(application_client, id):
    application_client.delete(pk=id)


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
