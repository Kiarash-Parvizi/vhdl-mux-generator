from typing import Tuple

# 
vhdl_input_signal_template = '''\
        inp_%i : in std_logic_vector(n-1 downto 0);
'''

vhdl_header_template = '''\
library ieee;
use ieee.std_logic_1164.all;
 
entity mux_%i is
    generic(n: natural);
    port(
%s
        sel: in std_logic_vector(%i downto 0);
        dataout: out std_logic_vector(n-1 downto 0)
    );
end entity;

'''
vhdl_architecture_template = '''
architecture bhv of mux_%i is
begin
process(%s) is
begin
%s
end process;
end architecture bhv;

'''

def generate_inps(sel_size: int) -> Tuple[str, str]:
    if sel_size < 1:
        return ('','')
    vec_size = 2**sel_size
    names, signals = '', ''
    # iter
    for i in range(0, vec_size):
        names   += 'inp_%i,'%(i)
        signals += vhdl_input_signal_template%(i)
    # return
    return (names, signals)

def generate_ifs(sel_size: int) -> str:
    if sel_size < 1:
        return ''
    vec_size = 2**sel_size
    res = 'if(sel = \"%s\") then\n'%format(0, '0%ib'%sel_size) +\
        '\tdataout <= inp_%i;\n'%0
    # iter
    for i in range(1, vec_size):
        res += 'elsif(sel = \"%s\") then\n'%format(i, '0%ib'%sel_size) +\
        '\tdataout <= inp_%i;\n'%i
    res += 'end if;\n'
    # return
    return res

import sys

def main(argv):
    sel_size = None
    try:
        sel_size = int(argv[0])
    except IndexError as err:
        print('usage:\npython3 generate_mux.py <mux_sel_size>')
        print('example:\npython3 generate_mux.py 4\n')
        sys.exit(2)
    except ValueError:
        print('Please enter an integer for [mux_sel_size]')
        sys.exit(2)
    output_file = 'mux_%i.vhd'%(sel_size)
    # generate mux-code
    inps = generate_inps(sel_size)
    ifs  =  generate_ifs(sel_size)
    mux_code = vhdl_header_template % (sel_size, inps[1], sel_size-1) +\
    vhdl_architecture_template % (sel_size, inps[0]+'sel', ifs)
    # write to file
    with open(output_file, 'w') as outfile:
        outfile.write(mux_code)
    print('written to: ' + output_file)

if __name__ == '__main__':
    main(sys.argv[1:])
