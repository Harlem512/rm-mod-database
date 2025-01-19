# controller

## room_start

```sp
-- clear cache
if global.__minimap {
  sprite_delete(global.__minimap)
}
-- mark minimap as dirty
global.__minimap = undefined
```

## draw_gui_end

```sp
-- check if we should render the map
if global.map_data_ != undefined and !global.trinket_active_[1] and !global.debug_ui_ {
  -- cache the minimap
  if !global.__minimap {
    -- build and clear surface
    let surf = surface_create(64, 64)
    surface_set_target(surf)
    draw_clear_alpha(c_black, 0)

    -- render the minimap
    let moffset_x = global.map_draw_offset_x_
    let moffset_y = global.map_draw_offset_y_
    global.map_draw_offset_x_ = global.player_map_x_ * 8 - 20
    global.map_draw_offset_y_ = global.player_map_y_ * 8 - 20
    with ogame {
      map_draw()
    }
    global.map_draw_offset_x_ = moffset_x
    global.map_draw_offset_y_ = moffset_y

    -- cache minimap
    global.__minimap = sprite_create_from_surface(surf, 0, 0, 40, 40, false, false, 0, 0)

    -- cleanup
    surface_reset_target()
    surface_free(surf)
  }

  let cam = instance_find(ocamera, 0)
  if !cam {
    return
  }
  let amult = 0.9
  let plr = instance_find(oplayer, 0)

  -- player position alpha
  if plr {
    let pdis = point_distance(cam.xpos + 22, cam.ypos + global.game_height - 22, plr.x, plr.y)
    if pdis < 90 {
      amult = clamp(lerp(-0.4, 1, pdis / 90), 0.2, 0.9)
    }
  }
  -- controller alpha
  if global.controller == 0 {
    let cdis = point_distance(22, global.game_height - 22,
      global.mousex - cam.xpos - max(0, (global.game_width - room_width_get()) / 2),
      global.mousey - cam.ypos - max(0, (global.game_height - room_height_get()) / 2)
    )
    if cdis < 100 {
      amult = min(clamp(lerp(-0.4, 1, cdis / 90), 0, 0.9), amult)
    }
  }
  draw_sprite_ext(global.__minimap, 0, 2, global.game_height - 42, 1, 1, 0, c_white, amult)
}
```