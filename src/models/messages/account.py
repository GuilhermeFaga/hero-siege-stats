from src.models.messages.base import BaseMessage


class AccountMessage(BaseMessage):
    version: int | None
    name: str
    class_id: int
    level: int
    experience: int
    herolevel: int
    talentMap: dict[str, int]
    hero_talents: list[int]
    aura: int
    loadout: int
    daily_hunt: int
    difficulty: int
    level_max_damage: float
    level_max_dps: int
    damage_source: str
    bind_button: list[int]
    bind_button2: list[int]
    bind_skill: list[int]
    bind_skill2: list[int]
    guild_reputation: int
    weapon_skin: list[int]
    fortune_enemies: int
    potion_autofill: int
    talent_reset: int
    season_reward_wings: int
    soloselffound: int
    acts: list[int]
    act_previous: int
    act_zones_1: list[int]
    act_zones_2: list[int]
    act_zones_3: list[int]
    act_zones_4: list[int]
    act_zones_5: list[int]
    act_zones_6: list[int]
    act_zones_7: list[int]
    act_zones_8: list[int]
    merc_alive: int
    merc_type: int
    merc_aura: int
    mercTalentMapMelee: dict
    mercTalentMapRanged: dict
    mercTalentMapMagic: dict
    chaos_towers_cleared: int
    wormhole_zone: list[int]
    wormhole_levels: list[int]
    fortune_item: str
    inventory_tab_name: list[str | None]
    shield_skin: int
    playstation_id: str
    attribute_points: list[int]
    socket_filter: int
    back_accessory: int
    inventory_reset: int
    hat: int
    skin: int
    hardcore: int
    loot_filter: list[list[int]]
    season: int
    season_reward_effect: int
    season_reward_portal: int

    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        self.version = msg_dict.get('version')
        self.name = msg_dict['name']
        self.class_id = msg_dict['class']
        self.level = msg_dict['level']
        self.experience = msg_dict['experience']
        self.herolevel = msg_dict['herolevel']
        self.talentMap = msg_dict['talentMap']
        self.hero_talents = msg_dict['hero_talents']
        self.aura = msg_dict['aura']
        self.loadout = msg_dict['loadout']
        self.daily_hunt = msg_dict['daily_hunt']
        self.difficulty = msg_dict['difficulty']
        self.level_max_damage = msg_dict['level_max_damage']
        self.level_max_dps = msg_dict['level_max_dps']
        self.damage_source = msg_dict['damage_source']
        self.bind_button = msg_dict['bind_button']
        self.bind_button2 = msg_dict['bind_button2']
        self.bind_skill = msg_dict['bind_skill']
        self.bind_skill2 = msg_dict['bind_skill2']
        self.guild_reputation = msg_dict['guild_reputation']
        self.weapon_skin = msg_dict['weapon_skin']
        self.fortune_enemies = msg_dict['fortune_enemies']
        self.potion_autofill = msg_dict['potion_autofill']
        self.talent_reset = msg_dict['talent_reset']
        self.season_reward_wings = msg_dict['season_reward_wings']
        self.soloselffound = msg_dict['soloselffound']
        self.acts = msg_dict['acts']
        self.act_previous = msg_dict['act_previous']
        self.act_zones_1 = msg_dict['act_zones_1']
        self.act_zones_2 = msg_dict['act_zones_2']
        self.act_zones_3 = msg_dict['act_zones_3']
        self.act_zones_4 = msg_dict['act_zones_4']
        self.act_zones_5 = msg_dict['act_zones_5']
        self.act_zones_6 = msg_dict['act_zones_6']
        self.act_zones_7 = msg_dict['act_zones_7']
        self.act_zones_8 = msg_dict['act_zones_8']
        self.merc_alive = msg_dict['merc_alive']
        self.merc_type = msg_dict['merc_type']
        self.merc_aura = msg_dict['merc_aura']
        self.mercTalentMapMelee = msg_dict['mercTalentMapMelee']
        self.mercTalentMapRanged = msg_dict['mercTalentMapRanged']
        self.mercTalentMapMagic = msg_dict['mercTalentMapMagic']
        self.chaos_towers_cleared = msg_dict['chaos_towers_cleared']
        self.wormhole_zone = msg_dict['wormhole_zone']
        self.wormhole_levels = msg_dict['wormhole_levels']
        self.fortune_item = msg_dict['fortune_item']
        self.inventory_tab_name = msg_dict['inventory_tab_name']
        self.shield_skin = msg_dict['shield_skin']
        self.playstation_id = msg_dict['playstation_id']
        self.attribute_points = msg_dict['attribute_points']
        self.socket_filter = msg_dict['socket_filter']
        self.back_accessory = msg_dict['back_accessory']
        self.inventory_reset = msg_dict['inventory_reset']
        self.hat = msg_dict['hat']
        self.skin = msg_dict['skin']
        self.hardcore = msg_dict['hardcore']
        self.loot_filter = msg_dict['loot_filter']
        self.season = msg_dict['season']
        self.season_reward_effect = msg_dict['season_reward_effect']
        self.season_reward_portal = msg_dict['season_reward_portal']
