#!/usr/bin/env python3
# -*- coding: utf-8 -*-
PROG_VERSION = "Time-stamp: <2019-12-30 11:22:22 vk>"

# TODO:
# - fix parts marked with «FIXXME»
# -

# ===================================================================== ##
#  You might not want to modify anything below this line if you do not  ##
#  know, what you are doing :-)                                         ##
# ===================================================================== ##

from importlib import import_module

def save_import(library):
    try:
        globals()[library] = import_module(library)
    except ImportError:
        print("Could not find Python module \"" + library +
              "\".\nPlease install it, e.g., with \"sudo pip install " + library + "\".")
        sys.exit(2)

import sys
import os
import argparse   # for handling command line arguments
import time
import logging
import configparser
save_import('orgformat')

PROG_VERSION_DATE = PROG_VERSION[13:23]

CONFIG_FILE_NAME = '.appendorgheading'

DESCRIPTION = "This tool appends Org mode formatted headings to existing Org mode files.\n\
\n\
The optional configuration file \"" + CONFIG_FILE_NAME + "\" can be placed:\n\
1. the current directory  ... OR ...\n\
2. the home directory (\"~/" + CONFIG_FILE_NAME + "\")\n\
Command line parameters override configuration file entries.\n\
\n\
A typical use-case for this script is logging:\n\
The author is using this to log events to some kind of 'errors.org' which is part\n\
of his Org mode agenda.\n\
\n\
  example_script.sh >out.log 2>&1 || appendorgheading --filecontent \"out.log\"\n\
\n\
This will use the default settings from your configuration file and log to the\n\
defined Org mode file only if \"example_script.sh\" has an exit status not equal\n\
to zero. It also appends the content of the log file for further analysis.\n\
\n\
\n\
"

# FIXXME: write blog entry and add this to the DESCRIPTION:
# Verbose description: http://Karl-Voit.at/FIXXME/

EPILOG = u"\n\
:copyright: (c) by Karl Voit <tools@Karl-Voit.at>\n\
:license: GPL v3 or any later version\n\
:URL: https://github.com/novoid/appendorgheading\n\
:bugreports: via github or <tools@Karl-Voit.at>\n\
:version: " + PROG_VERSION_DATE + "\n·\n"

parser = argparse.ArgumentParser(prog=sys.argv[0],
                                 # keep line breaks in EPILOG and such
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=EPILOG,
                                 description=DESCRIPTION)

parser.add_argument("--output",
                    dest="output",
                    nargs=1,
                    type=str,
                    metavar='<FILE.ORG>',
                    required=False,
                    help="Path to the Org mode file to append to")

parser.add_argument("--level",
                    dest="level",
                    nargs=1,
                    type=str,
                    metavar='<level>',
                    required=False,
                    help="The heading level (number of asterisks): 1, 2, 3, ...")

parser.add_argument("--keyword",
                    dest="keyword",
                    nargs=1,
                    type=str,
                    metavar='<TODO>',
                    required=False,
                    help="TODO keyword such as \"TODO\", \"ERROR\", ...")

parser.add_argument("--priority",
                    dest="priority",
                    nargs=1,
                    type=str,
                    metavar='"PRIO"',
                    required=False,
                    help="Priority indicator such as \"A\" or \"C\"")

parser.add_argument("--title",
                    dest="title",
                    nargs=1,
                    type=str,
                    metavar='"HEADING TITLE"',
                    required=False,
                    help="Title of the heading")

parser.add_argument("--tags",
                    dest="tags",
                    nargs=1,
                    type=str,
                    metavar='"STRING WITH TAGS"',
                    required=False,
                    help="One or more tags (if multiple: in quotes, separated by spaces)")

parser.add_argument("--scheduled",
                    dest="scheduled",
                    nargs=1,
                    type=str,
                    metavar='"STRING WITH DATE/TIME-STAMP"',
                    required=False,
                    help="An Org mode date- or time-stamp such as \"<2019-12-29 Sun>\" which is added as SCHEDULED")

parser.add_argument("--deadline",
                    dest="deadline",
                    nargs=1,
                    type=str,
                    metavar='"STRING WITH DATE/TIME-STAMP"',
                    required=False,
                    help="An Org mode date- or time-stamp such as \"<2019-12-29 Sun>\" which is added as DEADLINE")

parser.add_argument("--properties",
                    dest="properties",
                    nargs=1,
                    type=str,
                    metavar='"KEY1:VALUE1; KEY2:VALUE2"',
                    required=False,
                    help="A string with key-value pairs. Colons separate keys from values, semicolons separate the key-value-pairs.")

