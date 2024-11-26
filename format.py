import os
import re
import random

def scrape_cwd():
    """This function will scrape the text of each python file and return the text"""
    cwd_list = [chunk for chunk in os.listdir() if chunk.endswith('.py')]
    python_code = {}
    key = 0
    for file in cwd_list:
        try:
            with open('test.py', 'r') as f:
                content = f.readlines()
                python_code.update({key : content})
                key+=1
        except Exception as e:
            print(f"Error reading file {file}: {str(e)}")
    return formatter(chunk_dict(python_code))

# Remove this function maybe
def chunk_dict(python_code):
    """This function will chunk the dictionary values to format one function at a time"""
    chunks = ''

    chunked_list = []
    test_py_list = python_code[0]
    for chunk in test_py_list:
        if  not chunk.isspace():
            chunks+= chunk
        else:
            chunked_list.append(chunks)
            chunks = ''
    return chunked_list


def formatter(python_code):
    """This function will feature formating the document and return a newly formated file"""

    idx = 1
    shuffled_comments = []
    for chunk in python_code:
        if "#" in chunk: # or '"""' in chunk:

            char = '#'
            comment_indexes = [i for i, c in enumerate(chunk) if c == char]

            if comment_indexes: # Filters out empty sections of code where there are not #
                char = '\n'
                newline_indexes = [i for i, c in enumerate(chunk) if c == char]

                if len(comment_indexes) == 1 and len(newline_indexes) == 1: # If there is one item in the chunk then randomize using the first index in the \n array
                    new_chunk = chunk[:comment_indexes[0] + 2]
                    new_chunk += "".join(random.sample(chunk[comment_indexes[0]+2:newline_indexes[0]], len(chunk[comment_indexes[0]+2:newline_indexes[0]])))
                    new_chunk += chunk[newline_indexes[0]:]
                    python_code[python_code.index(chunk)] = new_chunk
                else:
                    for i in range(1,len(comment_indexes)):
                        if comment_indexes[i] > newline_indexes[i]:
                            newline_indexes.pop(newline_indexes.index(newline_indexes[i]))

                    new_chunk = chunk[:comment_indexes[0] + 2]
                    new_chunk += "".join(random.sample(chunk[comment_indexes[0]+2:newline_indexes[0]], len(chunk[comment_indexes[0]+2:newline_indexes[0]])))
                    new_chunk += chunk[newline_indexes[0]:]
                    python_code[python_code.index(chunk)] = new_chunk

        # make a section that focuses on variable names and converting those
        if '=' in chunk:
            "Swap variable names with names of fruit"
        if "def" in chunk: # formats function declaration to be exec("""""")
            python_code[idx]= 'exec("""'+ chunk + '""")'

    #print(python_code)

def main():
    """This function will house all input for the file"""
    scraped_python_code = scrape_cwd()

if __name__ == "__main__":
    main()