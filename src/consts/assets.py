# HUD
HudValueDisplayLg: str = "value_display_large.png"
HudValueDisplayMd: str = "value_display_normal.png"
HudValueDisplaySm: str = "value_display_small.png"
HudValueDisplayXl: str = "value_display_xl.png"

# Icons
IcLogo: str = "logo24x24.png"

IcLogo16: str = "logo16x16.png"
IcLogo24: str = "logo24x24.png"
IcLogo32: str = "logo32x32.png"
IcLogo48: str = "logo48x48.png"
IcLogo256: str = "logo256x256.png"

IcCoins: str = "coins.png"
IcXp: str = "xp.png"

IcTime: str = "time.png"

IcMailOff: str = "mail_0.png"
IcMailOn: str = "mail_1.png"

IcChest: str = "chest.png"

# Icons Satanic Zone Buffs:
IcBuffDefault: str = "sz_buff_default.png"
IcBuff_1: str = "sz_buff_loot.png"
IcBuff_2: str = "sz_buff_loot.png"
IcBuff_3: str = "sz_buff_runes.png"
IcBuff_4: str = "sz_buff_gold.png"
IcBuff_5: str = "sz_buff_heroic.png"
IcBuff_6: str = "sz_buff_angelic.png"
IcBuff_7: str = "sz_buff_zephy.png"
IcBuff_8: str = "sz_buff_fury_of_tempest.png"
IcBuff_9: str = "sz_buff_cast_rate.png"
IcBuff_10: str = "sz_buff_onslaught.png"
IcBuff_11: str = "sz_buff_nether_surge.png"
IcBuff_12: str = "sz_buff_relics.png"
IcBuff_13: str = "sz_buff_goblin.png"
IcBuff_14: str = "sz_buff_mf.png"
IcBuff_15: str = "sz_buff_mf.png"
IcBuff_16: str = "sz_buff_mf.png"
IcBuff_17: str = "sz_buff_combat_training.png"
IcBuff_18: str = "sz_buff_combat_training.png"
IcBuff_19: str = "sz_buff_combat_training.png"  
IcBuff_20: str = "sz_buff_clairvoyance.png"
IcBuff_21: str = "sz_buff_aftermath.png"
IcBuff_22: str = "sz_buff_deep_cuts.png"
IcBuff_23: str = "sz_buff_ancient_pack.png"
IcBuff_24: str = "sz_buff_ancient_pack_2.png"
IcBuff_25: str = "sz_buff_ancient_pack_2.png" #not sure if it exists havent seen it and dont know if it has a different icon like the first and second level of the acient pack buff

# retrieve buff icon path object helper function
def get_buff_icon(name):
    return globals()[name]

# Font Colors
FcDefault: str = "<font color=\"#C3AF75\">"
FcAngelic: str = "<font color=\"#F6F794\">"
FcHeroic: str = "<font color=\"#00FFAE\">"
FcSatanic: str = "<font color=\"#CA1717\">"
FcBlue: str = "<font color=\"#5050AE\">"


