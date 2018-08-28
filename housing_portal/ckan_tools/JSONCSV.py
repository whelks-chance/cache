import csv

import dpath as dpath
import requests

from housing_portal.survey_api import metadata, dc_info, question_detail, question_results


class JSONCSV:
    def __init__(self, username=None, password=None):

        self.username = username
        self.password = password

    def run2(self, metadata, filename, append=False):
        file_flag = 'w'
        if append:
            file_flag = 'a'

        f1 = csv.writer(open(filename, mode=file_flag))

        if not append:
            # Only write the header keys when first writing the file
            f1.writerow(sorted(metadata.keys()))

        row = []
        for key in sorted(metadata.keys()):
            cell_data = metadata[key]

            if type(cell_data) is list:
                row.append('::'.join(metadata[key]))

            elif type(cell_data) is dict:
                # Too complicated, ignore it
                # TODO whole new CSV file? *Do not* recreate a CSV filesystem style database
                row.append(None)

            else:
                row.append(metadata[key])

        f1.writerow(row)

    def run_multirow(self, metadata, filename, append=False):

        file_flag = 'w'
        if append:
            file_flag = 'a'

        f1 = csv.writer(open(filename, mode=file_flag))

        if not append:
            # Only write the header keys when first writing the file
            f1.writerow(sorted(metadata.keys()))

        should_continue = True
        row_count = 0

        # We continue while there are still rows to write
        # If we're expanding a long list this keeps going
        while should_continue:
            row = []

            for key in sorted(metadata.keys()):
                cell_data = metadata[key]

                # if the data is a list, start moving through it
                if type(cell_data) is list:

                    # print(len(cell_data), row_count, key)

                    if len(cell_data) > row_count:
                        # The length of the list is less than the current row count, write it
                        # print(key, metadata[key][row_count], len(row), row_count)
                        row.append(metadata[key][row_count])

                    else:
                        row.append('::'.join(metadata[key]))

                elif type(cell_data) is dict:
                    # Too complicated, ignore it
                    # TODO whole new CSV file? *Do not* recreate a CSV filesystem style database
                    row.append(None)

                else:
                    # if not a list...
                    if row_count == 0:
                        # if the first row, just write the value
                        row.append(metadata[key])
                    else:
                        # if we're in a later row, but it's not a list, write nothing
                        row.append(None)

            row_count += 1

            should_continue = False
            # Assume we're done, but check if there's anything in the row to write
            for cell_content in row:
                if cell_content is not None:
                    should_continue = True

            # Only write the row if there is something in it
            if should_continue:
                f1.writerow(row)

    def from_url(self, url, output_filename, dpath_desc=None):
        json_blob = requests.get(url, auth=(self.username, self.password)).json()
        if dpath_desc:
            json_blob = dpath.util.get(json_blob, dpath_desc)

        if type(json_blob) is list:
            for idx, item in enumerate(json_blob):
                if idx == 0:
                    # First run, overwrite old file
                    self.run2(item, output_filename, append=False)
                else:
                    # From then on, append lines to new file
                    self.run2(item, output_filename, append=True)
        else:
            # Overwrite old file with single item
            self.run2(json_blob, output_filename)


if __name__ == '__main__':
    jsoncsv = JSONCSV(username='ubuntu', password='a')
    jsoncsv.run2(metadata['search_result_data'][0]['data'], 'survey_metadata.csv')

    jsoncsv.run2(dc_info, 'dc_metadata.csv')

    jsoncsv.run2(question_detail, 'single_question_metadata.csv')

    jsoncsv.run2(question_results['search_result_data'][0]['data'], 'question_results_metadata.csv')

    jsoncsv.from_url(
        'https://data.wiserd.ac.uk/metadata/survey/wisid_C01WHF',
        'wisid_C01WHF_survey.csv',
        'search_result_data/0/data')

    jsoncsv.from_url(
        'https://data.wiserd.ac.uk/api/metadata/DcInfo/wisid_C01WHF/',
        'wisid_C01WHF_DcInfo.csv'
        )

    jsoncsv.from_url(
        'https://data.wiserd.ac.uk/api/metadata/Question/?survey__identifier=wisid_C01WHF&_=1535373714885',
        'questions_wisid_C01WHF.csv',
        'results'
    )
