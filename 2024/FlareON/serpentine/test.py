def get_offsets(regs):
    regs = dict([line.split(' : ') for line in regs.split('\n')])
    regs = {k.strip(): int(v, 16) for k, v in regs.items()}
    # print(regs)

    # if not 0 or 0x100000 or rax or rip, get offset from r9
    base = regs['R9']
    # print(base)

    offsets = { reg: regs[reg] - base for reg in regs if reg not in ['RIP', 'RAX', 'RBX', 'RDI', 'R10', 'R11', 'R12', 'R14'] }
    print({k: hex(v) for k, v in offsets.items()})

regs = '''RAX : 00000000069F0098
RBX : 0000000000000000
RCX : 00000000067FFC70
RDX : 00000000067FFEA8
RBP : 00000000067FF590
RSP : 00000000067FEFF8
RSI : 00000000067FFC70
RDI : 0000000000000000
R8  : 00000000067FF780
R9  : 00000000067FF5E0
R10 : 0000000000000000
R11 : 0000000000100000
R12 : 0000000000000000
R13 : 00000000067FF090
R14 : 0000000000000000
R15 : 00000000067FF780'''
get_offsets(regs)

regs = '''RAX : 00000000069F01A7
RBX : 0000000000000000
RCX : 00000000067FEDB0
RDX : 00000000067FEFD8
RBP : 00000000067FE6D0
RSP : 00000000067FE138
RSI : 00000000067FEDB0
RDI : 0000000000000000
R8  : 00000000067FE8C0
R9  : 00000000067FE720
R10 : 0000000000000000
R11 : 0000000000100000
R12 : 0000000000000000
R13 : 00000000067FE1D0
R14 : 0000000000000000
R15 : 00000000067FE8C0'''
get_offsets(regs)

regs = '''RAX : 00000000069F02A2
RBX : 0000000000000000
RCX : 00000000067FDEF0
RDX : 00000000067FE138
RBP : 00000000067FD810
RSP : 00000000067FD278
RSI : 00000000067FDEF0
RDI : 0000000000000000
R8  : 00000000067FDA00
R9  : 00000000067FD860
R10 : 0000000000000000
R11 : 0000000000100000
R12 : 0000000000000000
R13 : 00000000067FD310
R14 : 0000000000000000
R15 : 00000000067FDA00'''
get_offsets(regs)

regs = '''RAX : 00000000069F04A9
RBX : 0000000000000000
RCX : 00000000067FC170
RDX : 00000000067FC3B0
RBP : 00000000067FBA90
RSP : 00000000067FB4F8
RSI : 00000000067FC170
RDI : 0000000000000000
R8  : 00000000067FBC80
R9  : 00000000067FBAE0
R10 : 0000000000000000
R11 : 0000000000100000
R12 : 0000000000000000
R13 : 00000000067FB590
R14 : 0000000000000000
R15 : 00000000067FBC80'''
get_offsets(regs)

x = '''00000000067FFEA8
00000000067FEFF8
00000000067FEFD8
00000000067FE138
00000000067FD278
00000000067FC3B8'''
x = [int(i, 16) for i in x.split('\n')]
for i in range(len(x)-1):
    print(hex(x[i+1] - x[i]))   