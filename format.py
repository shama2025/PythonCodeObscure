import os

def scrape_cwd():
    """This function will scrape the text of each python file and return the text"""
    cwd_list = [element for element in os.listdir() if element.endswith('.py')]
    python_code = {}
    key = 0
    for file in cwd_list:
        try:
            with open(file, 'r') as f:
                content = f.read()
            python_code.update({key : content})
            key+=1
        except Exception as e:
            print(f"Error reading file {file}: {str(e)}")
    return python_code


def chunk_dict(python_code):
    """This function will chunk the dictionary value to format one function at a time"""


def formatter(python_code):
    """This function will feature formating the document and return a newly formated file"""

def main():
    """This function will house all input for the file"""
    scraped_python_code = scrape_cwd()

    if len(scraped_python_code) > 1:
        partition_dict = chunk_dict(scraped_python_code)
        formatter(partition_dict)
    else:
        formatter(scraped_python_code)

if __name__ == "__main__":
    main()