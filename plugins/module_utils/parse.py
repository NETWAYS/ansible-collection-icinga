# pylint: skip-file
import re


class Icinga2Parser(object):

    def parse(self, attrs, constants, indent=0):
        def attribute_types(attr):
            if re.search(r'^[a-zA-Z_][a-zA-Z0-9_]*$', attr):
                result = attr
            else:
                result = '"' + attr + '"'
            return result

        def value_types(value, indent=2):
            # Values without quotes
            if ((re.search(r'^-?\d+\.?\d*[dhms]?$', value)) or
               (re.search(r'^(true|false|null)$', value)) or
               (re.search(r'^!?(host|service|user)\.', value)) or
               any(value.startswith(constant + '.') for constant in constants)):
                result = value
            elif (re.search(r'^(True|False)$', value)):
                result = value.lower()
            elif value in constants:
                # Check if it is a constant
                result = value
            else:
                # Print a normal string
                result = '"' + value + '"'
            return result

        def parser(row):
            # Disable parsing of the value if prefix -:
            r = re.search(r'^-:(.*)$', row)
            if r:
                # print("Ignore Row: " + row)
                return r.group(1)

            # r = re.search(r'^\{{2}(.+)\}{2}$', row)
            r = re.search(r'^\{{2}(.+)\}{2}$', row)
            if r:
                return "{{ %s }}" % (r.group(1))

            r = re.search(r'^(.+)\s([\+-]|\*|\/|==|!=|&&|\|{2}|in)\s\{{2}(.+)\}{2}$', row)
            if r:
                # print("Im a expression with a function " + row )
                return "%s %s {{ %s }}" % (parser(r.group(1)), r.group(2), r.group(3))

            r = re.search(r'^(.+)\s([\+-]|\*|\/|==|!=|&&|\|{2}|in)\s(.+)$', row)
            if r:
                # print("Im a expression maybe assign " + row)
                return "%s %s %s" % (parser(r.group(1)), r.group(2), parser(r.group(3)))

            # Search for string with round brackets, then parse the function. Ex.: match("name", host.name)
            r = re.search(r'^(.+)\((.*)$', row)
            if r:
                s = ', '
                return "%s(%s" % (r.group(1), s.join(list(map(lambda x: x.lstrip(), parser(r.group(2)).split(',')))))

            # Search for closing bracket
            r = re.search(r'^(.*)\)(.+)?$', row)
            if r:
                s = ', '
                if r.group(2):
                    return "%s)%s" % (s.join(list(map(lambda x: parser(x.lstrip()), r.group(1).split(', ')))), r.group(2))
                else:
                    return " %s)" % (s.join(list(map(lambda x: parser(x.lstrip()), r.group(1).split(', ')))))

            r = re.search(r'^\((.*)$', row)
            if r:
                return "(%s" % (parser(r.group(1)))

            r = re.search(r'^\s*\[\s*(.*)\s*\]\s?(.+)?$', row)
            if r:
                # print("Its an array - process it " + row)
                result = "[ %s]" % (process_array(r.group(1).split(',')))
                if r.group(2):
                    result += " %s" % (parser(r.group(2)))
                return result

            r = re.search(r'^\s*\{\s*(.*)\s*\}\s?(.+)?$', row)
            if r:
                # print("Its an hash " + row)
                result = "%s" % (process_hash(dict(list(divide_chunks((re.sub(r'\s*=\s*|\s*,\s*', ',', r.group(1)).split(',')), 2)))))
                if r.group(2):
                    result += " %s" % (parser(r.group(2)))
                return result

            return str(value_types(row.lstrip(' ')))

        def process_array(items, indent=2):
            result = ''
            for item in items:
                if isinstance(item, dict):
                    result += "\n%s{\n%s%s}, " % (' ' * indent, process_hash(attrs=item, indent=indent+2), ' ' * indent)
                elif isinstance(item, list):
                    result += "[ %s], " % (process_array(item.split(','), indent=indent+2))
                else:
                    result += "%s, " % (parser(str(item)))
            return result

        def process_hash(attrs, level=3, indent=2, prefix=' '):
            result = ''
            if re.search(r'^\s+$', prefix):
                prefix = prefix * indent
            op = ''

            for attr, value in attrs.items():
                if isinstance(value, dict):
                    if "+" in value:
                        del value['+']
                        op = "+"
                    if not bool(value):
                        # print("Its empty- moving on")
                        if level == 1:
                            result += "%s%s %s={}\n" % (prefix, attr, op)
                        elif level == 2:
                            result += "%s[\"%s\"] %s= {\n%s%s}\n" % (
                                prefix, attr, op, process_hash(attrs=value, indent=indent+2), ' '*indent)
                        else:
                            result += "%s%s %s= {\n%s%s}\n" % (
                                prefix, attribute_types(attr), op, process_hash(attrs=value, indent=indent+2), ' '*indent)

                    # "%s%s #{op}= {\n%s%s}\n" % [prefix, attribute_typess(attr), process_hash(value, indent + 2), ' ' * indent]
                    else:
                        # print("Next Level for: " + str(value))
                        # print(indent)
                        indent_char = ' '
                        if level == 1:
                            result += process_hash(attrs=value, level=2, indent=indent, prefix=(prefix + attr))
                        elif level == 2:
                            result += "%s[\"%s\"] %s= {\n%s%s}\n" % (
                                prefix, attr, op, process_hash(attrs=value, indent=indent), (indent-2)*indent_char)
                        else:
                            result += "%s%s %s= {\n%s%s}\n" % (
                                prefix, attribute_types(attr), op, process_hash(attrs=value, indent=indent+2), ' '*indent)
                elif isinstance(value, list) and value:
                    if value[0] == "+":
                        op = "+"
                        value.pop(0)
                    elif value[0] == "-":
                        op = "-"
                        value.pop(0)
                    if level == 2:
                        result += "%s[\"%s\"] %s= [ %s]\n" % (
                            prefix, attribute_types(attr), op, process_array(value))
                    else:
                        result += "%s%s %s= [ %s]\n" % (
                            prefix, attribute_types(attr), op, process_array(value))
                else:
                    value = str(value)
                    r = re.search(r'^([\+,-])\s+', value)
                    if r:
                        operator = r.group(1)
                        value = re.sub(r'^[\+,-]\s+', '', value)
                    else:
                        operator = ''
                    if level > 1:
                        if level == 3:
                            if value != None:
                                result += "%s%s %s= %s\n" % (
                                    prefix, attribute_types(attr), operator, parser(value))
                        else:
                            if value != None:
                                result += "%s[\"%s\"] %s= %s\n" % (prefix, attr, operator, parser(value))
                    else:
                        if value != None:
                            result += "%s%s %s= %s\n" % (prefix, attr, operator, parser(value))

            return result

        def divide_chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i:i + n]

        config = ''
        op = ''

        for attr, value in attrs.items():
            # if re.search(r'^(assign|ignore) where$', attr):
            if attr == 'assign' or attr == 'ignore':
                for x in value:
                    config += "%s%s %s\n" % (' '*indent, attr+' where', parser(x))
            elif attr == 'vars':
                if isinstance(value, dict):
                    if "+" in value:
                        del value['+']
                    config += process_hash(attrs=value, indent=indent+2, level=1, prefix=("%s%s." % (' '*indent, attr)))
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            config += "%s%s += %s\n" % (indent*' ', attr, re.sub(r'^[\+,-]\s+/', '', item))
                        else:
                            if "+" in item:
                                del item["+"]
                            if not bool(item):
                                config += "%s%s += {}\n" % (' ' * indent, attr)
                            else:
                                config += process_hash(attrs=item, indent=indent+2, level=1, prefix=("%s%s." % (' '*indent, attr)))
                else:
                    if re.search(r'^\+\s+', value):
                        op = '+'
                        value = re.sub(r'^\+\s+', '', str(value))
                    config += "%s%s %s= %s\n" % (' ' * indent, attr, op, parser(value))
            else:
                if isinstance(value, dict):
                    if "+" in value:
                        op = '+'
                        del value['+']
                    if bool(value):
                        config += "%s%s %s= {\n%s%s}\n" % (' '*indent, attr, op, process_hash(attrs=value, indent=indent+2), ' '*indent)
                    else:
                        config += "%s%s %s= {}\n" % (' '*indent, op, attr)
                elif isinstance(value, list):
                    if value:
                        if value[0] == "+":
                            op = "+"
                            value.pop(0)
                        elif value[0] == "-":
                            op = "-"
                            value.pop(0)
                    config += "%s%s %s= [ %s]\n" % (' ' * indent, attr, op, process_array(value))
                elif value is None:
                    config += ''
                else:
                    r = re.search(r'^([\+,-])\s+', str(value))
                    if r:
                        config += "%s%s %s= %s\n" % (' '*indent, attr, r.group(1), parser(re.sub(r'^[\+,-]\s+', '', str(value))))
                    else:
                        config += "%s%s = %s\n" % (' '*indent, attr, parser(str(value)))

        return config
