# -------------------------------------------------------
# Copyright (c) [2024] FASNY
# All rights reserved
# -------------------------------------------------------
""" Invoices management script """
# -------------------------------------------------------
# Nadège LEMPERIERE, @6th November 2024
# Latest revision: 6th November 2024
# -------------------------------------------------------

# System includes
from logging    import config, getLogger
from os         import path as lpath

# Click includes
from click      import option, group

# Requests includes
from requests   import get, post

# Openpyxl includes
from openpyxl   import Workbook

# Logger configuration settings
logg_conf_path = lpath.normpath(lpath.join(lpath.dirname(__file__), 'conf/logging.conf'))

#pylint: disable=W0719, R0902
class Workflow:
    """ Class managing invoice processing workflow """

    s_ApiUrl = "https://graph.microsoft.com/v1.0"

    def __init__(self, token, path, output):
        """
        Constructor
        Parameters :
            token (str)     : A temporary oauth token creating to access the file (cf doc)
            path (str)      : The OneDrive tree root folder to process
            output (str)    : The resulting excel sheet to create
        Returns    :
        Throws     :
        """

        # Initialize logger
        self.__logger = getLogger('workflow')
        self.__logger.info('INITIALIZING PROCESSING')

        # Store configuration
        self.__header = { "Authorization": f"Bearer {token}" }
        self.__path   = f"/me/drive/root:/{path}:/children"
        self.__output = output

    def process(self):
        """
        Creating excel sheet
        Parameters :
        Returns    :
        Throws     :
        """

        self.__logger.info('STARTING PROCESSING')

        # Create a new Excel workbook
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "OneDrive Files"

        # Header row
        sheet.append(["File Name", "Shareable Link"])

        # Start processing the root folder
        Workflow.__process_folder(self.__logger, self.__header, self.__path, sheet)

        # Save workbook to Excel file
        try:
            workbook.save(self.__output)
            self.__logger.info('---> Excel sheet generated %s', self.__output)
        except Exception as e:
            self.__logger.error('Failed to save Excel sheet: %s', e)

    # Function to list files and folders in a OneDrive folder
    @staticmethod
    def __list_files(headers, path):
        """
        List file in a subdirectory (to be called recursively)
        Parameters :
            headers (dict) : http headers to use to retrieve OneDrive Files
            path (str)     : OneDrive file path
        Returns (list)     : The list of files in current directory
        Throws     :
        """

        result = {}

        url = f"{Workflow.s_ApiUrl}{path}"
        response = get(url, headers=headers, timeout=100)
        response.raise_for_status()
        result = response.json().get("value", [])
        return result

    # Function to create a shareable link for a file
    @staticmethod
    def __create_share_link(headers, file):
        """
        Share a file and return its access link (to be called recursively)
        Parameters :
            headers (dict) : http headers to use to retrieve OneDrive Files
            file (str)     : File identifier
        Returns (str)      : The file access url
        Throws     :
        """

        result = ""

        url = f"{Workflow.s_ApiUrl}/me/drive/items/{file}/createLink"
        payload = {
            "type": "view",
            "scope": "anonymous"  # 'anonymous' for anyone with the link
        }
        response = post(url, headers=headers, json=payload, timeout=100)
        response.raise_for_status()
        result = response.json().get("link", {}).get("webUrl", "")
        return result

    # Recursive function to process files in folders and subfolders
    @staticmethod
    def __process_folder(logger, headers, path, sheet):
        """
        Recursive function to process all subfolders, list files and share them
        Parameters :
            logger (Logger)     : the logger to use for traces
            headers (dict)      : http headers to use to update OneDrive Files
            path (str)          : root folder path
            sheet (Workbook)    : Excel sheet to update
        Throws     :
        """
        items = Workflow.__list_files(headers,path)
        for item in items:
            item_name = item["name"]
            item_id = item["id"]

            # Check if the item is a folder
            if item.get("folder"):
                # Recursive call to process files within this subfolder
                subfolder_path = f"/me/drive/items/{item_id}/children"
                logger.info('Processing folder %s', subfolder_path)
                Workflow.__process_folder(logger, headers, subfolder_path, sheet)
            else:
                # Generate shareable link for file
                link = Workflow.__create_share_link(headers, item_id)
                # Append file information to the sheet
                sheet.append([item_name, link])
                logger.debug('---> Processed file %s with link %s', item_name, link)

# pylint: disable=W0107
# Main function using Click for command-line options
@group()
def main():
    """ Main click group """
    pass
# pylint: enable=W0107, W0719

# pylint: disable=R0913
@main.command()
@option('--token', default='')
@option('--path', default='/')
@option('--output',default='links.xlsx')
def run(token, path, output):

    """ Script run function """
    workflow = Workflow(token, path, output)
    workflow.process()
# pylint: enable=R0913

if __name__ == "__main__":
    config.fileConfig(logg_conf_path)
    main()
