import click
import os
import yaml
from pathlib import Path

from .packet import IssueRequest, TimeRequest
from . import OTPTokenGenerator
from . import Util


config = {}
fp = None


def save_config():
    fp.seek(0)
    yaml.dump(config, fp, default_flow_style=False)


@click.group()
def cli():
    global config, fp

    path = Path(os.environ.get('UOTP_CONF', '~/.config/uotp/config.yml')).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        fp = click.open_file(path, 'r+', encoding='utf-8')
        config = yaml.load(fp)
    else:
        fp = click.open_file(path, 'w', encoding='utf-8')
        config = {
            'account': None,
            'timediff': 0,
        }
        save_config()
        click.echo(f'Created new configuration file into `{path}`.')


@cli.command()
@click.pass_context
def issue(ctx):
    if config['account']:
        click.confirm('An issued account already exists. Do you want to override it?', abort=True)

    ctx.invoke(sync)

    req = IssueRequest()
    req['mno'] = 'KTF'
    req['hw_id'] = 'GA15'
    req['hw_model'] = 'SM-N900P'
    req['version'] = (2, 0)

    resp = req()
    config['account'] = resp.params
    save_config()

    serial_number = Util.humanize(resp['serial_number'], char='-', each=4)

    click.echo('A new account was issued successfully.')
    click.echo(f'Serial number: {serial_number}')


@cli.command()
def sync():
    time = TimeRequest()()['time']
    timediff = time - Util.now()

    config['timediff'] = timediff
    save_config()

    click.echo(f'Synchronized local and remote time (difference: {timediff}sec).')


@cli.command()
def get():
    if not config['account']:
        click.echo('Please issue a new account first.')
        return

    generator = OTPTokenGenerator(config['account']['oid'], config['account']['seed'])
    generator.compensate_time_deviation(config['timediff'])
    token = generator.generate_token()

    token = Util.humanize(token, char=' ', each=3, maxgroup=2)
    click.echo(f'OTP Token: {token}')


if __name__ == '__main__':
    cli()
