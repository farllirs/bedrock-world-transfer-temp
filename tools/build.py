import pickle,struct,collections,nbt,sub
d,seq=pickle.load(open('db.pkl','rb'))
ORG=(1951,62,1840)           # where structure cell (0,0,0) lands
BOX=(1951,1987,1840,1900)    # old almacen footprint
CLR_Y0,CLR_Y1=63,95
SX,SY,SZ=29,31,51
b=open('/mnt/user-data/uploads/almacen_salon.mcstructure','rb').read()
root=nbt.read(b); s=root['structure']
# raw palette entries
def find_spans(b):
    # re-parse to get list spans for block_palette
    o=0; t=b[o]; nl=struct.unpack_from('<H',b,o+1)[0]; o+=3+nl
    # walk top compound
    def walk(o,path):
        res=None
        while True:
            tt=b[o];o+=1
            if tt==0: return None,o
            n=struct.unpack_from('<H',b,o)[0];k=b[o+2:o+2+n].decode();o+=2+n
            v,e=nbt.pay(b,o,tt)
            if k=='structure' or k=='palette' or k=='default':
                pass
            o=e
        return
    return None
# simpler: parse and locate via custom descent
def descend(b):
    o=0;nl=struct.unpack_from('<H',b,1)[0];o=3+nl
    def entries(o):
        while True:
            tt=b[o];o+=1
            if tt==0:return
            n=struct.unpack_from('<H',b,o)[0];k=b[o+2:o+2+n].decode();o+=2+n
            st=o; v,e=nbt.pay(b,o,tt)
            yield k,tt,st,v,e; o=e
    for k,tt,st,v,e in entries(o):
        if k=='structure':
            for k2,tt2,st2,v2,e2 in entries(st):
                if k2=='palette':
                    for k3,tt3,st3,v3,e3 in entries(st2):
                        if k3=='default':
                            for k4,tt4,st4,v4,e4 in entries(st3):
                                if k4=='block_palette': return v4.spans
spans=descend(b)
pal_raw=[b'\x0a\x00\x00'+b[a:e] for a,e in spans]
pal_names=[nbt.read(r)['name'] for r in pal_raw]
assert len(pal_raw)==len(s['palette']['default']['block_palette'])
AIR=pal_names.index('minecraft:air')
bi=s['block_indices'][0]
# placements
place={}   # (X,Y,Z)->raw
for sx in range(SX):
  for sy in range(SY):
    for sz in range(SZ):
      pi=bi[sx*SY*SZ+sy*SZ+sz]
      if pi<0: continue
      X,Y,Z=ORG[0]+sx,ORG[1]+sy,ORG[2]+sz
      if pi==AIR and Y==ORG[1]: continue
      place[(X,Y,Z)]=pal_raw[pi]
print('placements',len(place))
# block entities from structure -> world
bpd=s['palette']['default']['block_position_data']
# raw spans of block_entity_data compounds
def ben_spans(b):
    # locate block_position_data compound and each entry's block_entity_data raw
    res={}
    o=0;nl=struct.unpack_from('<H',b,1)[0];o=3+nl
    def entries(o):
        while True:
            tt=b[o];o+=1
            if tt==0:return
            n=struct.unpack_from('<H',b,o)[0];k=b[o+2:o+2+n].decode();o+=2+n
            st=o; v,e=nbt.pay(b,o,tt)
            yield k,tt,st,e; o=e
    for k,tt,st,e in entries(o):
        if k=='structure':
            for k2,tt2,st2,e2 in entries(st):
                if k2=='palette':
                    for k3,tt3,st3,e3 in entries(st2):
                        if k3=='default':
                            for k4,tt4,st4,e4 in entries(st3):
                                if k4=='block_position_data':
                                    for k5,tt5,st5,e5 in entries(st4):
                                        for k6,tt6,st6,e6 in entries(st5):
                                            if k6=='block_entity_data': res[int(k5)]=b[st6:e6]
    return res
