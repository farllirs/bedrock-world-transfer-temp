import struct
class L(list): pass
def read(b, off=0):
    t=b[off]; off+=1
    n=struct.unpack_from('<H',b,off)[0]; off+=2+n
    v,off=pay(b,off,t); return v
def pay(b,o,t):
    if t==1: return b[o],o+1
    if t==2: return struct.unpack_from('<h',b,o)[0],o+2
    if t==3: return struct.unpack_from('<i',b,o)[0],o+4
    if t==4: return struct.unpack_from('<q',b,o)[0],o+8
    if t==5: return struct.unpack_from('<f',b,o)[0],o+4
    if t==6: return struct.unpack_from('<d',b,o)[0],o+8
    if t==7:
        n=struct.unpack_from('<i',b,o)[0]; return b[o+4:o+4+n],o+4+n
    if t==8:
        n=struct.unpack_from('<H',b,o)[0]; return b[o+2:o+2+n].decode('utf8','replace'),o+2+n
    if t==9:
        it=b[o]; n=struct.unpack_from('<i',b,o+1)[0]; o+=5; l=L(); l.spans=[]
        for _ in range(n):
            st=o; v,o=pay(b,o,it); l.append(v); l.spans.append((st,o))
        return l,o
    if t==10:
        d={}
        while True:
            tt=b[o]; o+=1
            if tt==0: return d,o
            n=struct.unpack_from('<H',b,o)[0]; k=b[o+2:o+2+n].decode(); o+=2+n
            d[k],o=pay(b,o,tt)
    if t==11:
        n=struct.unpack_from('<i',b,o)[0]; return list(struct.unpack_from('<%di'%n,b,o+4)),o+4+4*n
    if t==12:
        n=struct.unpack_from('<i',b,o)[0]; return list(struct.unpack_from('<%dq'%n,b,o+4)),o+4+8*n