parser.add_argument("--section",
                    dest="section",
                    nargs=1,
                    type=str,
                    metavar='"STRING"',
                    required=False,
                    help="This is used as the section text or body of the heading.")

parser.add_argument("--filecontent",
                    dest="filecontent",
                    nargs=1,
                    type=str,
                    metavar='<FILE>',
                    required=False,
                    help="Path to a filename whose content gets appended to the section body within an EXAMPLE block")

parser.add_argument("--daily", action="store_true",
                    help="Add a time-stamp for today which is recurring on a daily basis")

parser.add_argument("--dryrun", dest="dryrun", action="store_true",
                    help="Enable dryrun mode: just simulate what would happen, do not modify files")

parser.add_argument("--generateconfigfile",
                    dest="generateconfigfile",
                    nargs=1,
                    type=str,
                    metavar='<FILE>',
                    required=False,
                    help="Path to a filename which gets created or overwritten with a configuration file that contains default values or the values given by the parameters")

parser.add_argument("-v", "--verbose",
                    dest="verbose", action="store_true",
                    help="Enable verbose mode")

parser.add_argument("-q", "--quiet",
                    dest="quiet", action="store_true",
                    help="Enable quiet mode")

parser.add_argument("--version",
                    dest="version", action="store_true",
                    help="Display version and exit")

options = parser.parse_args()


def handle_logging(verbose, quiet):
    """Log handling and configuration"""

    if verbose and quiet:
        error_exit(1, "Command line arguments for \"--verbose\" and \"--quiet\" found. " +
                   "This does not make any sense, if you think about it. You silly fool :-)")
    
    if verbose:
        print('set to verbose')
        FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    elif quiet:
        print('set to quiet')
        FORMAT = "%(levelname)-8s %(message)s"
        logging.basicConfig(level=logging.ERROR, format=FORMAT)
    else:
        print('set to else')
        FORMAT = "%(levelname)-8s %(message)s"
        logging.basicConfig(level=logging.INFO, format=FORMAT)


def error_exit(errorcode, text):
    """exits with return value of errorcode and prints to stderr"""

    sys.stdout.flush()
    logging.error(text)

    sys.exit(errorcode)


def successful_exit():
    logging.debug("successfully finished.")
    sys.stdout.flush()
    sys.exit(0)


def generate_configuration_file_content(output, level, keyword, priority, title, rawtags,
                                        scheduled, deadline, rawproperties, section,
                                        filecontent, daily):
    """
    Create or overwrite a configuration file with the given options.
    """

    result = '# This is a configuration file for the tool "appendorgheading".\n#\n'
    result += '# You can disable keys by removing its value, deleting the whole line or prepending with "# " or "; ".\n\n'
    result += '[DEFAULT]\n\n'
    result += '# output: Path to the Org mode file to append to\n'
    result += '# example: "~/org mode/my errors.org"\n'
    result += 'output = '
    if output:
        result += output

    result += '\n\n# level: The heading level (number of asterisks)\n'
    result += '# example: "2"\n'
    result += 'level = '
    if level:
        result += level

    result += '\n\n# keyword: One TODO keyword\n'
    result += '# example: "TODO" or "CRITICAL"\n'
    result += 'keyword = '
    if keyword:
        result += keyword

    result += '\n\n# priority: Priority indicator letter\n'
    result += '# example: "A" or "C"\n'
    result += 'priority = '
    if priority:
        result += priority

    result += '\n\n# title: Title of the heading\n'
    result += '# example: "This is a new heading title"\n'
    result += 'title = '
    if title:
        result += title

    result += '\n\n# tags: One or more tags (if multiple: in quotes, separated by spaces)\n'
    result += '# example: "tag1 tag2"\n'
    result += 'tags = '
    if rawtags:
        result += rawtags

    result += '\n\n# scheduled: An Org mode date- or time-stamp which gets added as SCHEDULED\n'
    result += '# example: "<2019-12-29 Sun>"\n'
    result += 'scheduled = '
    if scheduled:
        result += scheduled

    result += '\n\n# deadline: An Org mode date- or time-stamp which gets added as DEADLINE\n'
    result += '# example: "<2019-12-29 Sun>"\n'
    result += 'deadline = '
    if deadline:
        result += deadline

    result += '\n\n# properties: A string with key-value pairs. Colons separate keys from values, semicolons separate the key-value-pairs.\n'
    result += '# example: "key1:value1; key2 : value 2; key 3 : value 3"\n'
    result += 'properties = '
    if rawproperties:
        result += rawproperties

    result += '\n\n# section: This is used as the section text or body of the heading\n'
    result += '# example: "The new heading is important\\nbecause I will do this or that."\n'
    result += 'section = '
    if section:
        result += section

    result += '\n\n# filecontent: Path to a filename whose content gets appended to the section body within an EXAMPLE block\n'
    result += '# example: "~/my logs/logfile.txt"\n'
    result += 'filecontent = '
    if filecontent:
        result += filecontent

    result += '\n\n# daily: Add a time-stamp for today which is recurring on a daily basis\n'
    result += '# example: "True" or "False"\n'
    result += 'daily = '
    if daily:
        result += "True"
    else:
        result += 'False'

    logging.debug('There once were "verbose" and "quiet" in the configuration file as well. ' +
                  'However, the logging library had issues of changing logging level after ' +
                  'it was initially set via the command line parameters. So I had to remove ' +
                  'them from the configuration file. Sorry that you can\'t configure them here.')
        
    # result += '\n\n# X: \n'
    # result += '# example: ""\n'
    # result += 'X = '
    # if X:
    #     result += X

    result += '\n\n# End of configuration file'

    return result


