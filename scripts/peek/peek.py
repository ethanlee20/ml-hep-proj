import sys
import traceback

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
    if type(sep) != list:
        s = s.split(sep)
    elif type(sep) == list:
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

def is_int(s:str):
    try: int(s)
    except: return False
    return True

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
        code = "data["
        for index, simple_cut in enumerate(self.simple_cuts):
            code += f"(data['{simple_cut.var}'] {simple_cut.kind} {simple_cut.val})"
            if index  < len(self.connectors):
                code += self.connectors[index]
        code += ']'

        print("DEBUG:", code)
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
        self.mutable_data = cut.apply(self.mutable_data)
        
    def print_cuts(self):
        for cut in self.cut_hist:
            print(cut.string)
        

class Command:
    def __init__(self, name, action):
        self.name = name
        self.action = action




class Command_Manager:
    def __init__(self):
        self.commands = []
    def add_command(self, name, action):
        c = Command(name, action)
        self.commands.append(c)
    def find_command(self, name):
        try:
            command = [i for i in self.commands if i.name == name][0]
            return command
        except IndexError: raise ValueError("Command not found.")
    def run_command(self, name, arg):
        try:
            command = self.find_command(name)
            if arg: command.action(arg)
            else: command.action()
        except:                
            print("something went wrong...")
            traceback.print_exc()


class Parser:

    def __init__(self):
        self.set_defaults()

    def set_defaults(self):
        self.command = ''
        self.arg = ''

    def get_command(self, user_input):
        self.command = user_input.split()[0]
        
    def get_arg(self, user_input):
        arg = ""
        arg = arg.join(user_input.split()[1:])
        arg = arg.strip()
        if is_int(arg): arg = int(arg)
        if arg == "": arg = None
        self.arg = arg

    def parse_user_input(self, user_input:str):
        try:
            self.get_command(user_input)
            self.get_arg(user_input)
        except:
            print("something went wrong...")
            traceback.print_exc()


class Prompt:
    def __init__(self):
        self.sym = '|>__<| '
        self.input = None

    def get_input(self):
        self.input = input(self.sym)


def main():

    prompt = Prompt()
    parser = Parser()
    dh = Data_Handler(sys.argv[1])
    cm = Command_Manager()

    cm.add_command(name='head', action=dh.head)
    cm.add_command(name='load', action=dh.load)
    cm.add_command(name='refresh_data', action=dh.refresh_data)
    cm.add_command(name='count', action=dh.count)
    cm.add_command(name='quit', action=quit)


    while True:
        prompt.get_input()
        parser.parse_user_input(prompt.input)
        
        cm.run_command(parser.command, parser.arg)



        # if parser.command == "load":
        #     try:dh.load(parser.arg)
        #     except:
        #         print("something went wrong...")
        #         traceback.print_exc()

        # if parser.command == "refresh_data":
        #     try:dh.refresh_data()
        #     except:
        #         print("something went wrong...")
        #         traceback.print_exc()
        
        # if parser.command == "cut":
        #     try:
        #         cut = Cut(parser.arg)
        #         dh.cut_data(cut)

        #     except:
        #         print("something went wrong...")
        #         traceback.print_exc()

        # if parser.command == "veto_q2":
        #     try:dh.mutable_data = veto_q_squared(dh.mutable_data)
        #     except:
        #         print("something went wrong...")
        #         traceback.print_exc()

        # if parser.command == "noise_only":
        #     try:dh.mutable_data = section(dh.mutable_data, sig_noise='noise')
        #     except:
        #         print("something went wrong...")
        #         traceback.print_exc()

        # if parser.command == "signal_only":
        #     try:dh.mutable_data = section(dh.mutable_data, sig_noise='sig')
        #     except:
        #         print("something went wrong...")
        #         traceback.print_exc()

        # if parser.command == "gen_only":
        #     try:dh.mutable_data = section(dh.mutable_data, gen_det='gen')
        #     except:
        #         print("something went wrong...")
        #         traceback.print_exc()

        # if parser.command == "det_only":
        #     try:dh.mutable_data = section(dh.mutable_data, gen_det='det')
        #     except:
        #         print("something went wrong...")
        #         traceback.print_exc()

        # if parser.command == "count":
        #     try:dh.count()
        #     except:
        #         print("something went wrong...")
        #         traceback.print_exc()

        # if parser.command == "head":
        #     try:dh.head(int(parser.arg))
        #     except:
        #         print("something went wrong...")
        #         traceback.print_exc()

        # if parser.command == "print_cuts":
        #     try:dh.print_cuts()
        #     except:
        #         print("something went wrong...")
        #         traceback.print_exc()
        
        # if parser.command == "quit":
        #     print("all systems shutting down. Bye bye!")
        #     quit()
        
        parser.set_defaults()


if __name__ == "__main__":
    main()

