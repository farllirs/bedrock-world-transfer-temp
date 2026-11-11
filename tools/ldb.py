import struct, zlib, ctypes, os, glob
try:
    import snappy_py
except ImportError:
    snappy_py = None
try:
    snap = ctypes.CDLL('libsnappy.so.1')
except OSError:
    snap = None
def snappy_unc(b):
    if snap is None:
        if snappy_py is None:
            raise RuntimeError('falta snappy: instala libsnappy o tools/snappy_py.py')
        return snappy_py.uncompress(b)
    n=ctypes.c_size_t(0)
    snap.snappy_uncompressed_length(b,len(b),ctypes.byref(n))
    out=ctypes.create_string_buffer(n.value); m=ctypes.c_size_t(n.value)
    assert snap.snappy_uncompress(b,len(b),out,ctypes.byref(m))==0
    return out.raw[:m.value]
def varint(b,o):
    r=0;s=0
    while True:
        c=b[o];o+=1;r|=(c&127)<<s
        if c<128: return r,o
        s+=7
def unblock(data,type_):
    if type_==0: return data
    if type_==1: return snappy_unc(data)
    if type_ in (2,4):
        try: return zlib.decompress(data,-15)
        except Exception: return zlib.decompress(data)
    raise Exception('ctype %d'%type_)
def readblock(f,off,size):
    f.seek(off); d=f.read(size+5)
    return unblock(d[:size],d[size])
def block_entries(blk):
    nr=struct.unpack_from('<I',blk,len(blk)-4)[0]
    end=len(blk)-4-4*nr
    o=0;key=b''
    while o<end:
        sh,o=varint(blk,o); ns,o=varint(blk,o); vl,o=varint(blk,o)
        key=key[:sh]+blk[o:o+ns]; o+=ns
        yield key,blk[o:o+vl]; o+=vl
def read_sst(path):
    with open(path,'rb') as f:
        f.seek(-48,2); ft=f.read(48)
        o=0
        _,o=varint(ft,o);_,o=varint(ft,o)
        io,o=varint(ft,o);isz,o=varint(ft,o)
        idx=readblock(f,io,isz)
        for k,v in block_entries(idx):
            bo,p=varint(v,0);bs,p=varint(v,p)
            for ik,val in block_entries(readblock(f,bo,bs)):
                yield ik,val
def read_log(path):
    d=open(path,'rb').read()
    o=0;buf=b''
    while o+7<=len(d):
        # blocks of 32768
        bo=o%32768
        if 32768-bo<7: o+=32768-bo; continue
        crc,ln,t=struct.unpack_from('<IHB',d,o); o+=7
        if t==0 and ln==0: o=(o//32768+1)*32768; continue
        data=d[o:o+ln]; o+=ln
        if t==1: yield data
        elif t==2: buf=data
        elif t==3: buf+=data
        elif t==4: buf+=data; yield buf; buf=b''
def batch_entries(rec):
    seq,cnt=struct.unpack_from('<QI',rec,0); o=12
    for i in range(cnt):
        t=rec[o];o+=1
        kl,o=varint(rec,o);k=rec[o:o+kl];o+=kl
        if t==1:
            vl,o=varint(rec,o);v=rec[o:o+vl];o+=vl
            yield seq+i,k,v
        else: yield seq+i,k,None
def load(db):
    live={}  # key -> (seq,val)
    def put(s,k,v):
        c=live.get(k)
        if c is None or c[0]<s: live[k]=(s,v)
    for p in sorted(glob.glob(db+'/*.ldb')):
        for ik,v in read_sst(p):
            tag=struct.unpack('<Q',ik[-8:])[0]
            put(tag>>8,ik[:-8],v if (tag&0xff)==1 else None)
    for p in sorted(glob.glob(db+'/*.log')):
        for rec in read_log(p):
            for s,k,v in batch_entries(rec): put(s,k,v)
    return {k:v[1] for k,v in live.items() if v[1] is not None}, max(v[0] for v in live.values())
