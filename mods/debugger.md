Harlem512's debugger. Requires enabling `odebugger_new` by modifying the `data.win` file.

```sp
global.rmml.dev = true
```

# controller

## create

```sp
global.debug_unclamp_cam = false
```

## room_start

```catspeak
-- if global.map_data_ != undefined {
--   global.rmml.log(json_stringify(global.map_data_))
--   global.rmml.log(ds_grid_write(global.map_grid_))
--   let str = "{"
--   let x = 0
--   while x < array_length(global.map_data_) {
--     str += "\"" + string(x) + "\":{"
--     let y = 0
--     while y < array_length(global.map_data_[x]) {
--       d = global.map_data_[x][y]
--       str += "\"" + string(y) + "\":" + json_encode(d) + ","
--       y += 1
--     }
--     str += "},"
--     x += 1
--   }
--   str += "}"
--   global.rmml.log(str)
-- }

if instance_number(odebugger_new) == 0 {
  let debugger = instance_create_depth(0, 0, -1000, odebugger_new)
  debugger.persistent = true

  -- remove garbage debug options
  let i = 0
  while i < array_length(debugger.debug_data) {
    let data = debugger.debug_data[i]
    match data[1] {
      -- E
      case "Refresh" { array_delete(debugger.debug_data, i, 1) }
      -- O
      case "Log" { array_delete(debugger.debug_data, i, 1) }
      -- P
      case "Reset save" { array_delete(debugger.debug_data, i, 1) }
      -- J
      case "RLive" { array_delete(debugger.debug_data, i, 1) }
      -- B
      case "Undo room keys" { array_delete(debugger.debug_data, i, 1) }
      -- D
      case "text" { array_delete(debugger.debug_data, i, 1) }
      -- V
      case "Live" { array_delete(debugger.debug_data, i, 1) }
      else { i += 1}
    }
  }

  debugger.debug_add_function("J", "Player", "[c_red]", fun (a0, a1) {
    if a1 {
      if global.maya_mode {
        global.maya_mode = false
        global.ameli_mode_ = true
      } else if global.ameli_mode_ {
        global.ameli_mode_ = false
      } else {
        global.maya_mode = true
      }
    }
  })
  debugger.debug_add_function("V", "Cam unclamp", "[c_red]", fun (a0, a1) {
    if a1 {
      global.debug_unclamp_cam = !global.debug_unclamp_cam
    }
  })
  debugger.debug_add_function("O", "Quickboot", "[c_red]", fun (a0, a1) {
    if a1 {
      global.gamestate = 22
      game_restart()
      global.deb_quickboot = true
    }
  })
  debugger.debug_add_function("P", "_Reset Dev", "[c_red]", fun (a0, a1) {
    if a1 {
      file_delete(map_get_string(8))
      global.gamestate = 22
      game_restart()
      global.deb_quickboot = true
    }
  })
  debugger.debug_add_function("B", "Debug Names", "[c_red]", fun (a0, a1) {
    if a1 {
      global.deb_names = !global.deb_names
    }
  })
}
```

## draw

```sp
if global.deb_quickboot {
  with omenu_new {
    self.state = 8
    global.current_file = 8
    self.start_timer = 100
    global.speedrun_mode_ = 1
  }
  global.deb_quickboot = false
}

if global.debug_draw_hitboxes__ {
  -- main box
  draw_set_color(c_blue)
  -- position-bounds
  -- draw_rectangle(-32, -64, room_width_get() + 32, room_height_get() + 64, true)
  -- bbox-bounds
  with oplayer {
    draw_rectangle(
      -41, -- -32 - self.x + self.bbox_left,
      -96, -- -64 - self.y + self.bbox_top,
      room_width_get() + 40, --room_width_get() + 32 + self.bbox_right - self.x,
      room_height_get() + 64, true)
  }

  draw_set_color(c_green)
  draw_rectangle(0, 0, room_width_get(), room_height_get(), true)

  draw_set_color(c_orange)
  with oarena_test {
    draw_rectangle(self.bbox_left, self.bbox_top, self.bbox_right, self.bbox_bottom, true)
  }

  with par_boss {
    draw_circle(self.x, self.y, self.agro_range, true)
    draw_text(self.x, self.y - 15, string(self.state))
  }

  draw_set_color(c_red)
  with opit_generator {
    draw_rectangle(self.bbox_left, self.bbox_top, self.bbox_right, self.bbox_bottom, true)
  }

  draw_set_color(c_yellow)
  with oroom_transition {
    draw_rectangle(self.bbox_left, self.bbox_top, self.bbox_right, self.bbox_bottom, true)
  }

  with oplayer {
    draw_text(self.x, self.y - 15, string(self.shoot_delay))
    draw_text(self.x, self.y - 5, string(self.state))
  }

  draw_set_color(c_white)
}

if global.deb_names {
  with par_game {
    draw_text(self.x, self.y - 20, object_get_name(self.object_index))
  }
}
```

## step_end

```sp
with ocamera {
  if global.debug_unclamp_cam {
    self.clamp_pos = false
  } else {
    self.clamp_pos = true
  }
}
with oplayer {
  -- global.hlogger.dump_objects()
}
```

## draw_begin

```sp
if global.debug_unclamp_cam {
  with ogame {
    self.draw_catacombs_light = false
  }
}
```
