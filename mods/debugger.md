Harlem512's debugger. Requires enabling `odebugger_new` by modifying the `data.win` file.

```sp
global.rmml.dev = true

global.debug_unclamp_cam = false

global.deb_trans = {}

global.deb_trans_add = fun (roomA, roomB, _left, _right, _top, _bot) {
  if !global.deb_trans[roomA] {
    global.deb_trans[roomA] = {}
  }

  global.deb_trans[roomA][roomB] = {
    left: _left,
    right: _right,
    top: _top,
    bottom: _bot,
  }
}

global.time = {
  _times: {},
  start: fun (label) {
    if !global.time._times[label] {
      global.time._times[label] = {
        window_index: 0,
        window: array_create(600, 0),
        total: 0,
        start: 0,
      }
    }
    let t = global.time._times[label]
    t.start = get_timer()
  },
  end: fun (label, print) {
    let t = get_timer()
    let timer = global.time._times[label]
    let diff = t - timer.start
    
    timer.total += diff
    timer.total -= timer.window[timer.window_index]
    timer.window[timer.window_index] = diff
    timer.window_index = (timer.window_index + 1) % 600

    if print { global.rmml.log(diff) }
  },
  render: fun () {
    let names = variable_struct_get_names(global.time._times)
    let i = array_length(names) - 1
    while i >= 0 {
      let label = names[i]
      global.deb.log(global.time._times[label].total / 600, label)
      i -= 1
    }
  },
}

global.dump = {
  ds_map: fun (map) {
    let str = string(map) + ": ds_map = {\n"
    if !ds_exists(map, ds_type_map) { return "dne" }
    let keys = ds_map_keys_to_array(map)
    if array_length(keys) == undefined { return "no keys" }
    let i = array_length(keys) - 1
    while i >= 0 {
      let val = ds_map_find_value(map, keys[i])
      str += string(keys[i]) + ":" + string(val) + "\n"
      i -= 1
    }
    -- global.rmml.log(str + "}")
    return str + "}"
  },
  buffer: fun (buffer) {
    let size = buffer_get_size(buffer)
    let str = string(buffer) + ": buffer = {\n"
    let i = 0
    while i < size {
      str += string(buffer_peek(buffer, i, buffer_u8)) + "\n"
      i += 1
    }
    global.rmml.log(str + "}")
  },
  tilemap: fun (tilemap) {
    let dump = []
    -- tilemap id
    let tid = layer_tilemap_get_id(tilemap)
    let tile_width = tilemap_get_width(tid)
    let tile_height = tilemap_get_height(tid)
    let x = 0
    while x < tile_width {
      dump[x] = []
      let y = 0
      while y < tile_height {
        dump[x][y] = tile_get_index(tilemap_get(tid, x, y))
        y += 1
      }
      x += 1
    }
    return dump
  },
  layers: fun () {
    global.rmml.log(["LAYYYYY", room_get(), room_get_name(room_get())])
    let layers = layer_get_all()
    let i = 0
    while i < array_length(layers) {
      -- global.rmml.log(["LAYER", layer_get_name(layers[i]), layer_get_depth(layers[i])])
      let tilemap_id = layer_tilemap_get_id(layers[i])
      -- global.rmml.log([
      --   tilemap_get_x(tilemap_id), tilemap_get_y(tilemap_id),
      --   tilemap_get_tileset(tilemap_id),
      --   tilemap_get_width(tilemap_id), tilemap_get_height(tilemap_id),
      -- ])
      let dump = global.dump.tilemap(layers[i])
      -- global.rmml.log(dump)

      global.rmml.log(
        "global.room_lib.tile("
        + "<<REPLACE>>, "
        + string(layer_get_depth(layers[i]))
        + ", \""
        + layer_get_name(layers[i])
        + "\", "
        + string(tilemap_get_tileset(tilemap_id))
        + ", "
        + string(tilemap_get_width(tilemap_id))
        + ", "
        + string(tilemap_get_height(tilemap_id))
        + ", "
        + string(global.dump.tilemap(layers[i]))
        + ")"
      )
      i += 1
    }
  },
  camera: fun (camera_id) {
    global.rmml.log({
      view_x: camera_get_view_x(camera_id),
      view_y: camera_get_view_y(camera_id),
      view_width: camera_get_view_width(camera_id),
      view_height: camera_get_view_height(camera_id),
      camera_get_view_target: camera_get_view_target(camera_id),
    })
  },
  struct: fun (struct, names_only) {
    let s = ""
    let names = struct_get_names(struct)
    array_sort(names, true)
    let len = array_length(names)
    let i = 0
    let log = file_text_open_append(global.rmml.log_name)
    while i < len {
      let k = names[i]
      if names_only {
        file_text_write_string(log, string(k) + ": " + typeof(struct[k]) + "\n")
      } else if string_starts_with(k, "__catspeak") {
        file_text_write_string(log, string(k) + ": [[ catspeak internal ]]\n")
      } else if string_starts_with(k, "gml_") {
        file_text_write_string(log, string(k) + ": [[ gamemaker live internal ]]\n")
      } else if string_starts_with(k, "__scribble") {
        file_text_write_string(log, string(k) + ": [[ scribble internal ]]\n")
      } else if k == "rmml" {
        file_text_write_string(log, string(k) + ": [[ rmml internal ]]\n")
      } else {
        file_text_write_string(log, string(k) + ": " + string(struct[k]) + "\n")
      }
      i += 1
    }
    file_text_close(log)
    return s
  }
  instance: fun (inst, names_only) {
    with inst {
      global.rmml.log("INSTANCE:\n")
      global.dump.struct(self, names_only)
    }
  },
  global: fun (names_only) {
    global.rmml.log("GLOBALS:\n")
    global.dump.struct(global, names_only)
  },
}

global.tilemap_load = fun (tilemap_id, data) {
  let x = 0
  while x < array_length(data) {
    let y = 0
    while y < array_length(data[x]) {
      tilemap_set(tilemap_id, data[x][y], x, y)
      y += 1
    }
    x += 1
  }
}

global.rebuild_cameras = fun (room, camera) {
  let i = 0
  while i < 8 {
    if room_get_camera(room, i) == -1 {
      room_set_camera(
        room, i
        camera
        -- global.__c
        -- camera_create_view(0, 0, room_width_get(), room_height_get())
      )
    }
    i += 1
  }
}

global.deb = {
  _log: [],
  log: fun (text, label, run) {
    array_push(global.deb._log, {
      label,
      text,
      run: if run == undefined { true } else { run }
    })
  },
  clear: fun () { global.deb._log = [] },
  should_clear: true,
  color: c_white,
}

global.infinite = {
  event: fun (event_code) {
    method_get_self(
      ds_map_find_value(global.mod_map, event_code)
    ).callTime = infinity
    method_get_self(
      global.rmml_map[event_code][global.rmml_current_mod]
    ).callTime = infinity
  },
  fn: fun (function) {
    method_get_self(function).callTime = infinity
  },
  call: fun (function, a,b,c,d,e,f,g,h) {
    method_get_self(global.infinite.call).callTime = infinity
    method_get_self(function).callTime = infinity
    function(a,b,c,d,e,f,g,h)
  },
  call_in: fun (event_code, function, a,b,c,d,e,f,g,h) {
    method_get_self(
      ds_map_find_value(global.mod_map, event_code)
    ).callTime = infinity
    method_get_self(
      global.rmml_map[event_code][global.rmml_current_mod]
    ).callTime = infinity
    method_get_self(global.infinite.call_in).callTime = infinity
    method_get_self(function).callTime = infinity
    function(a,b,c,d,e,f,g,h)
  }
}
```

