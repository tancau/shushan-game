#!/usr/bin/env python3
"""蜀山剑侠传素材GPU快速生成 - 使用RTX 3060"""
import os, sys, time, torch, gc
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler
from PIL import Image

DEVICE = "cuda"
print(f"使用设备: {DEVICE}")
print(f"GPU: {torch.cuda.get_device_name(0)}")

OUTPUT_DIR = os.path.expanduser("~/shushan_assets")
MODEL_ID = "runwayml/stable-diffusion-v1-5"
STEPS = 15
SIZE = 384

print("加载模型到GPU...")
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID, torch_dtype=torch.float16,
    safety_checker=None, requires_safety_checker=False
)
pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to(DEVICE)
pipe.enable_attention_slicing()
pipe.enable_vae_slicing()
print("模型加载完成！")

def gen(prompt, path, size=SIZE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        return
    try:
        img = pipe(prompt, num_inference_steps=STEPS, height=size, width=size, guidance_scale=7.5).images[0]
        img.save(path)
        print(f"OK {os.path.basename(path)}")
    except Exception as e:
        print(f"FAIL {os.path.basename(path)}: {e}")
    gc.collect()
    torch.cuda.empty_cache()

# 功法(45)
for k,v in {
"skill_taiqing":"Chinese fantasy taiqing qi golden energy daoist game icon",
"skill_emei_sword_art":"Chinese fantasy emei sword art elegant female sword game icon",
"skill_ziqing_swords":"Chinese fantasy ziqing dual swords purple green game icon",
"skill_kunlun_sword":"Chinese fantasy kunlun sword ice mountain game icon",
"skill_wudang_sword":"Chinese fantasy wudang taiji sword yin yang game icon",
"skill_huashan_sword":"Chinese fantasy huashan sword cliff game icon",
"skill_qingcheng_sword":"Chinese fantasy qingcheng sword green game icon",
"skill_kongtong_demon":"Chinese fantasy kongtong demon sword dark game icon",
"skill_five_elements":"Chinese fantasy five elements magic colorful game icon",
"skill_thunder_jue":"Chinese fantasy thunder technique lightning game icon",
"skill_ice_soul":"Chinese fantasy ice soul technique frost game icon",
"skill_flame_palm":"Chinese fantasy flame palm fire hand game icon",
"skill_wind_walk":"Chinese fantasy wind walk air swirl game icon",
"skill_earth_escape":"Chinese fantasy earth escape ground game icon",
"skill_alchemy":"Chinese fantasy alchemy technique cauldron game icon",
"skill_dan_xinfa":"Chinese fantasy dan dao heart method pill game icon",
"skill_fire_control":"Chinese fantasy fire control flames game icon",
"skill_herb_identify":"Chinese fantasy herb identification plant game icon",
"skill_vajra":"Chinese fantasy vajra body golden armor game icon",
"skill_iron_shirt":"Chinese fantasy iron shirt metallic body game icon",
"skill_dragon_elephant":"Chinese fantasy dragon elephant strength powerful game icon",
"skill_bagua_formation":"Chinese fantasy bagua formation eight trigrams game icon",
"skill_qimen_dunjia":"Chinese fantasy qimen dunjia mystical door game icon",
"skill_five_element_formation":"Chinese fantasy five element formation colorful circle game icon",
"skill_seal_technique":"Chinese fantasy seal technique binding rune game icon",
"skill_sword_riding":"Chinese fantasy sword riding flying sword game icon",
"skill_escape_art":"Chinese fantasy escape art speed lines game icon",
"skill_divine_sense":"Chinese fantasy divine sense third eye game icon",
"skill_invisibility":"Chinese fantasy invisibility transparent game icon",
"skill_tiangan_36":"Chinese fantasy tiangan 36 transformations golden game icon",
"skill_disha_72":"Chinese fantasy disha 72 transformations dark game icon",
"skill_taishang_forget":"Chinese fantasy taishang forget emotion serene game icon",
"skill_soul_search":"Chinese fantasy soul search technique spirit hand game icon",
"skill_possession":"Chinese fantasy possession art dark spirit game icon",
"skill_blood_sacrifice":"Chinese fantasy blood sacrifice red ritual game icon",
"skill_star_sword":"Chinese fantasy star sword technique starlight game icon",
"skill_moon_blade":"Chinese fantasy moon blade technique crescent game icon",
"skill_sun_flame":"Chinese fantasy sun flame technique solar fire game icon",
"skill_shadow_step":"Chinese fantasy shadow step dark footsteps game icon",
"skill_spirit_shield":"Chinese fantasy spirit shield blue barrier game icon",
"skill_heal_art":"Chinese fantasy healing art green light game icon",
"skill_poison_art":"Chinese fantasy poison art purple venom game icon",
"skill_summon_beast":"Chinese fantasy beast summon creature game icon",
"skill_soul_refine":"Chinese fantasy soul refine spirit fire game icon",
"skill_nether_art":"Chinese fantasy nether world art ghostly game icon",
}.items():
    gen(v, f"{OUTPUT_DIR}/skills/{k}.png")

# NPC(24)
for k,v in {
"npc_qi_shuyin":"Chinese immortal female sect leader elegant white robes game icon",
"npc_miaoyi":"Chinese immortal male elder white beard serene daoist game icon",
"npc_zhu_mei_emei":"Chinese immortal short elder kind face red robes game icon",
"npc_zui_daoren":"Chinese immortal drunk elder wine gourd messy game icon",
"npc_zhu_mei_qc":"Chinese immortal elder green robes serious game icon",
"npc_zhong_xiansheng":"Chinese immortal tall elder scholarly game icon",
"npc_wei_shaoshao":"Chinese immortal young master handsome green game icon",
"npc_tie_san":"Chinese immortal stern elder iron umbrella game icon",
"npc_yuqing":"Chinese immortal female elder jade crown serene game icon",
"npc_xuanzhenzi_kl":"Chinese immortal grandmaster white hair powerful game icon",
"npc_xuanzhenzi_wd":"Chinese immortal calm elder taiji symbol game icon",
"npc_song_yuanqiao":"Chinese immortal dignified swordsman blue robes game icon",
"npc_yu_lianzhou":"Chinese immortal serious swordsman blue game icon",
"npc_kunlun_master":"Chinese dark sect master dark robes menacing game icon",
"npc_dushou":"Chinese dark cultivator poison hands evil game icon",
"npc_guiying":"Chinese dark assassin shadow hooded game icon",
"npc_ai_sou":"Chinese immortal dwarf elder short wise game icon",
"npc_mu_renqing":"Chinese immortal old skilled swordsman game icon",
"npc_feng_qingyang":"Chinese immortal hermit swordsman free spirit game icon",
"npc_merchant":"Chinese fantasy merchant trading goods friendly game icon",
"npc_blacksmith":"Chinese fantasy blacksmith forging muscular game icon",
"npc_alchemist":"Chinese fantasy alchemist cauldron wise game icon",
"npc_guide_elder":"Chinese immortal guide elder teaching kind game icon",
"npc_mysterious":"Chinese mysterious cultivator hooded unknown game icon",
}.items():
    gen(v, f"{OUTPUT_DIR}/npcs/{k}.png")

# 灵兽(23)
for k,v in {
"beast_phoenix":"Chinese fantasy phoenix fire bird legendary game icon",
"beast_kirin":"Chinese fantasy qilin kirin auspicious golden game icon",
"beast_tortoise":"Chinese fantasy black tortoise ancient shell game icon",
"beast_sparrow":"Chinese fantasy vermillion bird fire sparrow game icon",
"beast_serpent":"Chinese fantasy giant serpent water game icon",
"beast_centipede":"Chinese fantasy giant centipede dark game icon",
"beast_scorpion":"Chinese fantasy giant scorpion desert game icon",
"beast_spider":"Chinese fantasy giant spider dark web game icon",
"beast_bat":"Chinese fantasy giant bat cave game icon",
"beast_rat":"Chinese fantasy spirit rat swift game icon",
"beast_monkey":"Chinese fantasy spirit monkey clever game icon",
"beast_deer":"Chinese fantasy spirit deer graceful game icon",
"beast_crane":"Chinese fantasy immortal crane elegant game icon",
"beast_carp":"Chinese fantasy spirit carp golden game icon",
"beast_toad":"Chinese fantasy giant toad poison game icon",
"beast_beetle":"Chinese fantasy giant beetle armored game icon",
"beast_mantis":"Chinese fantasy giant mantis blade arms game icon",
"beast_eagle":"Chinese fantasy thunder eagle storm game icon",
"beast_leopard":"Chinese fantasy shadow leopard fast game icon",
"beast_bear":"Chinese fantasy spirit bear strong game icon",
"beast_fox_nine":"Chinese fantasy nine-tailed fox mystical game icon",
"beast_turtle_dragon":"Chinese fantasy turtle dragon hybrid game icon",
"beast_peacock":"Chinese fantasy peacock demon beautiful game icon",
}.items():
    gen(v, f"{OUTPUT_DIR}/beasts/{k}.png")

# 材料+丹药(6)
for k,v in {
"mat_spirit_jade":"Chinese fantasy spirit jade white green glowing game icon",
"mat_dragon_scale":"Chinese fantasy dragon scale green gold game icon",
"mat_phoenix_feather":"Chinese fantasy phoenix feather red gold game icon",
"mat_demon_core":"Chinese fantasy demon core dark purple game icon",
"mat_celestial_stone":"Chinese fantasy celestial stone starry game icon",
"pill_nine_turn":"Chinese fantasy nine-turn golden pill golden game icon",
}.items():
    gen(v, f"{OUTPUT_DIR}/misc/{k}.png")

# 飞剑(20)
for k,v in {
"sword_iron":"Chinese fantasy iron sword basic game icon",
"sword_bronze":"Chinese fantasy bronze sword ancient game icon",
"sword_steel":"Chinese fantasy steel sword sharp game icon",
"sword_jade":"Chinese fantasy jade sword white jade game icon",
"sword_wood":"Chinese fantasy wooden sword training game icon",
"sword_azure":"Chinese fantasy azure sword cyan spiritual game icon",
"sword_crimson":"Chinese fantasy crimson sword red fire game icon",
"sword_frost":"Chinese fantasy frost sword ice blue game icon",
"sword_thunder":"Chinese fantasy thunder sword purple lightning game icon",
"sword_earth":"Chinese fantasy earth sword brown stone game icon",
"sword_celestial":"Chinese fantasy celestial sword golden heavenly game icon",
"sword_dragon":"Chinese fantasy dragon sword green dragon game icon",
"sword_phoenix":"Chinese fantasy phoenix sword red gold game icon",
"sword_moon":"Chinese fantasy moon sword silver lunar game icon",
"sword_sun":"Chinese fantasy sun sword golden solar game icon",
"sword_void":"Chinese fantasy void sword dark purple space game icon",
"sword_time":"Chinese fantasy time sword gold silver temporal game icon",
"sword_soul":"Chinese fantasy soul sword ethereal blue game icon",
"sword_demon":"Chinese fantasy demon sword dark red evil game icon",
"sword_holy":"Chinese fantasy holy sword white gold divine game icon",
}.items():
    gen(v, f"{OUTPUT_DIR}/swords/{k}.png")

# 剑诀技能(15)
for k,v in {
"skill_sword_slash":"Chinese fantasy sword slash blade light game icon",
"skill_sword_thrust":"Chinese fantasy sword thrust piercing game icon",
"skill_sword_parry":"Chinese fantasy sword parry defense game icon",
"skill_sword_dodge":"Chinese fantasy sword dodge evasion game icon",
"skill_sword_fire":"Chinese fantasy fire sword flame blade game icon",
"skill_sword_ice":"Chinese fantasy ice sword frost blade game icon",
"skill_sword_thunder_sk":"Chinese fantasy thunder sword lightning game icon",
"skill_sword_wind":"Chinese fantasy wind sword air blade game icon",
"skill_sword_qi":"Chinese fantasy sword qi energy blade game icon",
"skill_sword_formation":"Chinese fantasy sword formation multiple game icon",
"skill_sword_flight":"Chinese fantasy flying sword aerial game icon",
"skill_sword_spirit":"Chinese fantasy sword spirit spectral game icon",
"skill_sword_seal":"Chinese fantasy sword seal binding game icon",
"skill_sword_break":"Chinese fantasy sword break destroying game icon",
"skill_sword_ultimate":"Chinese fantasy ultimate sword powerful game icon",
}.items():
    gen(v, f"{OUTPUT_DIR}/sword_skills/{k}.png")

# 剑灵(10)
for k,v in {
"spirit_dragon":"Chinese fantasy dragon spirit serpentine wise game icon",
"spirit_phoenix":"Chinese fantasy phoenix spirit fire bird game icon",
"spirit_tiger":"Chinese fantasy tiger spirit fierce game icon",
"spirit_turtle":"Chinese fantasy turtle spirit ancient game icon",
"spirit_crane":"Chinese fantasy crane spirit elegant game icon",
"spirit_fox":"Chinese fantasy fox spirit cunning game icon",
"spirit_snake":"Chinese fantasy snake spirit flexible game icon",
"spirit_wolf":"Chinese fantasy wolf spirit loyal game icon",
"spirit_deer":"Chinese fantasy deer spirit gentle game icon",
"spirit_koi":"Chinese fantasy koi spirit luck water game icon",
}.items():
    gen(v, f"{OUTPUT_DIR}/spirits/{k}.png")

# 剑气特效(10) - 大尺寸
for k,v in {
"effect_sword_qi_golden":"Chinese fantasy golden sword qi slash light game effect",
"effect_sword_qi_blue":"Chinese fantasy blue sword qi energy game effect",
"effect_sword_qi_purple":"Chinese fantasy purple sword qi mystical game effect",
"effect_sword_qi_fire":"Chinese fantasy fire sword qi flame game effect",
"effect_sword_qi_ice":"Chinese fantasy ice sword qi frost game effect",
"effect_sword_qi_thunder":"Chinese fantasy thunder sword qi lightning game effect",
"effect_sword_qi_wind":"Chinese fantasy wind sword qi air game effect",
"effect_sword_qi_void":"Chinese fantasy void sword qi dark game effect",
"effect_sword_qi_holy":"Chinese fantasy holy sword qi divine game effect",
"effect_sword_qi_demon":"Chinese fantasy demon sword qi dark red game effect",
}.items():
    gen(v, f"{OUTPUT_DIR}/sword_qi/{k}.png", size=512)

# 剑冢背景(6) - 大尺寸
for k,v in {
"bg_sword_tomb_entrance":"Chinese fantasy sword tomb entrance ancient gate mystical",
"bg_sword_tomb_hall":"Chinese fantasy sword tomb hall countless swords mystical",
"bg_sword_tomb_forge":"Chinese fantasy sword forge ancient furnace fire",
"bg_sword_tomb_vault":"Chinese fantasy sword vault treasure golden",
"bg_sword_tomb_arena":"Chinese fantasy sword arena training ground",
"bg_sword_tomb_spirit":"Chinese fantasy sword spirit realm ethereal",
}.items():
    gen(v, f"{OUTPUT_DIR}/sword_tomb/{k}.png", size=512)

# 飞行动画帧(20) - 小sprite
for k,v in {
"flight_takeoff_01":"Chinese cultivator standing ready white robes sprite",
"flight_takeoff_02":"Chinese cultivator sword appearing sprite",
"flight_takeoff_03":"Chinese cultivator stepping on sword sprite",
"flight_takeoff_04":"Chinese cultivator sword lifting sprite",
"flight_takeoff_05":"Chinese cultivator rising up sprite",
"flight_takeoff_06":"Chinese cultivator ascending sprite",
"flight_takeoff_07":"Chinese cultivator flying stance sprite",
"flight_takeoff_08":"Chinese cultivator stable flight sprite",
"flight_cruise_01":"Chinese cultivator flying on sword smooth sprite",
"flight_cruise_02":"Chinese cultivator flying slight tilt sprite",
"flight_cruise_03":"Chinese cultivator flying wind sprite",
"flight_cruise_04":"Chinese cultivator flying robes flow sprite",
"flight_cruise_05":"Chinese cultivator flying speed sprite",
"flight_cruise_06":"Chinese cultivator flying stable sprite",
"flight_land_01":"Chinese cultivator descending sprite",
"flight_land_02":"Chinese cultivator nearing ground sprite",
"flight_land_03":"Chinese cultivator landing sprite",
"flight_land_04":"Chinese cultivator stepping off sprite",
"flight_land_05":"Chinese cultivator sword sheathing sprite",
"flight_land_06":"Chinese cultivator landed sprite",
}.items():
    gen(v, f"{OUTPUT_DIR}/flight/{k}.png", size=128)

print("ALL DONE!")
total = 0
for root, dirs, files in os.walk(OUTPUT_DIR):
    total += len([f for f in files if f.endswith('.png')])
print(f"Total generated: {total}")
