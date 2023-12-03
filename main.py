import sys
import json

import attrs
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
