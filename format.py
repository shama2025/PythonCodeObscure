import os
import itertools
import random
from toolz import partition
import re

def scrape_cwd():
    """This function will scrape the text of each python file and return the text"""
    cwd_list = [chunk for chunk in os.listdir() if chunk.endswith(".py")]
    python_code = {}
    key = 0
    for file in cwd_list:
        try:
            with open("test.py", "r") as f:
                content = f.readlines()
                python_code.update({key: content})
                key += 1
        except Exception as e:
            print(f"Error reading file {file}: {str(e)}")
    return formatter(chunk_dict(python_code))


# Remove this function maybe
def chunk_dict(python_code):
    """This function will chunk the dictionary values to format one function at a time"""
    chunks = ""

    chunked_list = []
    test_py_list = python_code[0]
    for chunk in test_py_list:
        if not chunk.isspace():
            chunks += chunk
        else:
            chunked_list.append(chunks)
            chunks = ""
    return chunked_list

def get_var_names(chunk):
            pattern = r'\b(def|if|else|for|in|return|range|import|from|as|with|try|except|class|lambda|while|break|continue|and|or|not|is|None|True|False)\b|[()\[\]{},:;]|[+*/%\-<>=!&|^~]+|[\'"].*?[\'"]|__name__'
            variable_indexes = [i for i, c in enumerate(chunk) if c == "="]
            newline_indexes = [i for i, c in enumerate(chunk) if c == "\n"]
            result = [variable_indexes[0]] + [
                    variable_indexes[i+1]
                    for i in range(len(variable_indexes)-1)
                    if abs(variable_indexes[i+1] - variable_indexes[i]) > 1
                ]
            variable_indexes = result
            newline_indexes = newline_indexes[:-(len(newline_indexes) - len(variable_indexes))]

            combined_list = sorted(itertools.chain(newline_indexes,variable_indexes))

            if len(combined_list) > 2:
                combined_list = list(partition(2,combined_list))
                for sublist in combined_list:

                    test = re.sub(pattern,'',chunk[sublist[0]:sublist[1]])
                    has_hashtag = test.find('#')
                    if  has_hashtag != -1:
                        test = test.replace(test[has_hashtag:sublist[0]+8],'').replace("\n",'').replace(' ','')
                    #print(chunk.replace(test,"Some fruit"))
                return test
            else:
                    test = re.sub(pattern,'',chunk[combined_list[0]:combined_list[1]])
                    test = test.replace(test[combined_list[0]:combined_list[1]],'').replace("\n",'').replace(' ','')

                    return test


def formatter(python_code):
    """This function will feature formating the document and return a newly formated file"""

    for chunk in python_code:
        
        if "#" in chunk:  # or '"""' in chunk:

            comment_indexes = [i for i, c in enumerate(chunk) if c == "#"]

            if comment_indexes:
                newline_indexes = [i for i, c in enumerate(chunk) if c == "\n"]

                if len(comment_indexes) == 1 and len(newline_indexes) == 1:
                    new_chunk = chunk[: comment_indexes[0] + 1]
                    new_chunk += "".join(
                        random.sample(
                            chunk[comment_indexes[0] + 2 : newline_indexes[0]],
                            len(chunk[comment_indexes[0] + 2 : newline_indexes[0]]),
                        )
                    )
                    new_chunk += chunk[newline_indexes[0] :]
                    python_code[python_code.index(chunk)] = new_chunk
                else:
                    for i in range(1, len(comment_indexes)):
                        if comment_indexes[i] > newline_indexes[i]:
                            newline_indexes.pop(
                                newline_indexes.index(newline_indexes[i])
                            )

                    # will need to get the length of the comment and then pop everything right of it
                    """
                        for example:
                            comment_indexes = [5,17]
                            newline_indexes = [10,34,16]

                            newline_indexes = newline_indexes.pop(everything right of len(comment_indexes))

                            newline_indexes = [10,34]
                    """
                    # Fix this to include the second set of comments
                    #newline_indexes = newline_indexes[:-len(comment_indexes)+1]
                    # print("Post pop Newline indexs: ", newline_indexes)

                    # print("Comment indexes: ", comment_indexes)
                    new_chunk= chunk[: comment_indexes[0] + 1] # This gets the #
                   # print(new_chunk)
                    new_chunk += "".join( # This randomizes the actual comment
                        random.sample(
                            chunk[comment_indexes[0] + 2 : newline_indexes[0]],
                            len(chunk[comment_indexes[0] + 2 : newline_indexes[0]]),
                        )
                    )
                    #print(chunk[newline_indexes[0]])
                    new_chunk += chunk[newline_indexes[0] :] # This is the rest of the function
                    python_code[python_code.index(chunk)] = new_chunk
            chunk = new_chunk
        if "=" in chunk:
            print("Chunk with equal sign: \n", chunk)
            # Will need this to be a function that returns a
            # variable name and changes all occurences of that name
            var_names = get_var_names(chunk)
            print("A variable name: ",var_names)
            python_code[python_code.index(chunk)] = chunk.replace(var_names,"Blah_Blah")
            chunk = chunk.replace(var_names,"Blah_Blah")
        if "print" in chunk:
             "look for variable names and change them with the ones in var_names"
            #  print("In print if tree: ",var_names)
            #  print(chunk)
             python_code[python_code.index(chunk)] = chunk.replace(var_names,"Blah_print_Blah")
             print(python_code)
        if "def" in chunk:  # formats function declaration to be exec("""""")
            # can also add a way to change the parameter names as well
            python_code[python_code.index(chunk)] = f"exec(''' \n{chunk} ''')\n"
    return python_code
    #print(python_code)

def main():
    """This function will house all input for the file"""
    scraped_python_code = scrape_cwd()

    with open("test4.py", "w") as f:
        for code in scraped_python_code:
            f.write(code)

if __name__ == "__main__":
    main()
