# pylint: skip-file


from ansible.errors import AnsibleFilterError


def items2dict(items, key='name', keep_key=True):
    new_dict = dict()
    for item in items:
        if item[key] in new_dict:
            raise AnsibleFilterError('The key \'{}\' is not unique, thus no proper dictionary can be created.'.format(key))
        new_dict[item[key]] = dict()
        for k, v in item.items():
            new_dict[item[key]].update({k: v})
        if not keep_key:
            del new_dict[item[key]][key]
    return new_dict



class FilterModule(object):
    def filters(self):
        return {
            "items2dict": items2dict,
        }
