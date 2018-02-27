"""Trace treadmill application events.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import json
import zlib

import click

from treadmill import context
from treadmill import zknamespace as z
from treadmill import cli

_LOGGER = logging.getLogger(__name__)


def init():
    """Return top level command handler"""

    @click.group()
    @click.option('--cell', required=True,
                  envvar='TREADMILL_CELL',
                  callback=cli.handle_context_opt,
                  expose_value=False)
    @click.option('--zookeeper', required=False,
                  envvar='TREADMILL_ZOOKEEPER',
                  callback=cli.handle_context_opt,
                  expose_value=False)
    def top():
        """Show Treadmill apps"""
        pass

    @top.command()
    def scheduled():
        """List scheduled applications"""
        for app in sorted(context.GLOBAL.zk.conn.get_children(z.SCHEDULED)):
            cli.out(app)

    @top.command()
    def running():
        """List running applications"""
        for app in sorted(context.GLOBAL.zk.conn.get_children(z.RUNNING)):
            cli.out(app)

    @top.command()
    def pending():
        """List pending applications"""
        zkclient = context.GLOBAL.zk.conn

        data, _ = zkclient.get(z.PLACEMENT)
        if data:
            placement = json.loads(
                zlib.decompress(data).decode()
            )
        else:
            placement = []

        # App is pending if it's scheduled but has no placement.
        placed = {
            app for app, _before, _exp_before, after, _exp_after in placement
            if after
        }
        scheduled = set(zkclient.get_children(z.SCHEDULED))
        for app in sorted(scheduled - placed):
            cli.out(app)

    @top.command()
    def stopped():
        """List stopped applications"""
        running = set(context.GLOBAL.zk.conn.get_children(z.RUNNING))
        scheduled = set(context.GLOBAL.zk.conn.get_children(z.SCHEDULED))
        for app in sorted(running - scheduled):
            cli.out(app)

    del stopped
    del pending
    del running
    del scheduled

    return top