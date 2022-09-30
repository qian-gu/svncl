#!/usr/bin/env python
import sys
import os
import argparse
import logging
import xml.etree.ElementTree as ET
from subprocess import CalledProcessError, check_output
import datetime


__AUTHOR__ = "Qian Gu"
__version__ = "0.1.0"


header = '# Changelog\n\n'
header += 'All noteable changes to this project whill be documented in this file. '
header += 'See [standard-version]' \
          '(https://github.com/conventional-changelog/standard-version) ' \
          'for commit guideline.\n\n'

# logger
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)

logger = logging.getLogger('svncl')
logger.setLevel(logging.DEBUG)
logger.addHandler(console)


class LogParser(object):

    """A Parse that strips out svn log to generate a changelog."""

    def __init__(self, path, xml_file) -> None:
        self._path = path
        self._xml_file = xml_file
        self._root = None
        self._key_log = []

    def get_xml_log(self):
        if self._xml_file:
            if os.path.exists(self._xml_file):
                logger.debug("Use input xml file")
                tree = ET.parse(self._xml_file)
                self._root = tree.getroot()
            else:
                logger.info("Input file not exists!")
                self._root = None
        else:
            logger.info("Generate xml from svn command")
            try:
                xml_string = check_output(['svn', 'log', self._path, '--xml']).decode('utf-8')
                self._root = ET.fromstring(xml_string)
            except CalledProcessError as e:
                logger.info(str(e))
                self._root = None

    def strip_key_log(self):
        # get all log information
        logs = []
        for logentry in self._root:
            log = {}
            log.update(logentry.attrib)  # add revision information
            # discard unused information, e.g., 'date'
            for element in logentry:
                if element.tag in ['revision', 'msg']:
                    log.update({element.tag: element.text})
            logs.append(log)
        logger.debug(logs)
        # strip out key log, e.g., 'fix', 'feat'
        self._key_log = [ele for ele in logs if any(str in ele['msg'] for str in ['feat', 'fix'])]
        self._trim_msg_tail()
        logger.debug(self._key_log)

    def _trim_msg_tail(self):
        for i, ele in enumerate(self._key_log):
            self._key_log[i]['msg'] = ele['msg'].split('\n')[0]
        logger.debug(self._key_log)

    def get_log(self):
        return self._key_log


def generate_changelog(filename, logs):
    # file header
    changelog = header
    # get current datetime
    changelog += '## (' + str(datetime.date.today()) + ')\n\n'
    # generate changelog information
    changes = ["* " + element['msg'] + ' (r' + element['revision'] + ')\n' for element in logs]
    # read input changelog and filte out repetitive log
    filted_changes = filt_changes(changes, filename)
    # add filted changes into changelog
    changelog += ''.join(filted_changes)
    return changelog


def filt_changes(changes, filename):
    # TODO: read input changelog and discard repetitive log
    return changes


def write_logfile(filename, changelog):
    # write
    with open(filename, 'w') as f:
        f.write(changelog)


def svncl(argv):

    # parse cmdline args
    parser = argparse.ArgumentParser(description="Generate changelog from svn log.")
    parser.add_argument('--path', default='.', help='svn repository directory path')
    parser.add_argument('--xml', help='input xml format logfile')
    parser.add_argument('--input', help='input changelog logfile')
    parser.add_argument('--output', default='CHANGELOG.md', help='output changelog filename')
    args = parser.parse_args()
    logger.info('Generate changlog for dir: ' + args.path)
    logger.info('xml logfile: ' + str(args.xml))
    logger.info('input changelog file: ' + str(args.input))
    logger.info('output file: ' + str(args.output))
    # instantiate a LogParser object to do the job
    log_parser = LogParser(args.path, args.xml)
    log_parser.get_xml_log()  # get xml logdata
    log_parser.strip_key_log()  # strip out key log
    # generate changelog
    changelog = generate_changelog(args.input, log_parser.get_log())
    # write changelog file
    write_logfile(args.output, changelog)


if __name__ == '__main__':
    svncl(sys.argv)
