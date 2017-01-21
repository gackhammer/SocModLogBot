from __future__ import print_function




import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

class GoogleSpreadsheetHandler(object):


    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    CLIENT_SECRET_FILE = 'client_secrets.json'
    APPLICATION_NAME = 'Google Sheets API Python Quickstart'


    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'client_secrets.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def writeToSheet(self, submissionID, commentID, link, author, body, banned_by):
        """Shows basic usage of the Sheets API.

        Creates a Sheets API service object and prints the names and majors of
        students in a sample spreadsheet:
        https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)


        spreadsheet_id = '1YuAjfZ04yUnb0zZH-v784D0a2Xo3M5-QBRNEkFM210U'
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        range_name = '!A' + self.first_empty_row(sheet_metadata[0]) + ':G'

        values = [
            [
                submissionID, commentID, link, author, body, banned_by
            ]
        ]
        body = {
            'values': values
        }

        value_input_option = "USER_ENTERED";
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()

    def first_empty_row(self, sheet):
        all = sheet.get_all_values()
        row_num = 1
        consecutive = 0
        for row in all:
            flag = False
            for col in row:
                if col != "":
                    # something is there!
                    flag = True
                    break

            if flag:
                consecutive = 0
            else:
                # empty row
                consecutive += 1

            if consecutive == 2:
                # two consecutive empty rows
                return row_num - 1
            row_num += 1
        # every row filled
        return row_num