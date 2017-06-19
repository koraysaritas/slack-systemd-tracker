#!/usr/bin/env python3
from multiprocessing import Process

import click

from helpers import journalctl_helper
from helpers import utils


@click.command()
@click.option('-d', '--debug', is_flag=True, default=False)
@click.option('-v', '--verbose', is_flag=True, default=False)
def main(debug, verbose):
    click.echo('Debug: %s' % debug)
    click.echo('Verbosity: %s' % verbose)

    config = utils.get_config(debug=debug)

    print('Starting journalctl worker.')
    prc = Process(name="poll_journal",
                  target=journalctl_helper.poll_journal,
                  args=(config, verbose))

    prc.start()
    prc.join()
    print("Proc={p} ExitCode={e}".format(p=prc.name, e=prc.exitcode))


if __name__ == '__main__':
    main()
