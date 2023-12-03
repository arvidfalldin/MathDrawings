import os
import re
import argparse


class StoreDict(argparse.Action):
    """
    Custom argparse action for storing dict.

    In: args1:0.0 args2:"dict(a=1)"
    Out: {'args1': 0.0, arg2: dict(a=1)}
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super(StoreDict, self).__init__(option_strings,
                                        dest,
                                        nargs=nargs,
                                        **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        arg_dict = {}
        for arguments in values:
            arg_dict_local = self.split(arguments)
            arg_dict = {**arg_dict, **arg_dict_local}
        setattr(namespace, self.dest, arg_dict)

    def split(self, arguments):
        arg_dict = {}
        key = arguments.split(":")[0]
        value = ":".join(arguments.split(":")[1:])
        # Evaluate the string as python code
        try:
            if ':' in value:
                arg_dict_lower = self.split(value)
                arg_dict[key] = arg_dict_lower
            else:
                arg_dict[key] = eval(value)
        except NameError:
            arg_dict[key] = value
        except SyntaxError:
            return {key: value}

        return arg_dict


def load_settings(yaml_file, args):
    import yaml

    # Yaml bug workaround,
    # https://stackoverflow.com/questions/30458977/yaml-loads-5e-6-as-string-and-not-a-number
    # (seem to be work to add this to yaml main)
    loader = yaml.SafeLoader
    loader.add_implicit_resolver(
        u'tag:yaml.org,2002:float',
        re.compile(u'''^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$''', re.X),
        list(u'-+0123456789.'))

    # Load settings from yaml file
    if os.path.isfile(yaml_file):
        with open(yaml_file, 'r') as f:
            # settings_dict = yaml.safe_load(f)
            settings = yaml.load(f, Loader=loader)
    else:
        settings = {}

    # Overwrite hyperparams from command line, if exists
    if args.settings is not None:
        for k, v in args.settings.items():
            if type(v) is not dict:
                settings[k] = v
            # Solution for overwriting single kwargs of second 'level'
            elif k not in settings:
                settings[k] = v
            else:
                for k2, v2 in v.items():
                    settings[k][k2] = v2

    return settings

def dump_settings(dictionary, yaml_file):
    """
    Dump dictionary of settings to a yaml-file.
    """
    import yaml
    with open(yaml_file, 'w') as file:
        yaml.dump(dictionary, file)