def read_config_from_file():
    """
    Locate user configuration file and read user preferences from configuration file.
    """

    logging.debug("locating and reading " + CONFIG_FILE_NAME + " ...")

    config = configparser.RawConfigParser()
    potential_config_file_locations = []
    config_file_read = False

    for directory in os.curdir, os.path.expanduser("~"):
        config_file_name = os.path.join(directory, CONFIG_FILE_NAME)
        potential_config_file_locations.append(config_file_name)
        #logging.debug('Probing for config file: ' + config_file_name)

        if os.path.isfile(config_file_name) and not config_file_read:
            logging.debug('Reading existing config file from: ' + config_file_name)
            config.read(config_file_name)
            config_file_read = True
        elif os.path.isfile(config_file_name) and config_file_read:
            logging.debug('Existing config file was overruled by previous one: ' + config_file_name)
        elif not os.path.isfile(config_file_name) and config_file_read:
            logging.debug('Non-existing config file would have been overruled by previous one: ' + config_file_name)
        else:
            logging.debug('Config file not found at: ' + config_file_name)

    return config_file_read, config, potential_config_file_locations


def handle_preference_priorities(config_file_read, config):

    if options.output:
        output = options.output[0]
    elif config_file_read and 'output' in config['DEFAULT'].keys() and len(config['DEFAULT']['output']) > 0:
        output = config['DEFAULT']['output']
    else:
        output = None

    if options.level:
        level = int(options.level[0])  # FIXXME: check for integer type
    elif config_file_read and 'level' in config['DEFAULT'].keys() and len(config['DEFAULT']['level']) > 0:
        level = int(config['DEFAULT']['level'])  # FIXXME: check for integer type
    else:
        level = None

    if options.keyword:
        keyword = options.keyword[0]
    elif config_file_read and 'keyword' in config['DEFAULT'].keys() and len(config['DEFAULT']['keyword']) > 0:
        keyword = config['DEFAULT']['keyword']
    else:
        keyword = None

    if options.priority:
        priority = options.priority[0]
    elif config_file_read and 'priority' in config['DEFAULT'].keys() and len(config['DEFAULT']['priority']) > 0:
        priority = config['DEFAULT']['priority']
    else:
        priority = None

    if options.title:
        title = options.title[0]
    elif config_file_read and 'title' in config['DEFAULT'].keys() and len(config['DEFAULT']['title']) > 0:
        title = config['DEFAULT']['title']
    else:
        title = None

    if options.tags:  # FIXXME: check for format before converting
        rawtags = options.tags[0]
    elif config_file_read and 'tags' in config['DEFAULT'].keys() and len(config['DEFAULT']['tags']) > 0:
        rawtags = config['DEFAULT']['tags']
    else:
        tags = None
    if rawtags:
        tags = rawtags.split(' ')

    if options.scheduled:
        scheduled = options.scheduled[0]
    elif config_file_read and 'scheduled' in config['DEFAULT'].keys() and len(config['DEFAULT']['scheduled']) > 0:
        scheduled = config['DEFAULT']['scheduled']
    else:
        scheduled = None

    if options.deadline:
        deadline = options.deadline[0]
    elif config_file_read and 'deadline' in config['DEFAULT'].keys() and len(config['DEFAULT']['deadline']) > 0:
        deadline = config['DEFAULT']['deadline']
    else:
        deadline = None

    if options.properties:
        rawproperties = options.properties[0]
    elif config_file_read and 'properties' in config['DEFAULT'].keys() and len(config['DEFAULT']['properties']) > 0:
        rawproperties = config['DEFAULT']['properties']
    else:
        properties = None
        rawproperties = None
    if rawproperties:
        properties = []
        pairs = options.properties[0].split(';')
        for pair in pairs:
            key, value = pair.strip().split(':')
            properties.append((key.strip(), value.strip()))

    if options.section:
        section = options.section[0]
    elif config_file_read and 'section' in config['DEFAULT'].keys() and len(config['DEFAULT']['section']) > 0:
        section = config['DEFAULT']['section']
    else:
        section = None

    if options.filecontent:
        filecontent = options.filecontent[0]
    elif config_file_read and 'filecontent' in config['DEFAULT'].keys() and len(config['DEFAULT']['filecontent']) > 0:
        filecontent = config['DEFAULT']['filecontent']
    else:
        filecontent = None

    if options.generateconfigfile:
        generateconfigfile = options.generateconfigfile[0]
    elif config_file_read and 'generateconfigfile' in config['DEFAULT'].keys() and len(config['DEFAULT']['generateconfigfile']) > 0:
        generateconfigfile = config['DEFAULT']['generateconfigfile']
    else:
        generateconfigfile = None

    if options.daily:
        daily = True
    elif config_file_read and 'daily' in config['DEFAULT'].keys() and len(config['DEFAULT']['daily']) > 0:
        daily = config['DEFAULT'].getboolean('daily')
    else:
        daily = False

    return scheduled, rawtags, keyword, tags, section, generateconfigfile, rawproperties, \
        daily, priority, deadline, filecontent, output, title, level, properties


