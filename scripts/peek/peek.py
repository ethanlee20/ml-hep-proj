
import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util import open_data, section, veto_q_squared


# parser.add_argument("--veto_q2", action='store_true', help="veto out J/Psi and Psi(2S) regions of q squared")

# parser.add_argument("-n", "--noise_only", action='store_true', help="only include noise events")
# parser.add_argument("-s", "--sig_only", action='store_true', help="only include signal events")
# parser.add_argument("-g", '--gen_only', action='store_true', help="only include generator level data")
# parser.add_argument("-d",'--det_only', action='store_true', help="only include detector level data")


# parser.add_argument("--cut_var", help="variable to cut on")
# parser.add_argument("--lower_bound", help="lower bound for cut", type=float)
# parser.add_argument("--upper_bound", help="upper bound for cut", type=float)
# parser.add_argument("--equal_to", help="equality to cut on", type=float)
# parser.add_argument("--not_equal_to", help="inequality to cut on", type=float)



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

    def cut_data(self, var, lower_bound=None, upper_bound=None, equality=None, inequality=None):
        assert (bool(lower_bound) | bool(upper_bound)) ^ (bool(equality) | bool(inequality))
        assert ~(bool(equality) & bool(inequality))

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


def find_enums(p, l, inv=False):
    """Find the enumeration (element, index) of each element of list l (not) included in list p."""
    enums = []
    for i in range(len(l)):
        if inv:
            cond = l[i] not in p
        cond = l[i] in p
        if cond:
            enums.append((i, l[i]))
    if enums == []:
        raise ValueError(f"No (all) elements of list p found in list l.")
    return enums


def is_between(low, high, l):
    """
    Find the indicies of elements of list l greater than low and less than high.
    Note: Assumes that l is sorted from low to high.
    """
    l_check = l.copy()
    l_check.sort()
    assert l_check == l, Exception("Unsorted list.") 

    low_i = l.index(low)
    high_i = l.index(high)
    i = list(range(low_i+1, high_i))
    return i

def is_greater_than(low, l):
    """
    Find the indicies of elements of list l greater than low.
    Note: Assumes that l is sorted from low to high.
    """
    l_check = l.copy()
    l_check.sort()
    assert l_check == l, Exception("Unsorted list.") 

    low_i = l.index(low)
    i = list(range(low_i+1, len(l)))
    return i


def group_enum_between(p, l):
    """
    Group enumerations in p with the nearest lower enumeration in l.
    Example p: [(1, 'a'), (3, 'b')], l: [(0, 'c'), (2, 'd')] -> [((0, 'c'), [(1, 'a')]), ((2, 'd'), [(3, 'b')])] 
    """
    l_n, l_v = zip(*l)

    groups = []
    last_i = len(l) - 1
    for i in range(len(l)):
        if i != last_i:
            up_n = l_n[i+1]
            low_n = l_n[i]
            p_group_i = is_between(low_n, up_n, p)
        else:
            low_n = l_n[i]
            p_group_i = is_greater_than(low_n, p)
        p_group = [p[i] for i in p_group_i]
        groups.append((l[i], p_group))
    
    return groups


class Parser:

    def __init__(self):
        self.set_defaults()

    def set_defaults(self):
        self.tokens = None
        self.commands = []
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
        self.load = False
        self.path = None
        self.num_ex = 5
        self.veto_q2 = False
        self.noise_only = False
        self.signal_only = False
        self.gen_only = False
        self.det_only = False
        self.cut = False
        self.print_head = False
        self.print_count = False
        self.refresh_data = False
        self.quit = False


    

    def get_user_input(self, user_input):
        self.tokens = user_input.split()

    def get_commands(self):
        self.commands = find_enums(self.known_commands, self.tokens)

    def get_args(self):
        self.args = find_enums(self.known_commands, self.tokens, inv=True)
    
    def link_commands_args(self):

        grouped = group_enum_between(self.args, self.commands)
        cmd_idxs, cmds = zip(*self.commands)
        arg_idxs, args = zip(*self.args)
        for cmd_idx in cmd_idxs:


        for i in range(len(self.commands)):
            cmd_idx = self.commands[i][0]
            next_cmd_idx = self.commands[i+1][0]


        for cmd, cmd_idx in self.commands:
            

    def get_opt_args(self, cmd_idx):

    def parse_user_input(self):

        for cmd, cmd_idx in self.commands:
            if cmd == "load":
                self.load = True
                self.path = self.get_pos_arg(cmd_idx, 1)
            if cmd == "head":
                self.print_head = True

            if "num_ex" in tokens:
                num_ex_idx = tokens.index("num_ex") + 1 
                self.num_ex = int(tokens[num_ex_idx])

        if "count" in tokens:
            self.print_count = True
        
        if "cut" in tokens:
            assert "var" in tokens
            self.cut = True
            
            cut_var_idx = tokens.index("var") + 1
            self.cut_var = tokens[cut_var_idx]

            try: 
                cut_low_bound_idx = tokens.index("lower_bound") + 1
                self.cut_low_bound = float(tokens[cut_low_bound_idx])
            except ValueError: self.cut_low_bound = None            
            
            try: 
                cut_up_bound_idx = tokens.index("upper_bound") + 1
                self.cut_up_bound = float(tokens[cut_up_bound_idx])
            except ValueError: self.cut_up_bound = None
            
            try: 
                cut_equality_idx = tokens.index("equal_to") + 1
                self.cut_equality = float(tokens[cut_equality_idx])
            except ValueError: self.cut_equality = None
            
            try: 
                cut_inequality_idx = tokens.index("not_equal_to") + 1
                self.cut_inequality = float(tokens[cut_inequality_idx])
            except ValueError: self.cut_inequality = None
            

        if "refresh_data" in tokens:
            self.refresh_data = True

        if "veto_q2" in tokens:
            self.veto_q2 = True

        if "noise_only" in tokens:
            self.noise_only = True
        
        if "signal_only" in tokens:
            self.signal_only = True
        
        if "gen_only" in tokens:
            self.gen_only = True
        
        if "det_only" in tokens:
            self.det_only = True     

        if "quit" in tokens:
            self.quit = True



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
        parser.parse_user_input(prompt.cmd)

        if parser.load:
            dh.load(parser.path)

        if parser.refresh_data:
            dh.refresh_data()
        
        if parser.cut:
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

