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
    help="Obris application id.",
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
    application_client.delete(pk=id)


@application.command()
@click.option(
    '--id', required=True,
    help="Obris application id.",
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


# ------------------------------------------------------------------------------
# Repository Commands
# ------------------------------------------------------------------------------
@cli.group()
@click.pass_context
def repo(ctx):
    ctx.obj = ctx.obj.create_client(CommandOption.REPO)


@repo.command()
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def list(repo_client, application_id):
    repos = repo_client.list(application_id=application_id)
    logger.log_json({"repos": repos})


@repo.command()
@click.option(
    '--credential-id', '-c',
    help="GitHub credential id. run: `obris credential github list` to view options.",
)
@click.option(
    '--name', '-n', required=True,
    help="Internal Obris used name of the github repo.",
)
@click.option(
    '--url', '-u', required=True,
    help="HTTPS url for github repo.",
)
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def create(repo_client, application_id, url, name, credential_id):
    repo = repo_client.create(
        application_id=application_id, url=url, name=name, credential_id=credential_id
    )
    logger.log_json({"repo": repo})


@repo.command()
@click.option(
    '--credential-id', '-c',
    help="GitHub credential id. run: `obris credential github list` to view options.",
)
@click.option(
    '--name', '-n',
    help="Internal Obris used name of the github repo.",
)
@click.option(
    '--url', '-u',
    help="HTTPS url for github repo.",
)
@click.option(
    '--id', required=True,
    help="Id of Obris repo.",
)
@click.pass_obj
def update(repo_client, id, url, name, credential_id):
    repo = repo_client.update(
        pk=id, url=url, name=name, credential_id=credential_id
    )
    logger.log_json({"repo": repo})


@repo.command()
@click.option(
    '--id', required=True,
    help="Obris repo id.",
)
@click.pass_obj
def delete(repo_client, id):
    repo_client.delete(
        pk=id
    )


@repo.command()
@click.option(
    '--id', required=True,
    help="GitHub credential id.",
)
@click.pass_obj
def clear_credential(github_creds_client, id):
    repo = github_creds_client.clear_credential(
        pk=id
    )
    logger.log_json({"repo": repo})


# ------------------------------------------------------------------------------
# Credentials Command Group
# ------------------------------------------------------------------------------
@cli.group()
@click.pass_context
def credential(ctx):
    pass


# ------------------------------------------------------------------------------
# GitHub Credential Commands
# ------------------------------------------------------------------------------
@credential.group()
@click.pass_context
def github(ctx):
    ctx.obj = ctx.obj.create_client(CommandOption.CREDENTIAL_GITHUB)


@github.command()
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def list(github_creds_client, application_id):
    credentials = github_creds_client.list(
        application_id=application_id
    )
    convert_list = None
    if credentials is not None:
        convert_list = [credentials]
    logger.log_json({"credentials": convert_list})


@github.command()
@click.option(
    '--token', '-t', prompt=True, hide_input=True,
    help="GitHub personal access token (classic) with repo and workflow permissions.",
)
@click.option(
    '--username', '-u', required=True,
    help="GitHub username associated with the credentials.",
)
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def create(github_creds_client, application_id, username, token):
    _credential = github_creds_client.create(
        application_id=application_id, username=username, token=token
    )
    logger.log_json({"credential": _credential})


@github.command()
@click.option(
    '--token', '-t', is_flag=True,
    help="Update GitHub personal access token (classic) with repo and workflow permissions.",
)
@click.option(
    '--username', '-u',
    help="GitHub username associated with the credentials.",
)
@click.option(
    '--id', required=True,
    help="GitHub credential id.",
)
@click.pass_obj
def update(github_creds_client, id, username, token):
    user_token = None
    if token:
        user_token = click.prompt('Enter new GitHub personal access token (classic)', type=str)

    _credential = github_creds_client.update(
        pk=id, username=username, token=user_token
    )
    logger.log_json({"credential": _credential})


@github.command()
@click.option(
    '--id', required=True,
    help="GitHub credential id.",
)
@click.pass_obj
def delete(github_creds_client, id):
    github_creds_client.delete(
        pk=id
    )


# ------------------------------------------------------------------------------
# Processes Command Group
# ------------------------------------------------------------------------------
@cli.group()
@click.pass_context
def process(ctx):
    ctx.obj = ctx.obj.create_client(CommandOption.PROCESS)


@process.command()
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def list(process_client, application_id):
    processes = process_client.list(
        application_id=application_id
    )
    logger.log_json({"processes": processes})


@process.command()
@click.option(
    '--route-match', '-m',
    help="If serving web traffic, comma seperated list of patterns that route traffic to the deployed server"
         " (ex. \"*, /v1/*, /backend/*\").",
)
@click.option(
    '--local-port', '-p',
    help="If serving web traffic, the local port the deployed server runs on.",
)
@click.option(
    '--procfile-path', '-s', required=True,
    help="The path to the Procfile in the associated repo.",
)
@click.option(
    '--requirements-path', '-d', required=True,
    help="The path to the file containing the process' dependencies in the associated repo.",
)
@click.option(
    '--runtime', '-t', required=True,
    help="The runtime id for your process.",
)
@click.option(
    '--repository-id', '-r', required=True,
    help="Obris repository id to associate with the process.",
)
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id to associate with the process.",
)
@click.pass_obj
def create(
        process_client,
        application_id,
        repository_id,
        runtime,
        requirements_path,
        procfile_path,
        local_port,
        route_match
):
    _process = process_client.create(
        application_id=application_id,
        repository_id=repository_id,
        runtime=runtime,
        requirements_path=requirements_path,
        procfile_path=procfile_path,
        local_port=local_port,
        route_match=route_match
    )
    logger.log_json({"process": _process})