def check_arguments(output, level, keyword, priority, title, rawtags, tags, scheduled, deadline,
                    rawproperties, properties, section, filecontent, daily):
    pass ## FIXXME


def generate_heading_wrapper(level, keyword, priority, title, rawtags, tags, scheduled, deadline, rawproperties, properties, section, filecontent, daily):
    pass  ## FIXXME


def main():
    """Main function"""

    if options.version:
        print(os.path.basename(sys.argv[0]) + " version " + PROG_VERSION_DATE)
        sys.exit(0)

    handle_logging(options.verbose, options.quiet)

    config_file_read, config, potential_config_file_locations = read_config_from_file()

    if not config_file_read:
        logging.debug('No config found.')

    scheduled, rawtags, keyword, tags, section, generateconfigfile, rawproperties, \
        daily, priority, deadline, filecontent, output, title, level, properties = \
            handle_preference_priorities(config_file_read, config)

    # output, level, keyword, priority, title, rawtags, tags, scheduled, deadline, rawproperties, properties, section, filecontent, daily
    for pair in [('output', output), ('level', level), ('keyword', keyword), ('priority', priority),
                 ('title', title), ('rawtags', rawtags), ('tags', tags),
                 ('scheduled', scheduled), ('deadline', deadline),
                 ('rawproperties', rawproperties), ('properties', properties),
                 ('section', section), ('filecontent', filecontent),
                 ('daily', daily)]:
        logging.debug('Variable ' + str(pair[0]) + ': [' + str(pair[1]) + ']')

    check_arguments(output, level, keyword, priority, title, rawtags, tags, scheduled, deadline, rawproperties, properties, section, filecontent, daily)
        
    if generateconfigfile:
        config_file_content = generate_configuration_file_content(output, level, keyword, priority, title, rawtags, scheduled, deadline, rawproperties, section, filecontent, daily)
        if dryrun:
            logging.info('I would write the file "%s" with following content:' % generateconfigfile)
            print('-' * 80)
            print(config_file_content)
            print('-' * 80)
        else:
            logging.info('Writing new configuration to: ' + generateconfigfile)
            with open(generateconfigfile, 'w') as outputhandle:
                outputhandle.write(config_file_content)
            logging.info('Copy newly written configuration file to one of the locations: ' + str(potential_config_file_locations)[1:-1])
            logging.debug('New configuration written.')
    elif not output or not level:
        logging.info('Please do provide at least "output" and "level" parameters to generate a heading.')
    else:
        content = generate_heading_wrapper(level, keyword, priority, title, rawtags, tags, scheduled, deadline, rawproperties, properties, section, filecontent, daily)
        ## write to file (if not dryrun)


    successful_exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        logging.info("Received KeyboardInterrupt")

# END OF FILE #################################################################
# end
