
import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util import open_data, section, veto_q_squared


def remove_all(a, l):
    """Remove all occurances of a from list l."""
    while True:
        try: l.remove(a)
        except ValueError: return l


def flatten2d(l):
    """Flatten a 2d array to 1d."""
    i = []
    for a in l:
        for b in a:
            i.append(b)
    return i


def split_and_strip(s, sep):
    """Split string s on the given separators and clean result."""
    if type(s) != list:
        s = s.split(sep)
    elif type(s) == list:
        s = s.split(sep[0])
        if len(sep) > 1:
            for p in sep[1:]:
                s = [i.split(p) for i in s]
                s = flatten2d(s)
    s = [i.strip() for i in s]
    s = remove_all('', s)
    return s


def odd(a:int):
    return (a % 2) == 1


class SimpleCut:
    def __init__(self, string):
        self.string = string
        self.var, self.val, self.kind = self.parse()
    def parse(self):
        known_syms = [
            '<=',
            '>=',
            '==',
            '!=',
            '>',
            '<',
        ]
        for sym in known_syms:
            if sym in self.string:
                s = split_and_strip(self.string, sep=sym)
                assert len(s) == 2
                var=s[0]
                val=s[1]
                kind=sym
                return var, val, kind
        raise ValueError(f"Cut not recognized: {self.string}")


class Cut: 
    def __init__(self, string):
        self.string = string
        self.simple_cuts, self.connectors = self.parse()
    def parse(self):
        delims = [
            '[',
            ']'
        ]
        known_connectors = [
            '|~',
            '&~',
            '&',
            '|',
        ]
        s = split_and_strip(self.string, sep=delims)
        simple_cuts = [SimpleCut(i) for i in s[0::2]]
        
        assert odd(len(s)), ValueError
        try: connectors = s[1::2]
        except: connectors = []
        for c in connectors: 
            assert c in known_connectors, ValueError(f"Cut not recognized: {self.string}")

        return simple_cuts, connectors
    
    def apply(self, data):
        code = ""
        for simple_cut, index in enumerate(self.simple_cuts):
            code = code.join(f"(data[data[{simple_cut.var}] {simple_cut.kind} {simple_cut.val}])")
            if index  < len(self.connectors):
                code = code.join(self.connectors[index])
        data = eval(code)
        return data


class Data_Handler:

    def __init__(self, data_path):
        self.load(data_path)
        self.cut_hist = []

    def load(self, path):
        self.original_data = open_data(path)
        self.mutable_data = self.original_data.copy()
    
    def refresh_data(self):
        self.cut_hist = []
        self.mutable_data = self.original_data.copy()

    def head(self, num_ex):
        print(self.mutable_data.head(num_ex))

    def count(self):
        try:
            print("num gen", len(section(self.mutable_data, gen_det='gen')))
        except KeyError as err: print("no gen events?", err)
        try:
            print("num gen sig", len(section(self.mutable_data, gen_det='gen', sig_noise='sig')))
        except KeyError as err: print("no gen sig events?", err)
        try:
            print("num det sig", len(section(self.mutable_data, sig_noise='sig', gen_det='det')))
        except KeyError as err: print("no detector signal events?", err)
        print("num det noise", len(section(self.mutable_data, gen_det='det', sig_noise='noise')))
        print("num det tot", len(section(self.mutable_data, gen_det='det')))

    def cut_data(self, cut):
        self.cut_hist.append(cut)
        self.mutable_data = self.cut.apply(self.mutable_data)
        
    def print_cuts(self):
        for cut in self.cut_hist:
            print(cut.cut_str)
        


class Parser:

    def __init__(self):
        self.set_defaults()
        self.known_commands = [
            'cut',
            'head',
            'count',
            'quit',
            'load',
            'veto_q2',
            'refresh_data',
            'noise_only',
            'signal_only',
            'gen_only',
            'det_only',
        ]

    def set_defaults(self):
        self.command = None
        self.arg = None

    def get_command(self, user_input):
        command = user_input.split()[0]
        assert command in self.known_commands
        self.command = command
        
    def get_arg(self, user_input):
        arg = ""
        arg.join(user_input.split()[1:])
        arg = arg.strip()
        self.arg = arg

    def parse_user_input(self, user_input:str):
        self.get_command(user_input)
        self.get_arg(user_input)


class Prompt:
    def __init__(self):
        self.sym = '|>__<| '
        self.cmd = None

    def get_cmd(self):
        self.cmd = input(self.sym)


def main():

    prompt = Prompt()
    parser = Parser()
    dh = Data_Handler()

    while True:
        prompt.get_cmd()
        try: parser.parse_user_input(prompt.cmd)
        except Exception as err: print(f"Something went wrong... {err}")

        if parser.command == "load":
            dh.load(parser.arg)

        if parser.command == "refresh_data":
            dh.refresh_data()
        
        if parser.command == "cut":
            dh.cut_data(parser.arg)
        if parser.command == "veto_q2":
            dh.mutable_data = veto_q_squared(
                dh.mutable_data
            )
        if parser.command == "noise_only":
            dh.mutable_data = section(dh.mutable_data, sig_noise='noise')
        if parser.command == "signal_only":
            dh.mutable_data = section(dh.mutable_data, sig_noise='sig')
        if parser.command == "gen_only":
            dh.mutable_data = section(dh.mutable_data, gen_det='gen')
        if parser.command == "det_only":
            dh.mutable_data = section(dh.mutable_data, gen_det='det')

        if parser.command == "print_count":
            dh.count()
        if parser.command == "print_head":
            dh.head(parser.arg)
        
        if parser.quit:
            print("all systems shutting down. Bye bye!")
            quit()
        
        parser.set_defaults()


if __name__ == "__main__":
    main()

