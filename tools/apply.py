import pickle,struct,re,math,collections,csv,nbt,sub,model
a=pickle.load(open('final_db.pkl','rb')); seq=3025429
signs,frames,chests=pickle.load(open('cat.pkl','rb'))
cmap={(c[0],c[1],c[2]):c for c in chests}
pairs=set()
for (x,y,z),c in cmap.items():
    if c[3] is not None: pairs.add(tuple(sorted([(x,y,z),(c[3],y,c[4])])))
pairs=sorted(pairs)
P={}   # pair -> dict(frame,item)
for f in frames:
    fx,fy,fz=f[:3]
    p=next(p for p in pairs if p[0][1]==fy and any(abs(c[0]-fx)+abs(c[2]-fz)==1 for c in p))
    m=re.search(r"'Name': '([^']+)'",f[3])
    P[p]=dict(frame=(fx,fy,fz),item=m.group(1).replace('minecraft:','') if m else None,new=False)
cen=lambda p:((p[0][0]+p[1][0])/2,p[0][1],(p[0][2]+p[1][2])/2)
def dist(p,q):
    a_,b_=cen(p),cen(q); return math.hypot(a_[0]-b_[0],a_[2]-b_[2])+0.3*abs(a_[1]-b_[1])
floor=lambda p:0 if p[0][1]<66 else 1
empty=set(p for p in P if P[p]['item'] is None)
byitem=collections.defaultdict(list)
for p,v in P.items():
    if v['item']: byitem[v['item']].append(p)
def take_empty(anchor):
    c=[p for p in empty if floor(p)==floor(anchor)] or list(empty)
    if not c: return None
    q=min(c,key=lambda p:dist(p,anchor)); empty.discard(q); return q
sections=collections.defaultdict(list)   # item -> pairs
for it,ps in list(byitem.items()):
    need=min(8,max(1,math.ceil(model.qty(it)/(54*model.stack(it)))))
    ps=list(ps)
    while len(ps)<need:
        q=take_empty(ps[0])
        if q is None: break
        P[q]['item']=it;P[q]['new']=True; ps.append(q)
    sections[it]=ps
EXTRA=[('oak_planks','oak_log'),('spruce_planks','spruce_log'),('birch_planks','birch_log'),('jungle_planks','jungle_log'),('acacia_planks','acacia_log'),
 ('dark_oak_planks','dark_oak_log'),('cherry_planks','cherry_log'),('mangrove_planks','mangrove_log'),('pale_oak_planks','pale_oak_log'),('bamboo_planks','bamboo'),
 ('crimson_planks','crimson_stem'),('warped_planks','warped_stem'),('dirt','gravel'),('cobbled_deepslate','deepslate'),('cooked_porkchop','porkchop'),('baked_potato','potato'),
 ('diamond_pickaxe','diamond_axe'),('diamond_chestplate','diamond_helmet'),('diamond_leggings','diamond_boots'),('iron_chestplate','iron_helmet'),('furnace','hopper'),('chest','hopper')]
for it,anch in EXTRA:
    if it in sections: continue
    q=take_empty(byitem[anch][0] if byitem.get(anch) else next(iter(empty)))
    if q is None: break
    P[q]['item']=it;P[q]['new']=True; sections[it]=[q]
    need=min(8,max(1,math.ceil(model.qty(it)/(54*model.stack(it)))))
    while len(sections[it])<need:
        r=take_empty(q)
        if r is None: break
        P[r]['item']=it;P[r]['new']=True; sections[it].append(r)
# reparto de cantidades
fill={}   # pair -> (item,count)
for it,ps in sections.items():
    total=int(round(model.qty(it))); cap=54*model.stack(it); total=min(total,cap*len(ps))
    base,rem=divmod(total,len(ps))
    for i,p in enumerate(ps): fill[p]=(it,base+(1 if i<rem else 0))
print('pares llenos',len(fill),'vacios sin usar',len(empty),'items distintos',len(sections))
# --- NBT helpers
def nstr(s): b=s.encode(); return struct.pack('<H',len(b))+b
def tag(t,name,pl): return bytes([t])+nstr(name)+pl
ENCH=[(26,1),(17,3),(18,3),(15,5),(9,5),(0,4),(14,3),(16,1),(19,5),(2,4)]
def item(name,count,slot=None,ench=None):
    pl=tag(1,'Count',bytes([count]))+tag(2,'Damage',struct.pack('<h',0))+tag(8,'Name',nstr('minecraft:'+name))+tag(1,'WasPickedUp',b'\0')
    if slot is not None: pl+=tag(1,'Slot',bytes([slot]))
    if ench:
        el=b''.join(tag(2,'id',struct.pack('<h',i))+tag(2,'lvl',struct.pack('<h',l))+b'\0' for i,l in ench)
        pl+=tag(10,'tag',tag(9,'ench',bytes([10])+struct.pack('<i',len(ench))+el)+b'\0')
    return pl+b'\0'
def itemlist(it,count):
    st=model.stack(it); stacks=[]
    while count>0 and len(stacks)<54: n=min(st,count); stacks.append(n); count-=n
    halves=[stacks[:27],stacks[27:54]]; out=[]
    k=0
    for h in halves:
        its=[]
        for s,n in enumerate(h):
            ench=[ENCH[k%len(ENCH)]] if it=='enchanted_book' else None; k+=1
            its.append(item(it,n,s,ench))
        out.append(bytes([10])+struct.pack('<i',len(its))+b''.join(its))
    return out
def set_key(payload,key,val,t):
    o=0
    while True:
        tt=payload[o]
        if tt==0: return payload[:o]+tag(t,key,val)+payload[o:]
        n=struct.unpack_from('<H',payload,o+1)[0]; k=payload[o+3:o+3+n].decode(); vo=o+3+n
        _,e=nbt.pay(payload,vo,tt)
        if k==key: return payload[:vo]+val+payload[e:]
        o=e
# indices
chest_new={};frame_new={}
for p,(it,cnt) in fill.items():
    l=itemlist(it,cnt)
    chest_new[p[0]]=l[0]; chest_new[p[1]]=l[1]
    if P[p]['new']: frame_new[P[p]['frame']]=it
touched=0
for cx in range(121,125):
  for cz in range(115,119):
    k=struct.pack('<ii',cx,cz)+bytes([49]); data=a.get(k)
    if not data: continue
    o=0;out=[]
    while o<len(data):
        e=sub.skip_root(data,o);raw=data[o:e];o=e
        dd=nbt.read(raw); pos=(dd['x'],dd['y'],dd['z']); pl=raw[3:]
        if dd['id']=='Chest' and pos in chest_new: pl=set_key(pl,'Items',chest_new[pos],9); touched+=1
        elif dd['id']=='ItemFrame' and pos in frame_new:
            pl=set_key(pl,'Item',item(frame_new[pos],1),10); touched+=1
        out.append(raw[:3]+pl)
    a[k]=b''.join(out)
print('block entities modificados',touched)
pickle.dump((a,seq),open('final2.pkl','wb'))
pickle.dump((P,fill,{k:v for k,v in sections.items()}),open('alloc.pkl','wb'))