# controller

## create

```sp
let debugger = instance_create_depth(0, 0, -1000, odebugger_new, {
  persistent: true
})

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
      global.maya_mode = false
    } else {
      global.maya_mode = true
      global.ameli_mode_ = false
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
    file_delete(map_get_string(6))
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
```

## room_start

```catspeak
-- add room transitions
let data = {}
with oroom_transition {
  global.deb_trans_add(self.target_room, room_get(), self.x - self.bbox_left, self.x - self.bbox_right, self.y - self.bbox_top, self.y - self.bbox_bottom)
}
```

## draw_end

```sp
if global.deb_quickboot {
  with omenu_new {
    self.state = 8
    global.current_file = 6
    self.start_timer = 100
    global.speedrun_mode_ = true
    global.speedrun_timer_ = false
    global.deb_quickboot = false
  }
}

if global.debug_draw_hitboxes__ {
  -- main box
  draw_set_color(c_blue)
  -- position-bounds
  draw_rectangle(-32, -64, room_width_get() + 32, room_height_get() + 64, true)
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
    draw_text(self.x, self.y, string([self.dir, self.marg, self.y_off]))
    draw_text(self.x, self.y - 12, string(room_get_name(self.target_room)))
    draw_text(self.x, self.y - 24, string(self.id))

    -- adjacent rooms
    if global.deb_trans[room_get()] {
      let data = global.deb_trans[room_get()][self.target_room]
      if data {
        draw_rectangle(self.x+data.left, self.y+data.top, self.x+data.right, self.y+data.bottom, true)
      }
    }
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
```

## draw_begin

```sp
if global.debug_unclamp_cam {
  with ogame {
    self.draw_catacombs_light = false
  }
}
```

## draw_gui_end

```sp
global.time.render()
let col = draw_get_color()
draw_set_color(global.deb.color)
let y = 0
while y < array_length(global.deb._log) and y < 100 {
  let log = global.deb._log[y]
  let text = log.text
  let run = log.run
  let label = log.label
  if run and typeof(text) == "method" {
    text = text()
  }
  draw_text(0, y * 10, string(label) + ": " + string(text))
  y += 1
}
draw_set_color(col)
if global.deb.should_clear { global.deb.clear() }

-- gimmick debug options
-- if keyboard_check_pressed(vk_f1) {
--   global.trinket_active_[24] = !global.trinket_active_[24]
-- }
-- if keyboard_check_pressed(vk_f2) {
--   global.reload_[2] = 0
-- }
-- if global.trinket_active_ != undefined {
--   global.deb.log(global.trinket_active_[24], "f1 heavy ammo")
--   global.deb.log(0, "f2 reload")
--   global.deb.log(global.deb__test, "f3 disable gimmick")
--   global.deb.log(global.trinket_active_[4], "f5 slippers")
--   global.deb.log(room_get_name(room_get()), "room")
-- }
-- if keyboard_check_pressed(vk_f3) {
--   global.deb__test = !global.deb__test
-- }
-- if global.deb__test {
--   with oplayer {
--     self.__gimmick_jumps = 0
--   }
-- }
-- if keyboard_check_pressed(vk_f5) {
--   global.trinket_active_[4] = !global.trinket_active_[4]
-- }
```
