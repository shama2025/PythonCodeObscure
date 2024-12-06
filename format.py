import os
import itertools
import random
from toolz import partition
import re
FRUITS = [
    "apple",
    "banana",
    "cherry",
    "date",
    "elderberry",
    "fig",
    "grape",
    "honeydew",
    "kiwi",
    "lemon",
    "mango",
    "nectarine",
    "orange",
    "papaya",
    "quince",
    "raspberry",
    "strawberry",
    "tangerine",
    "ugli fruit",
    "watermelon"
]

def get_random_fruit_names(var_name_len):
    return [FRUITS.pop(random.randint(0, len(FRUITS) - 1)) for _ in range(var_name_len)]

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
        except Exception as e:
            print(f"Error reading file {file}: {str(e)}")
        #print(python_code)
    return formatter(chunk_dict(python_code))

def chunk_dict(python_code):
    """This function will chunk the dictionary values to format one function at a time"""
    chunks = ""
    chunked_list = []
    print(type(python_code))
    python_code_list = python_code[0] #Change this when it comes to multiple file support
    python_code_list.append('\n')
    print(type(python_code_list))
    for chunk in python_code_list:
        print("Lines: ", chunk)
        if not chunk.isspace():
            chunks += chunk
        else:
            chunked_list.append(chunks)
            chunks = ""
    return chunked_list

def get_var_names(chunk):
            if "=" in chunk:
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

                        var_name = re.sub(pattern,'',chunk[sublist[0]:sublist[1]])
                        has_hashtag = var_name.find('#')
                        if  has_hashtag != -1:
                            var_name = var_name.replace(var_name[has_hashtag:sublist[0]+8],'').replace("\n",'').replace(' ','')
                    return var_name
                else:
                        var_name = re.sub(pattern,'',chunk[combined_list[0]:combined_list[1]])
                        var_name = var_name.replace(var_name[combined_list[0]:combined_list[1]],'').replace("\n",'').replace(' ','')

                        return var_name

def formatter(python_code):
    """This function will feature formating the document and return a newly formated file"""
    var_names = []
    for chunk in python_code:
        if "#" in chunk:  # or '"""' in chunk:

            comment_indexes = [i for i, c in enumerate(chunk) if c == "#"]

            if comment_indexes:
                newline_indexes = [i for i, c in enumerate(chunk) if c == "\n"]

                if len(comment_indexes) == 1:
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
                    for i in range(0, len(comment_indexes)):
                        if comment_indexes[i] > newline_indexes[i]:
                            newline_indexes.pop(
                                newline_indexes.index(newline_indexes[i])
                            )

                    for i in range(0,len(comment_indexes)):
                        new_chunk = chunk[: comment_indexes[i] + 1]
                        comment = chunk[comment_indexes[i]:newline_indexes[i]].split('#')
                        if '' in comment:
                            comment.remove('')
                        comment[0] = '#' + "".join(random.sample(comment[0],len(comment[0])))
                    python_code[python_code.index(chunk)] = chunk.replace(chunk[comment_indexes[i]:newline_indexes[i]], comment[0])
                    chunk = chunk.replace(chunk[comment_indexes[i]:newline_indexes[i]], comment[0])

        var_names.append(get_var_names(chunk))
        if None in var_names:
            var_names.remove(None)
        if "def" in chunk:
            python_code[python_code.index(chunk)] = f"exec(''' \n{chunk} ''')\n"
    fruit_names = get_random_fruit_names(len(var_names))
    for i, chunk in enumerate(python_code): # Fix this to change all names to fruit
        for name in var_names:
            chunk = chunk.replace(name, fruit_names[var_names.index(name)])
        python_code[i] = chunk

    return python_code

def main():
    """This function will house all input for the file"""
    scraped_python_code = scrape_cwd()

    with open("test11.py", "w") as f:
        for code in scraped_python_code:
            f.write(code)

if __name__ == "__main__":
    main()
