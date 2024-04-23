
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


class Data_Handler:
    def load(self, path):
        self.original_data = open_data(path)
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

        if type(cut) == SimpleCut:
        elif type(cut) == CompoundCut:


        if lower_bound:
            self.mutable_data = self.mutable_data[self.mutable_data[var] > lower_bound]
        if upper_bound:
            self.mutable_data = self.mutable_data[self.mutable_data[var] < upper_bound]
        if equality:
            self.mutable_data = self.mutable_data[self.mutable_data[var] == equality]
        if inequality:
            self.mutable_data = self.mutable_data[self.mutable_data[var] != inequality]
            
    def refresh_data(self):
        self.mutable_data = self.original_data.copy()


# def find_all(a, l, start=0):
#     """
#     Find all occurances of substring a in string l.
#     Return a list of the indicies.
#     """
#     i_s = []
#     while True:
#         try:
#             i = l.index(a, start)
#             i_s.append(i)
#             start = i + len(a)
#         except ValueError:
#             return i_s


# def find_enums(p, l, inv=False):
#     """
#     Search through l for items in p.
#     Return the (index, item) of each found item in terms of its location in l.
#     """
#     enums = []
#     for i in range(len(l)):
#         if inv:
#             cond = l[i] not in p
#         else:
#             cond = l[i] in p
#         if cond:
#             enums.append((i, l[i]))
#     if enums == []:
#         raise ValueError(f"No (all) elements of list p found in list l.")
#     return enums


# def is_between(low, high, l):
#     """
#     Find the indicies of elements of list l greater than low and less than high.
#     Note: Assumes that l is sorted from low to high.
#     """
#     l_check = l.copy()
#     l_check.sort()
#     assert l_check == l, Exception("Unsorted list.") 

#     low_i = l.index(low)
#     high_i = l.index(high)
#     i = list(range(low_i+1, high_i))
#     return i

# def is_greater_than(low, l):
#     """
#     Find the indicies of elements of list l greater than low.
#     Note: Assumes that l is sorted from low to high.
#     """
#     l_check = l.copy()
#     l_check.sort()
#     assert l_check == l, Exception("Unsorted list.") 

#     low_i = l.index(low)
#     i = list(range(low_i+1, len(l)))
#     return i


# def group_enum_between(p, l):
#     """
#     Group enumerations in p with the nearest lower enumeration in l.
#     Example p: [(1, 'a'), (3, 'b')], l: [(0, 'c'), (2, 'd')] -> [((0, 'c'), [(1, 'a')]), ((2, 'd'), [(3, 'b')])] 
#     """
#     l_n, l_v = zip(*l)

#     groups = []
#     last_i = len(l) - 1
#     for i in range(len(l)):
#         if i != last_i:
#             up_n = l_n[i+1]
#             low_n = l_n[i]
#             p_group_i = is_between(low_n, up_n, p)
#         else:
#             low_n = l_n[i]
#             p_group_i = is_greater_than(low_n, p)
#         p_group = [p[i] for i in p_group_i]
#         groups.append((l[i], p_group))
    
#     return groups





class SimpleCut:
    def __init__(self, var, val, kind):
        self.var = var
        self.val = val
        self.kind = kind

class CompoundCut: 
    def __init__(self, simple_cuts, connectors):
        self.simple_cuts = simple_cuts
        self.connectors = connectors


def parse_simple_cut(cut_string):
    known_syms = [
        '>',
        '<',
        '>=',
        '<=',
        '==',
        '!=',
    ]
    for sym in known_syms:
        if sym in cut_string:
            s = split_and_strip(cut_string, sep=sym)
            assert len(s) == 2
            cut = SimpleCut(var=s[0], val=s[1], kind=sym)
            return cut


def parse_compound_cut(cut_string):
    delims = [
        '[',
        ']'
    ]

    connect = [
        '&',
        '|',
        '&~',
        '|~',
    ]

    cut_string = split_and_strip(cut_string, sep=delims)
    
    assert odd(len(cut_string)), ValueError
    assert len(cut_string) > 1, ValueError

    connectors = cut_string[1::2]
    simple_cuts = [parse_simple_cut(i) for i in cut_string[0::2]]

    cut = CompoundCut(simple_cuts=simple_cuts, connectors=connectors)
    return cut


def parse_cut_string(cut_string):
    try: cut = parse_compound_cut(cut_string)
    except ValueError: cut = parse_simple_cut(cut_string)
    return cut
        





class Parser:

    def __init__(self):
        self.set_defaults()

    def set_defaults(self):
        self.command = None
        self.arg = None
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
    
    sym = '|>__<| '
    
    def get_cmd(self):
        self.cmd = input(self.sym)


def main():

    prompt = Prompt()
    parser = Parser()
    dh = Data_Handler()

    run = True

    while run:
        prompt.get_cmd()
        try: parser.parse_user_input(prompt.cmd)
        except Exception as err: print(f"Something went wrong... {err}")

        if parser.command == "load":
            dh.load(parser.arg)

        if parser.command == "refresh_data":
            dh.refresh_data()
        
        if parser.command == "cut":
            dh.cut_data(
                parser.cut_var, 
                lower_bound=parser.cut_low_bound,
                upper_bound=parser.cut_up_bound,
                equality=parser.cut_equality,
                inequality=parser.cut_inequality
            )
        if parser.veto_q2:
            dh.mutable_data = veto_q_squared(
                dh.mutable_data
            )
        if parser.noise_only:
            dh.mutable_data = section(dh.mutable_data, sig_noise='noise')
        if parser.signal_only:
            dh.mutable_data = section(dh.mutable_data, sig_noise='sig')
        if parser.gen_only:
            dh.mutable_data = section(dh.mutable_data, gen_det='gen')
        if parser.det_only:
            dh.mutable_data = section(dh.mutable_data, gen_det='det')

        if parser.print_count:
            dh.count()
        if parser.print_head:
            dh.head(parser.num_ex)
        
        if parser.quit:
            print("all systems shutting down. Bye bye!")
            quit()
        
        parser.set_defaults()


if __name__ == "__main__":
    main()