bes=ben_spans(b)
def patch(payload,vals):
    o=0;out=bytearray(payload)
    while True:
        tt=payload[o];o+=1
        if tt==0:break
        n=struct.unpack_from('<H',payload,o)[0];k=payload[o+2:o+2+n].decode();o+=2+n
        if k in vals and tt==3: struct.pack_into('<i',out,o,vals[k])
        _,o=nbt.pay(payload,o,tt)
    return bytes(out)
new_be=collections.defaultdict(list); chests=[]
for idx,raw in bes.items():
    sx=idx//(SY*SZ);sy=(idx//SZ)%SY;sz=idx%SZ
    X,Y,Z=ORG[0]+sx,ORG[1]+sy,ORG[2]+sz
    dd=nbt.read(b'\x0a\x00\x00'+raw)
    vals={'x':X,'y':Y,'z':Z}
    if 'pairx' in dd: vals['pairx']=dd['pairx']-1950+ORG[0]; vals['pairz']=dd['pairz']-1840+ORG[2]
    pr=patch(raw,vals)
    new_be[(X>>4,Z>>4)].append(b'\x0a\x00\x00'+pr)
    if dd['id']=='Chest': chests.append((X,Y,Z,vals.get('pairx'),vals.get('pairz')))
print('block entities',sum(len(v) for v in new_be.values()),'chests',len(chests))
# actors in region?
dig=[k for k in d if k.startswith(b'digp') and len(k)==12]
n=0
for k in dig:
    cx,cz=struct.unpack('<ii',k[4:12])
    if 121<=cx<=124 and 115<=cz<=118: n+=len(d[k])//8
print('actors in region chunks',n)
# edit chunks
air_raw=pal_raw[AIR]
touched=0; removed_be=0
for cx in range(121,125):
  for cz in range(115,119):
    subs={}
    for si in range(0,8):
        k=struct.pack('<ii',cx,cz)+bytes([47,si])
        if k in d: subs[si]=sub.parse(d[k])[1]
    cells=collections.defaultdict(dict)
    for (X,Y,Z),r in place.items():
        if X>>4==cx and Z>>4==cz: cells[Y>>4][(X&15)*256+(Z&15)*16+(Y&15)]=r
    for si in range(3,6):
        if si not in subs: subs[si]=[[[0]*4096,[air_raw]]]
        st=subs[si]
        for idx,pal in st:
            ai=next((i for i,r in enumerate(pal) if sub.name_of(r)=='minecraft:air'),None)
            if ai is None: pal.append(air_raw); ai=len(pal)-1
            for x in range(16):
              for z in range(16):
                X=cx*16+x;Z=cz*16+z
                if BOX[0]<=X<=BOX[1] and BOX[2]<=Z<=BOX[3]:
                  for y in range(16):
                    Y=si*16+y
                    if CLR_Y0<=Y<=CLR_Y1: idx[x*256+z*16+y]=ai
        idx,pal=st[0]
        pm={r:i for i,r in enumerate(pal)}
        for li,r in cells.get(si,{}).items():
            if r not in pm: pal.append(r); pm[r]=len(pal)-1
            idx[li]=pm[r]
        d[struct.pack('<ii',cx,cz)+bytes([47,si])]=sub.build(si,st); touched+=1
    # block entities
    k=struct.pack('<ii',cx,cz)+bytes([49])
    keep=[]
    if k in d:
        data=d[k];o=0
        while o<len(data):
            e=sub.skip_root(data,o);raw=data[o:e];o=e
            dd=nbt.read(raw)
            if BOX[0]<=dd['x']<=BOX[1] and BOX[2]<=dd['z']<=BOX[3] and dd['y']>=CLR_Y0: removed_be+=1
            else: keep.append(raw)
    allbe=keep+new_be.get((cx,cz),[])
    if allbe: d[k]=b''.join(allbe)
    elif k in d: del d[k]
print('subchunks rewritten',touched,'old block entities removed',removed_be)
pickle.dump((d,seq),open('db_new.pkl','wb'))
pickle.dump(chests,open('chests.pkl','wb'))
