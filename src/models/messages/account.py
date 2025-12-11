from src.models.messages.base import BaseMessage
from src.consts.season import CURRENT_SEASON

class AccountMessage(BaseMessage):
    version: int | None
    name: str
    class_id: int
    level: int
    experience: int
    herolevel: int
    talentMap_0: dict[str,int]
    talentMap_1: dict[str, int]
    talentMap_2: dict[str,int]
    talentMap_3: dict[str,int]
    subTalentMap_0: dict[str, dict[str, int]]
    subTalentMap_1: dict[str, dict[str, int]]
    subTalentMap_2: dict[str, dict[str, int]]
    subTalentMap_3: dict[str, dict[str, int]]
    aura: list[list[int]]
    loadout: int
    talent_loadout: int
    difficulty: int
    level_max_damage: int
    level_max_dps: int
    damage_source: str
    bind_skill: list[list[int]]
    bind_skill2: list[list[int]]
    weapon_skin: list[int]
    fortune_enemies: list[list[int]]
    potion_autofill: int
    potion_useall: int
    talent_reset: int
    season_reward_wings: int
    soloselffound: int
    acts: list[int]
    act_previous: list[list[int]]
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
    merc_talents: list[int]
    merc_hat: list[int]
    merc_skin: list[int]
    merc_name: list[str]
    chaos_towers_cleared: int
    wormhole_zone: list[int]
    wormhole_levels: list[int]
    fortune_item: list[list[str]]
    inventory_tab_name: list[str | None]
    shield_skin: int
    playstation_id: str
    attribute_points: list[list[int]]
    back_accessory: int
    inventory_reset: int
    hat: int
    skin: int
    hardcore: int
    season: int
    season_reward_effect: int
    season_reward_portal: int
    incarnation_exp: int
    title: int
    companion: int
    player_explosion: int
    player_trail: int
    heroboard: str
    grindfest_door_open: int
    waypoints: dict
    codex_data: str
    playtime: int
    chaos_tower_boss_kills: int
    chaos_tower_boss_kills_hash: str
    hell_subdifficulty: int
    spell_chain_skin: int
    spell_explo_skin: int
    quest_chains: dict[str, int | str]
    blood_pact: int

    def get_current_season_mode(self):
        if self.season != CURRENT_SEASON:
            return "GNH" if self.hardcore == 1 else "GNS"
        else:
            return "GSH" if self.hardcore == 1 else "GSS"
        return "GBP"
    
    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        self.version = msg_dict.get('version')
        self.name = msg_dict['name']
        self.class_id = msg_dict['class']
        self.level = msg_dict['level']
        self.experience = msg_dict['experience']
        self.herolevel = msg_dict['herolevel']
        self.talentMap_0 = msg_dict['talentMap_0']
        self.talentMap_1 = msg_dict['talentMap_1']
        self.talentMap_2 = msg_dict['talentMap_2']
        self.talentMap_3 = msg_dict['talentMap_3']
        self.subTalentMap_0 = msg_dict['subTalentMap_0']
        self.subTalentMap_1 = msg_dict['subTalentMap_1']
        self.subTalentMap_2 = msg_dict['subTalentMap_2']
        self.subTalentMap_3 = msg_dict['subTalentMap_3']
        self.aura = msg_dict['aura']
        self.loadout = msg_dict['loadout']
        self.talent_loadout = msg_dict.get('talent_loadout', 0)
        self.difficulty = msg_dict['difficulty']
        self.level_max_damage = msg_dict['level_max_damage']
        self.level_max_dps = msg_dict['level_max_dps']
        self.damage_source = msg_dict['damage_source']
        self.bind_skill = msg_dict['bind_skill']
        self.bind_skill2 = msg_dict['bind_skill2']
        self.weapon_skin = msg_dict['weapon_skin']
        self.fortune_enemies = msg_dict['fortune_enemies']
        self.potion_autofill = msg_dict['potion_autofill']
        self.potion_useall = msg_dict.get('potion_useall', 0)
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
        self.merc_talents = msg_dict['merc_talents']
        self.merc_hat = msg_dict['merc_hat']
        self.merc_skin = msg_dict['merc_skin']
        self.merc_name = msg_dict['merc_name']
        self.chaos_towers_cleared = msg_dict['chaos_towers_cleared']
        self.wormhole_zone = msg_dict['wormhole_zone']
        self.wormhole_levels = msg_dict['wormhole_levels']
        self.fortune_item = msg_dict['fortune_item']
        self.inventory_tab_name = msg_dict['inventory_tab_name']
        self.shield_skin = msg_dict['shield_skin']
        self.playstation_id = msg_dict['playstation_id']
        self.attribute_points = msg_dict['attribute_points']
        self.back_accessory = msg_dict['back_accessory']
        self.inventory_reset = msg_dict['inventory_reset']
        self.hat = msg_dict['hat']
        self.skin = msg_dict['skin']
        self.hardcore = msg_dict['hardcore']
        self.season = msg_dict['season']
        self.season_reward_effect = msg_dict['season_reward_effect']
        self.season_reward_portal = msg_dict['season_reward_portal']
        self.incarnation_exp = msg_dict['incarnation_exp']
        self.title = msg_dict['title']
        self.companion = msg_dict['companion']
        self.player_explosion = msg_dict['player_explosion']
        self.player_trail = msg_dict['player_trail']
        self.heroboard = msg_dict['heroboard']
        self.grindfest_door_open = msg_dict['grindfest_door_open']
        self.waypoints = msg_dict['waypoints']
        self.codex_data = msg_dict['codex_data']
        self.playtime = msg_dict['playtime']
        self.chaos_tower_boss_kills = msg_dict['chaos_tower_boss_kills']
        self.chaos_tower_boss_kills_hash = msg_dict['chaos_tower_boss_kills_hash']
        self.hell_subdifficulty = msg_dict['hell_subdifficulty']
        self.spell_chain_skin = msg_dict['spell_chain_skin']
        self.spell_explo_skin = msg_dict['spell_explo_skin']
        self.quest_chains = msg_dict['quest_chains']
        self.blood_pact = msg_dict['blood_pact']
