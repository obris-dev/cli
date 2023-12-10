#!/usr/bin/env python

import click


from obriscli import (
    CommandOption,
    ClientFactory,
    Logger
)
from .execeptions import (
    ApplicationAlreadyLinkedError,
    ProviderNotReleasedError
)

logger = Logger()


@click.group()
@click.version_option(package_name="obris")
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
    help="A helpful description outlining your application's purpose.",
)
@click.option(
    '--region',
    "-r",
    required=True,
    help="The cloud provider specific region that hosts your application.",
)
@click.option(
    '--provider',
    "-p",
    type=click.Choice(['aws', 'azure', 'gcp']),
    required=True,
    help="The cloud provider that hosts your application.",
)
@click.option(
    '--name', "-n", required=True,
    help="Name of your application.",
)
@click.pass_obj
def create(application_client, name, provider, region, description):
    _application = application_client.create(
        name=name,
        provider=provider,
        region=region,
        description=description
    )
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

    try:
        application_client.start_link(pk=target_id)
    except ApplicationAlreadyLinkedError:
        exit(0)
    except ProviderNotReleasedError as ex:
        logger.log(f"Oops, you found us before we're ready! We're hard at work finishing \n"
                   f"our integration with {ex.unimplemented_human_provider}! In the meantime, please feel free \n"
                   f"to configure an AWS application.\n\n")
        if click.confirm(
                f"Would you like to be informed when we release our "
                f"{ex.unimplemented_human_provider} link?"
        ):
            application_client.notify_on_link_release(provider=ex.unimplemented_provider)
            logger.log("We'll reach out as soon as we've completed the finishing touches!\n")
        else:
            logger.log("No problem! We won't send a notification. Please check back soon!\n")
        exit(0)

    link_success = application_client.poll_link(pk=target_id)
    if not link_success:
        exit(1)


@application.command()
@click.option(
    '--provider',
    "-p",
    type=click.Choice(['aws', 'azure', 'gcp']),
    required=True,
    help="The cloud provider that hosts your application.",
)
@click.pass_obj
def regions(application_client, provider):
    _regions = application_client.regions(provider)
    logger.log_json({"regions": _regions})


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
    '--post-build-script', '-l',
    help="Executable post build script script string."
)
@click.option(
    '--build-script', '-b',
    help="Executable pre cloud init script string."
)
@click.option(
    '--pre-cloud-init-script', '-f',
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
        pre_cloud_init_script,
        build_script,
        post_build_script
):
    _webserver = webserver_client.create(
        application_id=application_id,
        name=name,
        process_ids=process_ids,
        instance_type=instance_type,
        keypair=keypair,
        runtime=runtime,
        availability_zones=availability_zones,
        domain=domain,
        pre_cloud_init_script=pre_cloud_init_script,
        pre_process_init_script=build_script,
        post_cloud_init_script=post_build_script
    )
    logger.log_json({"webserver": _webserver})


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
    '--post-build-script', '-l',
    help="Executable post build script script string."
)
@click.option(
    '--build-script', '-b',
    help="Executable build script string."
)
@click.option(
    '--pre-cloud-init-script', '-f',
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
    '--runtime', '-r',
    help="Webserver runtime.",
)
@click.option(
    '--keypair', '-k',
    help="Keypair name.",
)
@click.option(
    '--instance-type', '-i',
    help="Cluster instance type.",
)
@click.option(
    '--process-ids', '-p', multiple=True,
    help="Obris process ids.",
)
@click.option(
    '--name', '-n',
    help="Webserver name.",
)
@click.option(
    '--id',
    help="Obris comput id.",
)
@click.pass_obj
def update(
        webserver_client,
        id,
        name,
        process_ids,
        instance_type,
        keypair,
        runtime,
        availability_zones,
        domain,
        pre_cloud_init_script,
        build_script,
        post_build_script
):
    _webserver = webserver_client.update(
        pk=id,
        name=name,
        process_ids=process_ids,
        instance_type=instance_type,
        keypair=keypair,
        runtime=runtime,
        availability_zones=availability_zones,
        domain=domain,
        pre_cloud_init_script=pre_cloud_init_script,
        pre_process_init_script=build_script,
        post_cloud_init_script=post_build_script
    )
    logger.log_json({"webserver": _webserver})


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


@webserver.command()
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def runtimes(webserver_client, application_id):
    _runtimes = webserver_client.runtimes(
        application_id=application_id
    )
    logger.log_json({"runtimes": _runtimes})