@process.command()
@click.option(
    '--route-match', '-m',
    help="If serving web traffic, comma seperated list of patterns that route traffic to the deployed server"
         " (ex. \"*, /v1/*, /backend/*\").",
)
@click.option(
    '--local-port', '-p',
    help="If serving web traffic, the local port the deployed server runs on.",
)
@click.option(
    '--procfile-path', '-s',
    help="The path to the Procfile in the associated repo.",
)
@click.option(
    '--requirements-path', '-d',
    help="The path to the file containing the process' dependencies in the associated repo.",
)
@click.option(
    '--runtime', '-t',
    help="The runtime id for your process.",
)
@click.option(
    '--repository-id', '-r',
    help="Obris repository id to associate with the process.",
)
@click.option(
    '--id', required=True,
    help="Obris process id.",
)
@click.pass_obj
def update(
        process_client,
        id,
        repository_id,
        runtime,
        requirements_path,
        procfile_path,
        local_port,
        route_match
):
    _process = process_client.update(
        pk=id,
        repository_id=repository_id,
        runtime=runtime,
        requirements_path=requirements_path,
        procfile_path=procfile_path,
        local_port=local_port,
        route_match=route_match
    )
    logger.log_json({"process": _process})


@process.command()
@click.option(
    '--id', required=True,
    help="Obris process id.",
)
@click.pass_obj
def clear_route_config(
        process_client,
        id
):
    _process = process_client.clear_route_config(
        pk=id,
    )
    logger.log_json({"process": _process})

@process.command()
@click.option(
    '--id', required=True,
    help="Obris process id.",
)
@click.pass_obj
def delete(
        process_client,
        id
):
    _process = process_client.delete(
        pk=id
    )


@process.command()
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def runtime_types(process_client, application_id):
    _runtime_types = process_client.runtime_types(
        application_id=application_id
    )
    logger.log_json({"runtime_types": _runtime_types})


@process.command()
@click.option(
    '--runtime-type', '-t', required=True,
    help="The type of runtimes to list.",
)
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def runtimes(process_client, application_id, runtime_type):
    processes = process_client.runtimes(
        application_id=application_id,
        runtime_type=runtime_type
    )
    logger.log_json({"processes": processes})

# ------------------------------------------------------------------------------
# Webserver Command Group
# ------------------------------------------------------------------------------
@cli.group()
@click.pass_context
def webserver(ctx):
    ctx.obj = ctx.obj.create_client(CommandOption.WEBSERVER)


@webserver.command()
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def list(webserver_client, application_id):
    webservers = webserver_client.list(
        application_id=application_id
    )
    logger.log_json({"webservers": webservers})


@webserver.command()
@click.option(
    '--post-process-init', '-c',
    help="Executable pre cloud init script string."
)
@click.option(
    '--pre-process-init', '-c',
    help="Executable pre cloud init script string."
)
@click.option(
    '--pre-cloud-init', '-c',
    help="Executable pre cloud init script string.",
)
@click.option(
    '--domain', '-d',
    help="Owned domain name (ex. example.com) to associated with the webserver.",
)
@click.option(
    '--availability-zones', '-z',
    multiple=True, required=True,
    help="AZs for instance.",
)
@click.option(
    '--runtime', '-r', required=True,
    help="Webserver runtime.",
)
@click.option(
    '--keypair', '-k', required=True,
    help="Keypair name.",
)
@click.option(
    '--instance-type', '-i', required=True,
    help="Cluster instance type.",
)
@click.option(
    '--process-ids', '-p', multiple=True, required=True,
    help="Obris process ids.",
)
@click.option(
    '--name', '-n', required=True,
    help="Webserver name.",
)
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def create(
        webserver_client,
        application_id,
        name,
        process_ids,
        instance_type,
        keypair,
        runtime,
        availability_zones,
        domain,
        pre_cloud_init,
        pre_process_init,
        post_process_init
):
    webserver = webserver_client.create(
        application_id=application_id,
        name=name,
        process_ids=process_ids,
        instance_type=instance_type,
        keypair=keypair,
        runtime=runtime,
        availability_zones=availability_zones,
        domain=domain,
        pre_cloud_init_script=pre_cloud_init,
        pre_process_init_script=pre_process_init,
        post_process_init_script=post_process_init
    )
    logger.log_json({"webserver": webserver})


@webserver.command()
@click.option(
    '--id', required=True,
    help="Obris compute id.",
)
@click.pass_obj
def delete(webserver_client, id):
     webserver_client.delete(
        pk=id
    )


if __name__ == "__main__":
    cli()
