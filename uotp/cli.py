import click
import yaml
from pathlib import Path

from .packet import IssueRequest, TimeRequest
from . import OTPTokenGenerator
from . import OTPUtil


config = {}
fp = None


def save_config():
    fp.seek(0)
    yaml.dump(config, fp, default_flow_style=False)


@click.group()
@click.option('--conf', default='~/.config/uotp/config.yml', envvar='UOTP_CONF', help='Path to the configuration file.')
def cli(conf):
    global config, fp

    path = Path(conf).expanduser()
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
        click.echo(f'A new configuration file has been created on `{path}`.')
        click.echo()


@cli.command()
@click.pass_context
def new(ctx):
    if config['account']:
        click.confirm('Account already exists. Do you want to replace it?', abort=True)

    ctx.invoke(sync)

    req = IssueRequest()
    req['mno'] = 'KTF'
    req['hw_id'] = 'GA15'
    req['hw_model'] = 'SM-N900P'
    req['version'] = (2, 0)

    resp = req()
    config['account'] = resp.params
    save_config()

    serial_number = OTPUtil.humanize(resp['serial_number'], char='-', each=4)

    click.echo('A new account has been issued successfully.')
    click.echo()
    click.echo(f'Serial Number: {serial_number}')


@cli.command()
def sync():
    time = TimeRequest()()['time']
    timediff = time - OTPUtil.now()

    config['timediff'] = timediff
    save_config()

    click.echo(f'Time synchronized with the remote server (offset: {timediff}sec).')


@cli.command()
def get():
    if not config['account']:
        click.echo('Please issue a new account first. You can do this with `uotp new`')
        return

    generator = OTPTokenGenerator(config['account']['oid'], config['account']['seed'])
    generator.compensate_time_deviation(config['timediff'])
    token = generator.generate_token()

    token = OTPUtil.humanize(token, char=' ', each=3, maxgroup=2)
    click.echo(f'OTP Token: {token}')


if __name__ == '__main__':
    cli()