@webserver.command()
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def availability_zones(webserver_client, application_id):
    _availability_zones = webserver_client.availability_zones(
        application_id=application_id
    )
    logger.log_json({"availability_zones": _availability_zones})


@webserver.command()
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def key_pairs(webserver_client, application_id):
    _key_pairs = webserver_client.key_pairs(
        application_id=application_id
    )
    logger.log_json({"key_pairs": _key_pairs})


@webserver.command()
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def instance_types(webserver_client, application_id):
    _instance_types = webserver_client.instance_types(
        application_id=application_id
    )
    logger.log_json({"instance_types": _instance_types})


# ------------------------------------------------------------------------------
# Env var Command Group
# ------------------------------------------------------------------------------
@cli.group()
@click.pass_context
def env_var(ctx):
    ctx.obj = ctx.obj.create_client(CommandOption.ENV_VAR)


@env_var.command("list")
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def list_(env_var_client, application_id):
    env_vars = env_var_client.list(
        application_id=application_id
    )
    logger.log_json({"env_vars": env_vars})


@env_var.command()
@click.option(
    '--value', '-v', required=True,
    help="Environment variable value.",
)
@click.option(
    '--key', '-k', required=True,
    help="Environment variable key.",
)

@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def create(env_var_client, application_id, key, value):
    _env_var = env_var_client.create(
        application_id=application_id,
        key=key,
        value=value
    )
    logger.log_json({"env_var": _env_var})


@env_var.command()
@click.option(
    '--value', '-v',
    help="Environment variable value.",
)
@click.option(
    '--key', '-k',
    help="Environment variable key.",
)
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.option(
    '--id', required=True,
    help="Obris environment variable id.",
)
@click.pass_obj
def update(env_var_client, id, application_id, key, value):
    _env_var = env_var_client.update(
        pk=id,
        application_id=application_id,
        key=key,
        value=value
    )
    logger.log_json({"env_var": _env_var})


@env_var.command()
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.option(
    '--id', required=True,
    help="Obris environment variable id.",
)
@click.pass_obj
def delete(env_var_client, id, application_id):
    env_var_client.delete(
        pk=id,
        application_id=application_id
    )


# ------------------------------------------------------------------------------
# SSL/TLS Certificate Command Group
# ------------------------------------------------------------------------------
@cli.group()
@click.pass_context
def certificate(ctx):
    ctx.obj = ctx.obj.create_client(CommandOption.CERTIFICATE)


@certificate.command("list")
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def list_(certificate_client, application_id):
    certificates = certificate_client.list(
        application_id=application_id
    )
    logger.log_json({"certificates": certificates})


@certificate.command("import")
@click.option(
    '--cert-chain-path', '-c',
    help="Local path to chain.pem file.",
)
@click.option(
    '--cert-private-key-path', '-p', required=True,
    help="Local path to privkey.pem file.",
)
@click.option(
    '--cert-body-path', '-b', required=True,
    help="Local path to cert.pem file.",
)
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def import_(
        certificate_client,
        application_id,
        cert_body_path,
        cert_private_key_path,
        cert_chain_path
):
    _certificate = certificate_client.create(
        application_id=application_id,
        cert_body_file_path=cert_body_path,
        cert_private_key_file_path=cert_private_key_path,
        cert_chain_file_path=cert_chain_path
    )
    logger.log_json({"certificate": _certificate})


@certificate.command()
@click.option(
    '--cert-chain-path', '-c',
    help="Local path to chain.pem file.",
)
@click.option(
    '--cert-private-key-path', '-p', required=True,
    help="Local path to privkey.pem file.",
)
@click.option(
    '--cert-body-path', '-b', required=True,
    help="Local path to cert.pem file.",
)
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.option(
    '--id',  required=True,
    help="Obris SSL/TLS certificate id.",
)
@click.pass_obj
def reimport(
        certificate_client,
        id,
        application_id,
        cert_body_path,
        cert_private_key_path,
        cert_chain_path
):
    _certificate = certificate_client.update(
        pk=id,
        application_id=application_id,
        cert_body_file_path=cert_body_path,
        cert_private_key_file_path=cert_private_key_path,
        cert_chain_file_path=cert_chain_path
    )
    logger.log_json({"certificate": _certificate})


@certificate.command()
@click.option(
    '--id', required=True,
    help="Obris SSL/TLS certificate id.",
)
@click.option(
    '--application-id', '-a', required=True,
    help="Obris application id.",
)
@click.pass_obj
def delete(
        certificate_client,
        application_id,
        id
):
    _certificate = certificate_client.delete(
        application_id=application_id,
        pk=id,
    )


if __name__ == "__main__":
    cli()
