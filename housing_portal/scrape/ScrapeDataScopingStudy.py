import getopt
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cache.settings")
import django
django.setup()

from housing_portal import models
import csv

__author__ = 'ubuntu'


if __name__ == "__main__":

    input_file = ''
    identifier = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:s:", ["ifile=", "survey="])
        print(opts)
        print(args)
    except getopt.GetoptError as egiog:
        print(egiog)
        print('test.py -i <inputfile> -s <survey_identifier>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            input_file = arg

        elif opt in ("-s", "--survey"):
            identifier = arg

    if input_file and identifier:
        load_shapefile_description(input_file, identifier)
    else:
        print('need a file and survey_id')
        print('update_survey_region_metadata.py -i <inputfile> -s <survey>')
        sys.exit(2)