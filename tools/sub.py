import struct, nbt
def skip_root(b,o):
    nl=struct.unpack_from('<H',b,o+1)[0]
    _,e=nbt.pay(b,o+3+nl,10); return e
def parse(b):
    v=b[0]; assert v in(8,9); ns=b[1]; o=2; yi=None
    if v==9: yi=struct.unpack_from('<b',b,o)[0]; o+=1
    st=[]
    for _ in range(ns):
        h=b[o];o+=1;bpb=h>>1
        if bpb==0: idx=[0]*4096
        else:
            per=32//bpb;nw=-(-4096//per)
            w=struct.unpack_from('<%dI'%nw,b,o);o+=4*nw
            m=(1<<bpb)-1;idx=[]
            for x in w:
                for j in range(per): idx.append((x>>(j*bpb))&m)
            idx=idx[:4096]
        pc=struct.unpack_from('<i',b,o)[0];o+=4;pal=[]
        for _ in range(pc):
            e=skip_root(b,o);pal.append(b[o:e]);o=e
        st.append([idx,pal])
    assert o==len(b),(o,len(b))
    return yi,st
def name_of(raw): return nbt.read(raw)['name']
def pack(idx,npal):
    bpb=next(x for x in (1,2,3,4,5,6,8,16) if (1<<x)>=max(npal,2))
    per=32//bpb;nw=-(-4096//per);out=[]
    for w in range(nw):
        v=0
        for j in range(per):
            i=w*per+j
            if i<4096: v|=idx[i]<<(j*bpb)
        out.append(v)
    return bytes([bpb<<1])+struct.pack('<%dI'%nw,*out)
def build(yi,st):
    out=bytearray([9,len(st)])+struct.pack('<b',yi)
    for idx,pal in st:
        used=sorted(set(idx)); mp={u:i for i,u in enumerate(used)}
        nidx=[mp[i] for i in idx]; npal=[pal[u] for u in used]
        out+=pack(nidx,len(npal))+struct.pack('<i',len(npal))
        for r in npal: out+=r
    return bytes(out)
