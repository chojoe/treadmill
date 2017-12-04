"""Treadmill module.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import logging.config

import click

from treadmill import cli

# Disable click warning for importing unicode_literals in python 2
click.disable_unicode_literals_warning = True


# TODO: add options to configure logging.
@click.group(cls=cli.make_commands('treadmill.cli'))
@click.option('--dns-domain', required=False,
              envvar='TREADMILL_DNS_DOMAIN',
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--dns-server', required=False, envvar='TREADMILL_DNS_SERVER',
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--ldap', required=False, envvar='TREADMILL_LDAP',
              type=cli.LIST,
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--ldap-user', required=False, envvar='TREADMILL_LDAP_USER',
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--ldap-pwd', required=False, envvar='TREADMILL_LDAP_PWD',
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--ldap-suffix', required=False,
              envvar='TREADMILL_LDAP_SUFFIX',
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--profile', required=False,
              envvar='TREADMILL_PROFILE',
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--outfmt', type=click.Choice(['json', 'yaml']))
@click.option('--debug/--no-debug',
              help='Sets logging level to debug',
              is_flag=True, default=False)
@click.pass_context
def run(ctx, outfmt, debug):
    """Treadmill CLI."""
    ctx.obj = {}
    ctx.obj['logging.debug'] = False

    if outfmt:
        cli.OUTPUT_FORMAT = outfmt

    # Default logging to cli.conf, at CRITICAL, unless --debug
    cli.init_logger('cli.conf')
    if debug:
        ctx.obj['logging.debug'] = True
        logging.getLogger('treadmill').setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)


# pylint complains "No value passed for parameter ... in function call".
# This is ok, as these parameters come from click decorators.
if __name__ == '__main__':
    run()  # pylint: disable=no-value-for-parameter
