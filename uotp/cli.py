import click
import yaml
from pathlib import Path
from base64 import b64encode

from . import UOTP
from .packet import TimeRequest
from .util import OTPUtil


config = {}
fp = None


def save_config():
    fp.seek(0)
    yaml.dump(config, fp, default_flow_style=False)


@click.group(invoke_without_command=True)
@click.option('--conf', default='~/.config/uotp/config.yml', envvar='UOTP_CONF', help='Path to the configuration file.')
@click.pass_context
def cli(ctx, conf):
    global config, fp

    path = Path(conf).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        fp = click.open_file(str(path), 'r+', encoding='utf-8')
        config = yaml.load(fp)
    else:
        fp = click.open_file(str(path), 'w', encoding='utf-8')
        config = {
            'account': None,
            'timediff': 0,
        }
        save_config()
        click.echo('A new configuration file has been created on `{}`.'.format(path))
        click.echo()

    if ctx.invoked_subcommand is None:
        ctx.invoke(get)


@cli.command()
@click.pass_context
def new(ctx):
    if config['account']:
        click.confirm('Account already exists. Do you want to replace it?', abort=True)

    ctx.invoke(sync)

    uotp = UOTP()
    uotp.issue_account()

    config['account'] = {
        'oid': uotp.account_oid,
        'seed': uotp.account_seed,
        'serial_number': uotp.account_serial_number,
        'user_hash': uotp.account_id.encode(),
    }
    save_config()

    click.echo('A new account has been issued.')
    click.echo('Please keep your configuration file safe as it is not possible to recover the account if it gets lost.')
    click.echo()
    click.echo('Serial Number: {}'.format(uotp.account_serial_number))


@cli.command()
def sync():
    time = TimeRequest()()['time']
    timediff = time - OTPUtil.now()

    config['timediff'] = timediff
    save_config()

    click.echo('Time synchronized with the remote server (offset: {}sec).'.format(timediff))


@cli.command()
@click.option('-s', '--autosync', is_flag=True, help='Automatically synchronize time before generating OTP token')
@click.pass_context
def get(ctx, autosync):
    if not config['account']:
        if click.confirm('Account not exists. Do you want to issue one now?', default=True):
            ctx.invoke(new)
        else:
            click.echo('Please issue a new account first. You can do this with `uotp new`.')
        return

    if autosync:
        ctx.invoke(sync)

    uotp = UOTP(
        config['account']['user_hash'].decode(),
        config['account']['oid'],
        config['account']['seed'],
        config['account']['serial_number']
    )
    uotp.sync_time(config['timediff'])
    token = uotp.generate_token()

    token = OTPUtil.humanize(token, char=' ', each=3, maxgroup=2)
    click.echo('OTP Token: {}'.format(token))


@cli.command()
def info():
    if not config['account']:
        click.echo('Please issue a new account first. You can do this with `uotp new`.')
        return

    click.echo('S/N: {}'.format(config['account']['serial_number']))
    click.echo('Time offset: {}sec'.format(config['timediff']))
    click.echo('Oid: {}'.format(config['account']['oid']))
    click.echo('Seed: {}'.format(b64encode(config['account']['seed']).decode()))


@cli.command()
def gui():
    import wx
    from .gui import MainWindow
    app = wx.App()
    MainWindow()
    app.MainLoop()


if __name__ == '__main__':
    cli()
