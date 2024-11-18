from unicorn import *
from unicorn.x86_const import *
import lief
import capstone

libapp = open("libapp.so", "rb").read()
elf = lief.parse(libapp)
size = 0x40000

cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

start = 0x0001ba9b
end = 0x0001bba2

mu = Uc(UC_ARCH_X86, UC_MODE_64)
mu.mem_map(0, size)
mu.mem_write(0, libapp)

# stack
mu.mem_map(0x1000000, 0x2000, UC_PROT_ALL)
mu.reg_write(UC_X86_REG_RSP, 0x1000000)

# def hook_code(uc, address, size, user_data):
#     code = mu.mem_read(address, size)
#     for i in cs.disasm(code, address):
#         print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))
#         print("RSP: 0x%x" % mu.reg_read(UC_X86_REG_RSP))
#         # input()

#     pass
    
# mu.hook_add(UC_HOOK_CODE, hook_code)

mu.emu_start(start, end)

def dump_stack(uc: Uc, size=0x200):
    rsp = uc.reg_read(UC_X86_REG_RSP)
    dat = b''
    for i in range(0, size + 1, 8):
        # d = st.unpack('<Q', uc.mem_read(rsp + i, 8))[0]
        # print(f"0x{rsp + i:x}: 0x{d:016x}")
        dat += uc.mem_read(rsp + i, 8)
    print(dat)
    print(dat.decode())

dump_stack(mu)