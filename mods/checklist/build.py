import json

with open("data/room_data.json") as f:
    json_data = json.load(f)
    out = 'global.checklist_draw = fun(mx, my, md) {if !ds_exists(global.save_data, ds_type_map){return}if global.rmml.__mod_controllers.archipelago{\nlet check=global.archipelago.save.checkedLocations\n'

    # archipelago prints
    for room, data in json_data.items():
        checks = []
        if 'pickup' in data:
            for pickup in data['pickup']:
                checks.append(
                    f'variable_struct_exists(check, "{pickup["type"][1:]}_{room}")'
                )
        if 'gun' in data:
            checks.append(f'variable_struct_exists(check, "pickup_weapon_{room}",0)')

        if len(checks) > 0:
            out += f'if '
            # out += f'(md[{room}][0].found or global.checklist_cheat) and '
            out += f'!({" and ".join(checks)}) {{'
            out += f'draw_sprite(smap_seer, 0, {data["map_x"] * 8} - mx, {data["map_y"] * 8} - my)'
            out += '}\n'

    # standard map
    out += "} else {"

    for room, data in json_data.items():
        checks = []
        if 'pickup' in data:
            for pickup in data['pickup']:
                checks.append(
                    f'map_return_safe("{pickup["type"][1:]}_{room}",0)'
                )
        if 'gun' in data:
            checks.append(f'map_return_safe("pickup_weapon_{room}",0)')

        if len(checks) > 0:
            out += f'if '
            # out += f'(md[{room}][0].found or global.checklist_cheat) and '
            out += f'!({" and ".join(checks)}) {{'
            out += f'draw_sprite(smap_seer, 0, {data["map_x"] * 8} - mx, {data["map_y"] * 8} - my)'
            out += '}\n'

    out += "} }"


with open('mods/checklist/codegen.meow', 'w') as f:
    f.write(out)
