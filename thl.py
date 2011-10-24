#!/usr/bin/env python

import sys
from optparse import OptionParser
from clint.textui import puts, colored
import TheHitList

USAGE = '''usage: %prog [options] <command>
commands
list            List tasks
add <string>    Add new task
'''


class THLParser(OptionParser):
    def __init__(self):
        OptionParser.__init__(self, usage=USAGE)
        self.add_option("--list", dest="list",
            default='inbox', help="Use a specific list")

    def parse_args(self):
        opts, args = OptionParser.parse_args(self)
        if len(args) == 0:
            args = ['list']

        command = args.pop(0).lower()
        if command not in ['add', 'list']:
            parser.error('Invalid command')

        return command, opts, args


def show_tasks(thl, opts, args):
    if len(args) == 0:
        list = 'today'
    else:
        list = args.pop(0)
    puts(colored.yellow('Showing tasks in %s' % unicode(list, 'utf8', 'replace')))
    for task in thl.find_list(list).tasks():
        print task.title


def add_task(thl, opts, args):
    puts(colored.yellow('Adding task to %s' % opts.list))
    list = thl.find_list(opts.list)
    task = TheHitList.Task()
    task.title = ' '.join(args)
    list.add_task(task)


def main():
    command, opts, args = THLParser().parse_args()

    thl = TheHitList.Application()

    if command == 'list':
        show_tasks(thl, opts, args)
    if command == 'add':
        add_task(thl, opts, args)

if __name__ == '__main__':
    main()
