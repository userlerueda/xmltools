#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage:
  {py} [options] view
  {py} [options] merge <inputXML1> <inputXML2>
  {py} (-h | --help)
  {py} -v

Arguments:
  <xmlfile>  File that contains XML text.

Options:
  -h --help                         Show this screen.
  -v --version                      Show version.
  -i --input=<xmlfile>              XML file used for input.
  -o --output=<xmlfile>             XML file used for output.
  -t --tag=<tag>                    XML tag that is common for merging (make sure to include ns).
  -p --pretty_print                 If enabled the XML will be Pretty Printed.
  --loglevel=<loglevel>             Log level, default is CRITICAL, can be ERROR, WARNING, INFO, DEBUG [defaul: critical]

"""
from docopt import docopt
from lxml import etree
import logging
import os
import pbr.version
import sys

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__status__ = "Development"   # Prototype, Development or Production
# __version__ = pbr.version.VersionInfo('xmltools').release_string()
__version__ = pbr.version.VersionInfo('xmltools').release_string()


def main():
    logger = logging.getLogger()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    program_name = os.path.basename(sys.argv[0])
    args = docopt(__doc__.replace('{py}', program_name), version=__version__)
    valid_log_levels = ("INFO", "ERROR", "WARNING", "DEBUG", "CRITICAL")
    if args["--loglevel"]:
        if args["--loglevel"].upper() in valid_log_levels:
            SCREEN_LOGGING_LEVEL = eval("logging." + args["--loglevel"]
                                        .upper())
        else:
            print("Invalid logging level '{}'".format(args["--loglevel"]))
            print("Must be {}".format(valid_log_levels))
            sys.exit(10)
    else:
        SCREEN_LOGGING_LEVEL = logging.CRITICAL
    logger.setLevel(SCREEN_LOGGING_LEVEL)
    stream_handler.setLevel(SCREEN_LOGGING_LEVEL)
    logger.debug(args)

    if args["view"]:
        xmldoc = etree.parse(args["--input"])
        print(type(xmldoc))
        print(etree.tostring(xmldoc, pretty_print=args["--pretty_print"]))

    if args["merge"]:
        xmldoc1 = etree.parse(args["<inputXML1>"])
        xmldoc2 = etree.parse(args["<inputXML2>"])
        root1 = xmldoc1.getroot()
        root2 = xmldoc2.getroot()
        # Ensure tag exists in XML1 and XML2
        if args["--tag"]:
            if root1.findall(args["--tag"]) and \
               root2.findall(args["--tag"]):
                intersect1 = root1.findall(args["--tag"])[0]
                intersect2 = root2.findall(args["--tag"])[0]
                intersect1.getparent().append(intersect2)
                print(etree.tostring(root1))
        else:
            print("'{}' tag not found in either '{}' or '{}'".format(
                args["--tag"], args["<inputXML1>"], args["<inputXML1>"]))
        if args["--output"]:
            outFile = open(args["--output"], 'w')
            root1.getroottree().write(
                outFile, pretty_print=args["--pretty_print"])

    # if args["generate"]:
    #     root = etree.Element('config', xmlns='http://tail-f.com/ns/config/1.0')
    #     print(type(root))
    #     print(root.tag)
    #     catalogET = etree.SubElement(root, 'catalog', xmlns='http://cisco.com/ns/branch-infra-common')
    #     nameET = etree.SubElement(catalogET, 'name')
    #     nameET.text = 'vBranch'
    #     deploymentET = etree.SubElement(catalogET, 'deployment')
    #     xmldoc = etree.ElementTree(root)
    #     if args["--output"]:
    #         outFile = open(args["--output"], 'w')
    #         xmldoc.write(outFile, pretty_print=rgs["--pretty_print"])


if __name__ == "__main__":
    sys.exit(main())
