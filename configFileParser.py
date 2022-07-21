from distutils.log import error


def parse_file(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()
    file.close()

    data = []
    list_string_values = []
    values = []
    params = {}
    new_value = 1

    for line in lines:
        current_line_values = []
        line = line.replace('\n', '')
        # Two parts param_name and param_value:
        # name_param = param_value
        if new_value:
            params = {}
            values = [value.strip() for value in line.split('=')]
            params['attribute'] = values[0]
            list_string_values = []

            # Analyse beginning of value expression
            if values[1][0] == '[':
                # Removes beginning brackets
                removed_begginning_brackets_string = \
                    values[1][1:].strip()
                values[1] = \
                    removed_begginning_brackets_string

                # Initialize params value
                params['value'] = []

            else:
                raise Exception("Invalid value format!")

        # Format: param_value_element_1, param_value_element_2,...
        else:
            values[0] = ""
            values[1] = line

        [current_line_values.append(value) for value in values[1].split(',')]

        list_last_value = len(current_line_values) - 1

        # If the line ends without comma ,
        if (current_line_values[list_last_value] != ''):
            # Removes Ending brackets ]
            current_line_values[list_last_value] = \
                current_line_values[list_last_value][0:-1]

            # Removes beginning and ending quotes '
            current_line_values = \
                [value.strip()[1:-1] for value in current_line_values]

            [list_string_values.append(value) for value in current_line_values]

            params['value'] = list_string_values

            new_value = 1

            data.append(params)

        # Continues on the next line
        else:
            # Removes void element ''
            current_line_values.pop()

            # Removes beginning and ending quotes ' '
            current_line_values = \
                [value.strip()[1:-1] for value in current_line_values]

            [list_string_values.append(value) for value in current_line_values]

            new_value = 0

    return data