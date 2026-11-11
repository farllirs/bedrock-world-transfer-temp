import math,re
D=200; KEEP=0.6   # dias de juego efectivos con herramientas, fraccion que sigue guardada
FORT=2.2; LOOT=2.5
# base: items/dia SIN encantamientos
BASE=dict(
 cobblestone=140,deepslate=80,stone=25,andesite=15,diorite=12,granite=12,tuff=30,gravel=25,sand=35,red_sand=8,sandstone=10,red_sandstone=6,
 netherrack=160,basalt=18,smooth_basalt=8,blackstone=25,soul_sand=8,soul_soil=8,end_stone=40,calcite=6,clay=6,clay_ball=20,snow=10,ice=8,packed_ice=5,blue_ice=3,
 obsidian=10,magma=8,moss_block=10,mud=15,mud_bricks=8,bone_block=3,prismarine=6,sea_lantern=1,glass=25,smooth_stone=12,stonebrick=15,brick_block=8,hardened_clay=6,
 netherbrick=10,nether_brick=8,quartz_block=3,glowstone=5,amethyst_block=2,sponge=0.4,
 oak_log=30,birch_log=20,spruce_log=20,jungle_log=15,acacia_log=15,dark_oak_log=20,cherry_log=15,mangrove_log=12,pale_oak_log=20,poplar_log=20,crimson_stem=20,warped_stem=20,
 bamboo=100,stick=40,paper=60,book=10,
 wheat=80,wheat_seeds=100,carrot=90,potato=90,beetroot=40,melon_slice=100,pumpkin=40,sweet_berries=30,cocoa_beans=40,reeds=120,cactus=60,kelp=120,dried_kelp=60,nether_wart=80,
 brown_mushroom=20,red_mushroom=20,apple=12,bread=15,hay_block=6,honey_bottle=10,honeycomb=12,sugar=40,bone_meal=100,golden_carrot=5,golden_apple=0.3,
 cooked_beef=40,cooked_chicken=35,cooked_mutton=25,cooked_cod=15,cooked_salmon=15,cod=15,salmon=15,beef=40,porkchop=40,chicken=35,mutton=25,egg=30,
 crimson_fungus=15,warped_fungus=15,crimson_roots=15,warped_roots=15,nether_sprouts=10,twisting_vines=15,weeping_vines=15,shroomlight=10,
 charcoal=20,torch=15,tnt=12,
 gold_ingot=12,gold_nugget=40,iron_ingot=120,iron_nugget=30,copper_ingot=35,
 amethyst_shard=5,ancient_debris=1.2,glowstone_dust=10,flint=12,
 lever=1.5,repeater=1.5,comparator=1,observer=1.5,piston=1.5,sticky_piston=1,dispenser=1,dropper=1,hopper=2,redstone_lamp=3,rail=15,golden_rail=3,bookshelf=1,slime=1.5,
 oak_planks=20,spruce_planks=12,birch_planks=12,jungle_planks=8,acacia_planks=8,dark_oak_planks=12,cherry_planks=8,mangrove_planks=6,pale_oak_planks=14,bamboo_planks=8,crimson_planks=8,warped_planks=8,
 dirt=30,end_bricks=10,cobbled_deepslate=60,cooked_porkchop=25,baked_potato=20,furnace=3,chest=3,diamond_pickaxe=0.01,
)
# con Fortune III (x2.2)
FORTUNE=dict(diamond=3,emerald=2.5,lapis_lazuli=12,coal=45,quartz=25,raw_iron=40,raw_gold=18,raw_copper=35)
FORTUNE_X=dict(redstone=(25,1.75))
# con Looting III (x2.5)
LOOTING=dict(bone=90,rotten_flesh=130,string=70,spider_eye=25,gunpowder=70,arrow=50,ender_pearl=12,slime_ball=15,ink_sac=18,glow_ink_sac=3,feather=40,leather=25,rabbit_hide=3,
 blaze_rod=8,blaze_powder=6,ghast_tear=0.5,magma_cream=4,shulker_shell=0.6,dragon_breath=1,fire_charge=2,chorus_fruit=15,chorus_flower=3,nautilus_shell=0.2,name_tag=0.3)
OTHER=dict(end_rod=2,end_crystal=0.6,purpur_block=20,ender_eye=3,nether_star=0.03,beacon=0.03,dragon_egg=0.005,elytra=0.01)
COMPRESS=dict(iron_block='iron_ingot',gold_block='gold_ingot',diamond_block='diamond',emerald_block='emerald',lapis_block='lapis_lazuli',coal_block='coal',redstone_block='redstone',
 copper_block='copper_ingot',raw_iron_block='raw_iron',raw_gold_block='raw_gold')
FIXED=dict(diamond_helmet=4,diamond_boots=4,diamond_chestplate=3,diamond_leggings=3,diamond_axe=3,diamond_hoe=3,diamond_sword=5,diamond_shovel=3,diamond_pickaxe=3,
 iron_axe=8,iron_hoe=6,iron_pickaxe=10,iron_shovel=8,iron_sword=8,iron_helmet=6,iron_leggings=6,iron_boots=6,iron_chestplate=6,
 netherite_axe=1,netherite_hoe=1,bow=6,crossbow=4,shield=4,fishing_rod=8,shears=5,minecart=24,anvil=8,enchanted_book=30,
 bucket=48,water_bucket=8,lava_bucket=8,elytra=1,dragon_egg=1,beacon=6,nether_star=6,name_tag=24,nautilus_shell=6,shulker_shell=40)
def stack(n):
    if re.search(r'(helmet|chestplate|leggings|boots|sword|pickaxe|_axe|shovel|_hoe|^bow$|crossbow|shield|fishing_rod|shears|minecart|enchanted_book|elytra|dragon_egg|water_bucket|lava_bucket)',n): return 1
    if n in('ender_pearl','egg','bucket','honey_bottle'): return 16
    return 64
def qty_raw(n,tab=None):
    """cantidad total acumulada estimada (antes de comprimir)"""
    if n in FORTUNE: return FORTUNE[n]*FORT*D*KEEP
    if n in FORTUNE_X: b,m=FORTUNE_X[n]; return b*m*D*KEEP
    if n in LOOTING: return LOOTING[n]*LOOT*D*KEEP
    if n in OTHER: return OTHER[n]*D*KEEP
    if n in BASE: return BASE[n]*D*KEEP
    return None
def qty(n):
    if n in FIXED: return FIXED[n]
    if n in COMPRESS:
        return qty_raw(COMPRESS[n])*0.20/9      # ~20% del mineral compactado en bloques
    r=qty_raw(n)
    if r is None: return 128
    if n in COMPRESS.values(): r*=0.80
    return r
