import pickle,struct,zlib,ctypes,os,shutil,nbt
d,seq=pickle.load(open('db_new.pkl','rb'))
# drop the 4 loose oak plank items from old floor
for k in list(d):
    if k.startswith(b'digp') and len(k)==12:
        cx,cz=struct.unpack('<ii',k[4:12])
        if 121<=cx<=124 and 115<=cz<=118:
            keep=b''
            for i in range(0,len(d[k]),8):
                ak=b'actorprefix'+d[k][i:i+8]
                e=nbt.read(d[ak]) if ak in d else None
                if e and e.get('identifier')=='minecraft:item': del d[ak]
                else: keep+=d[k][i:i+8]
            d[k]=keep
crc=ctypes.CDLL('./libcrc.so'); crc.crc32c.restype=ctypes.c_uint32; crc.crc32c.argtypes=[ctypes.c_char_p,ctypes.c_size_t]
def mask(c): return ((((c>>15)|(c<<17))&0xffffffff)+0xa282ead8)&0xffffffff
def vi(n):
    o=bytearray()
    while n>=128: o.append((n&127)|128); n>>=7
    o.append(n); return bytes(o)
class BB:
    def __init__(s): s.buf=bytearray(); s.rs=[0]; s.last=b''; s.n=0
    def add(s,k,v):
        if s.n%16==0:
            if s.n: s.rs.append(len(s.buf))
            sh=0
        else:
            sh=0
            m=min(len(s.last),len(k))
            while sh<m and s.last[sh]==k[sh]: sh+=1
        s.buf+=vi(sh)+vi(len(k)-sh)+vi(len(v))+k[sh:]+v; s.last=k; s.n+=1
    def size(s): return len(s.buf)+4*len(s.rs)+4
    def finish(s):
        return bytes(s.buf)+b''.join(struct.pack('<I',r) for r in s.rs)+struct.pack('<I',len(s.rs))
def trailer(data,ct): return bytes([ct])+struct.pack('<I',mask(crc.crc32c(data+bytes([ct]),len(data)+1)))
def wblock(f,raw,compress=True):
    off=f.tell()
    if compress:
        c=zlib.compressobj(6,zlib.DEFLATED,-15); z=c.compress(raw)+c.flush()
        if len(z)<len(raw): f.write(z+trailer(z,4)); return off,len(z)
    f.write(raw+trailer(raw,0)); return off,len(raw)
OUT='newdb'; shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
items=sorted(d.items())
files=[]; num=13800
i=0; N=len(items)
while i<N:
    path='%s/%06d.ldb'%(OUT,num); f=open(path,'wb'); idx=BB(); db=BB(); first=None; last=None
    while i<N and f.tell()<2*1024*1024:
        while i<N and db.size()<4096:
            k,v=items[i]; ik=k+struct.pack('<Q',(seq<<8)|1)
            if first is None: first=ik
            db.add(ik,v); last=ik; i+=1
        off,sz=wblock(f,db.finish()); idx.add(last,vi(off)+vi(sz)); db=BB()
    mo=wblock(f,BB().finish(),False)
    # metaindex: empty block
    ioff,isz=wblock(f,idx.finish(),False)
    ft=vi(mo[0])+vi(mo[1])+vi(ioff)+vi(isz); ft=ft+b'\0'*(40-len(ft))+struct.pack('<Q',0xdb4775248b80fb57)
    f.write(ft); size=f.tell(); f.close()
    files.append((num,size,first,last)); num+=1
# manifest
ve=vi(1)+vi(len(b'leveldb.BytewiseComparator'))+b'leveldb.BytewiseComparator'
ve+=vi(2)+vi(13791)+vi(9)+vi(0)+vi(3)+vi(13900)+vi(4)+vi(seq)
for n,sz,a,z in files: ve+=vi(7)+vi(3)+vi(n)+vi(sz)+vi(len(a))+a+vi(len(z))+z
assert len(ve)<32000
rec=struct.pack('<IHB',mask(crc.crc32c(b'\x01'+ve,len(ve)+1)),len(ve),1)+ve
open(OUT+'/MANIFEST-013790','wb').write(rec)
open(OUT+'/CURRENT','wb').write(b'MANIFEST-013790\n')
print(len(files),'tables',sum(f[1] for f in files)//1024//1024,'MB', len(items),'keys')
