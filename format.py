import os
import re
import random

def scrape_cwd():
    """This function will scrape the text of each python file and return the text"""
    cwd_list = [element for element in os.listdir() if element.endswith('.py')]
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
    for element in test_py_list:
        if  not element.isspace():
            chunks+= element
        else:
            chunked_list.append(chunks)
            chunks = ''
    return chunked_list


def formatter(python_code):
    """This function will feature formating the document and return a newly formated file"""

    idx = 1
    shuffled_comments = []
    for element in python_code:
        if "#" in element or '"""' in element:
            split_elements = element.split('\n')
            for element in split_elements:
                if "#" not in element and '"""' not in element:
                    split_elements.pop(split_elements.index(element))

            unshuffled_comments = [re.sub(r'\bprint\s*\([^)]*\)', '', element) for element in split_elements]

            for comment in unshuffled_comments:
                list_comment = list(comment.replace(" ", ""))
                if "#" in comment: # look at alternative ways to shuffle the text will need to implement ai to shuffle the text
                    """str + list + str"""
                    shuffled_comments.append(list_comment[0] + "".join(random.sample(list_comment[1:-2],len(list_comment[1:-2]))) + "".join(list_comment[-1:]))
                else:
                    #print(type(list_comment[0:2]) , type(random.sample(list_comment[3:-4],len(list_comment[3:-4]))) , type(list_comment[-3]))
                    """list + list + str"""
                    shuffled_comments.append("".join(list_comment[0:2]) + "".join(random.sample(list_comment[3:-4],len(list_comment[3:-4]))) + "".join(list_comment[-3:]))

            print(shuffled_comments)

        # now put the comments back into the code
        
        # make a section that focuses on variable names and converting those
        if '=' in element:
            "Swap variable names with names of fruit"
        if "def" in element: # formats function declaration to be exec("""""")
            python_code[idx]= 'exec("""'+ element + '""")'

    #print(python_code)

def main():
    """This function will house all input for the file"""
    scraped_python_code = scrape_cwd()

if __name__ == "__main__":
    main()