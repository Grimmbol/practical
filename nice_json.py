# -*- coding: utf-8 -*-
"""
@author Øystein Krogstie
Small python utility that can make a single-line json file more readable by
adding line breaks and indentation, as well as re-compacting an indented json file by
stripping it of both
"""
import sys


class json_processor:

    def __init__(self):
        self.json_string=""
        self.json_string_length=0
        self.indent = "    "

    # Reads the file at the source url, or the following command line argument, if
    # source_url is set to None
    def load_json(self, source_url):
        if source_url != None:
            source_file = open(source_url, 'r')
            self.json_string = source_file.read()
            self.json_string_length = len(self.json_string)

    def set_indent(self, type, number):
        if type == 's':
            self.indent = str.join("",[' ' for i in range(number)])
        elif type == 't':
            self.indent = str.join("",['\t' for i in range(number)])
        else:
            print("Unrecogniced indent type, indent unchanged. " +
                  "Current value is \"" + self.indent+"\"")

    # The default value of -1 indicates that the indentation process should end
    # at the final character of the string
    def indent_json(self, start=0, end=-1):
        result_strings = []
        indent_depth = 0
        if end == -1:
            end = self.json_string_length

        for i in range(start, end):
            current = self.json_string[i]
            result_strings.append(current)

            # For certain characters, we need to add line breaks or indents
            if (current == '{' or current == '['):
                indent_depth += 1
                result_strings.append('\n')
                result_strings.append("".join([self.indent for i in range(indent_depth)]))
            elif(current == ':'):
                result_strings.append(' ')

            elif(current == ','):
                result_strings.append('\n')
                result_strings.append("".join([self.indent for i in range(indent_depth)]))

            elif(current == '}' or current == ']'):
                indent_depth -= 1
                result_strings = result_strings[:len(result_strings)-1]+['\n']
                result_strings.append("".join([self.indent for i in range(indent_depth)]))
                result_strings += [current]

        result = "".join(result_strings)
        self.json_string_length = len(result)
        self.json_string = result

    # This method removes all whitespace from the json string
    def compact_json(self, start=0, end=-1):
        result_strings = []
        whitespace = [' ', '\t', '\n']

        if end == -1:
            end = self.json_string_length

        for i in range(start, end):
            current = self.json_string[i]
            if current not in whitespace:
                result_strings.append(current)

        result = "".join(result_strings)
        self.json_string_length = len(result)
        self.json_string = result

    def fix_quotes(self, start=0, end=-1):
        result_strings = [];
        if end == -1:
            end = self.json_string_length

        for i in range(start, end):
            current = self.json_string[i]
            if(current=='\''):
                result_strings.append('\"')
            else:
                result_strings.append(self.json_string[i])
        self.json_string = "".join(result_strings)
        self.json_string_length = len(self.json_string)


    def cleanup_json(self, start=0, end=-1):
        self.compact_json()
        self.fix_quotes()
        self.indent_json()

    def print_json(self):
        print(self.json_string)

    def get_info(self):
        return {"indent": self.indent, "lenght": self.json_string_length}

    # Iterates over the file, looing for spaces or tabs. If one is found,
    # the function returns with the location of the first delimiter detected
    def detect_indents(self, start):
        pass

    # Iterates over the file, looking for missing indents. If one is found,
    # return the location of the first inconsitency
    def detect_inconcistency(self, start):
        pass

def print_help():
    pass

# The main method processes program parameters, and takes appropriate actions
def main():
    echo = False
    direct_input = False
    input_source = sys.argv[1]
    arguments = iter(sys.argv[2:])
    processor = json_processor()

    while(True):
        try:
            current = next(arguments)
            if current == "-p":
                echo = True #print the result
            elif current == "-d":
                direct_input = True #Read the result directly from the input stream
            elif current == "-h":
                print("Summary of options: -p ")
                # If the argument didn't match any option, try to parse directly from
                # stream, if the flag is set. Otherwiseerwise, print an error and abort

        # When the arguments have all been fished out of the iterator,
        # we break out of the loop
        except StopIteration:
            break;


    json_string = processor.load_json(input_source)
    processor.set_indent('s', 4)
    processor.cleanup_json()
    processor.print_json()

main()
