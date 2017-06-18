#!/usr/bin/env python3
import json
import select
import subprocess
import sys
import time
import traceback
from multiprocessing import Process

import click

from helpers import SlackStore
from helpers import WorkerStore
from helpers import journalctl_helper
from helpers import slack_helper
from helpers import utils


def poll_journal(config, verbose):
    print("Started journalctl worker.")

    slack_store = SlackStore(config)
    worker_store = WorkerStore(config)
    slack_store.verbose = verbose
    worker_store.verbose = verbose

    args = ['journalctl', '--follow', '--lines', '0', '-o', 'json']
    print("$    journalctl --follow --lines 0 -o json")

    f = subprocess.Popen(args, stdout=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)
    while True:
        try:
            if p.poll(100):
                line = f.stdout.readline()
                if not line:
                    break
                if isinstance(line, bytes):
                    line = line.decode('utf-8')
                journal_json = json.loads('[' + line.strip() + ']')
                j = journalctl_helper.parse_journal_json(worker_store, journal_json)
                if j:
                    journalctl_helper.process_jentry(slack_store, worker_store, j)
                j = None
        except Exception as e:
            ex = "Exception @poll_journal: %s" % e
            print(e)
            traceback.print_exc(file=sys.stdout)
            slack_helper.slack_send_msg_channel(slack_store, ex)
            time.sleep(worker_store.seconds_sleep_on_error)


@click.command()
@click.option('-d', '--debug', is_flag=True, default=False)
@click.option('-v', '--verbose', is_flag=True, default=False)
def main(debug, verbose):
    click.echo('Debug: %s' % debug)
    click.echo('Verbosity: %s' % verbose)

    config = utils.get_config(debug=debug)

    print('Starting journalctl worker.')
    prc = Process(name="poll_journal",
                  target=poll_journal,
                  args=(config, verbose))

    prc.start()
    prc.join()
    print("Proc={p} ExitCode={e}".format(p=prc.name, e=prc.exitcode))


if __name__ == '__main__':
    main()
