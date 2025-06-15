```sp
global.more_saves = {
  version: 1,

  -- array mapping a save file to if that save file exists
  -- save_exists[N] == file_exists(map_get_string(N))
  save_exists: undefined,

  -- cached save data
  -- array of arrays
  -- 0: character (0 fern, 1 maya, 2 ameli)
  -- 1: difficulty (0 normal, 1 flexible, 2 speedrun)
  -- 2: playtime
  -- 3: trinkets
  -- 4: rooms
  -- 5: upgrades
  -- 6: titania pieces
  save_data: undefined,

  -- gets the character name
  hook_character_names: [
    ui_load_entry("face_names", 12),-- Fern
    ui_load_entry("boss_names", 2), -- Maya
    ui_load_entry("boss_names", 1), -- Ameli
  ],

  -- gets the difficulty name
  hook_difficulty_names: [
    ui_load_entry("menu_difficulties", 0), -- normal
    ui_load_entry("menu_difficulties", 1), -- flexible
    ui_load_entry("Speedrun_text", 0), -- speedrun
  ],

  -- hook that runs for a save file after it has loaded
  -- access `global.save_data` to pull data
  hook_load_save: fun (existing_save_data) {
    return existing_save_data
  },

  -- set to true if the save menu should have sensitive buttons
  -- ie allows you to add extra button elements to the left and right
  -- of the selected save file
  hook_save_select_sensitive_buttons: false,

  -- loads the preview data for each save file
  load_save_files: fun () {
    let save_data = array_create(50, undefined)
    let save_exists = array_create(50, false)

    global.more_saves.save_data = save_data
    global.more_saves.save_exists = save_exists

    let i = 0
    while i < 50 {
      let file_name = map_get_string(i)
      if file_exists(file_name) {
        global.save_data = loadjsonfromfile(file_name)
        let data = [
          if map_return_safe("maya_mode", 0) { 1 } else if map_return_safe("ameli_mode", 0) { 2 } else { 0 },
          if map_return_safe("speedrun_mode", -1) { 2 } else { map_return_safe("difficulty", 0) },
          map_return_safe("playtime", 1990),
          map_return_safe("trinkets_found", 13),
          map_return_safe("rooms_found", 0) * 100 / 651,
          map_return_safe("upgrades_found", 0),
          map_return_safe("stars", 0) + story_flag_triggered("titania_head_activated"),
        ]
        save_data[i] = global.more_saves.hook_load_save(data)

        if ds_exists(global.save_data, 1) {
          ds_map_destroy(global.save_data)
          global.save_data = -1
        }

        save_exists[i] = true
      } else {
        save_data[i] = [
          0,0,0,0,
          0,0,0
        ]
      }

      i += 1
    }
  }
}
```

# controller

## create

```sp
-- set depth to run after omenu_new
-- prevents double inputs
self.depth = -1001
```

## draw

```sp
-- prevent catspeak crash if window is held
method_get_self(
  ds_map_find_value(global.mod_map, "controller_events_draw")
).callTime = infinity
method_get_self(
  global.rmml_map["controller_events_draw"][global.rmml_current_mod]
).callTime = infinity

let menu = instance_find(omenu_new)
if !instance_exists(menu) {
  global.rmml.unload()
  -- dereference save_data so it can be garbage collected
  global.more_saves.save_data = undefined
  global.more_saves.save_exists = undefined
  catspeak_collect()
  return
}

match menu.state {
  -- save view state
  case 21 {
    self.should_cache_exists = true
    -- don't override substate 2 (delete substate)
    if menu.substate == 1 or menu.substate == 0 {
      menu.state = -516
    }
  }
  -- our state
  case -516 {
    -- re-cache exists map
    if self.should_cache_exists {
      global.more_saves.load_save_files()
      self.should_cache_exists = false
    }

    let col = draw_get_color()

    let next_state = menu.state
    let next_substate = menu.substate

    let oinput = instance_find(oinput)
    let b1p = oinput.button_1[1]
        or oinput.button_3[1]
        or keyboard_check_pressed(vk_space)
        or keyboard_check_pressed(vk_return)
        or mouse_check_button_pressed(mb_left)

    -- menu lerping
    menu.gb_x = lerp(menu.gb_x, -180, 0.09)
    if menu.gb_x > -180 { menu.gb_x -= 0.08 }
    menu.file_sub = lerp(menu.file_sub, 1, 0.6)

    -- escape key
    if keyboard_check_pressed(vk_escape) {
      if menu.substate == 0 {
        next_state = 14
        audio_play_sound_pitch(snd_menu_back, 0.6, 1, 0)
      } else if menu.substate == 1 {
        next_substate = 0
        menu.sub_select = 0
      }
    }

    --
    -- GENERAL MENU
    --

    -- controller save select
    if !global.controlled_by_mouse_ and menu.substate == 0 {
      let vv = oinput.down[1] - oinput.up[1]
      let hh = oinput.right[1] - oinput.left[1]
      let m = loopclamp(menu.menu_select + vv, 0, 49)

      -- hardcoded horizontal movement
      if hh > 0 {
        m = (m + (
          if m == 16 or m == 41 or m == 23 or m == 41 or m == 48 {
            6
          } else if m == 18 or m == 43 or m == 22 or m == 43 or m == 47 {
            5
          } else if m == 20 or m == 45 or m == 21 or m == 45 or m == 46 {
            4
          } else if m == 15 or m == 17 or m == 19 or m == 40 or m == 42 or m == 44 {
            11
          } else {
            7
          }
        )) % 50
      } else if hh < 0 {
        m = (50 + m - (
          if m == 0 or m == 24 or m == 25 or m == 49 {
            4
          } else if m == 1 or m == 3 or m == 5 or m == 26 or m == 28 or m == 30 {
            11
          } else if m == 2 or m == 23 or m == 27 or m == 48 {
            5
          } else if m == 4 or m == 22 or m == 29 or m == 47 {
            6
          } else {
            7
          }
        )) % 50
      }

      menu.menu_select = m

      -- file selection changed
      if vv != 0 or hh != 0 {
        menu.file_sub = 0.5
        audio_play_sound_pitch(snd_menu_1, 0.5, 0.9 + random(0.1), 0)
      }

      -- handle click
      if b1p {
        if menu.menu_select != 6 {
          if !global.more_saves.save_exists[menu.menu_select] {
            -- new save file
            next_state = 3
            global.current_file = menu.menu_select
            audio_play_sound_pitch(snd_menu_2, 0.6, 1, 0)
          } else {
            -- select save file
            global.current_file = menu.menu_select
            next_substate = 1
            menu.box_sub = 0
            -- comfirm
            audio_play_sound_pitch(snd_menu_comfirm_alt, 0.6, 1, 0)
          }
        } else {
          next_state = 14
          audio_play_sound_pitch(snd_menu_back, 0.6, 1, 0)
        }
      }
    }

    let save_index = 0
    let base_x = round(global.game_width * 0.1) + (menu.gb_x + 179) * 4
    let base_y = round(global.game_height * 0.19)

    let x = 0
    while x < 8 {
      let y = 0
      while y < 7 {
        -- check if save exists
        let dne = !global.more_saves.save_exists[save_index]

        let s_x = base_x + ((y % 2) * 26) + x * 52
        let s_y = base_y + y * 26

        -- selection
        if global.controlled_by_mouse_ and menu.substate == 0 {
          if abs(s_x - global.mouse_gui_x_) + abs(s_y - global.mouse_gui_y_) < 26 {
            -- selection changed
            if menu.menu_select != save_index {
              -- play audio
              menu.file_sub = 0.5
              audio_play_sound_pitch(snd_menu_1, 0.5, (0.9 + random(0.1)), 0)
            }
            menu.menu_select = save_index

            -- handle click
            if b1p {
              if menu.menu_select != 6 {
                if dne {
                  -- new save file
                  next_state = 3
                  global.current_file = menu.menu_select
                  audio_play_sound_pitch(snd_menu_2, 0.6, 1, 0)
                } else {
                  -- select save file
                  global.current_file = menu.menu_select
                  next_substate = 1
                  menu.box_sub = 0
                  -- comfirm
                  audio_play_sound_pitch(snd_menu_comfirm_alt, 0.6, 1, 0)
                }
              } else {
                next_state = 14
                audio_play_sound_pitch(snd_menu_back, 0.6, 1, 0)
              }
            }
          }
        }

        -- selection transparency
        let transparency = if menu.menu_select == save_index { 1 } else { 0.4 }
        if menu.substate != 0 {
          transparency *= 0.5
        }

        if x == 0 and y == 6 {
          -- back button
          draw_sprite_ext(
            smenu_file, 2,
            s_x, s_y,
            1, 1, 0, c_white,
            transparency
          )
        } else {
          if dne and menu.menu_select != save_index { transparency *= 0.6 }
          
          -- draw folder icon
          draw_sprite_ext(
            smenu_file, dne,
            s_x, s_y,
            1, 1, 0, c_white,
            transparency
          )
        }

        -- draw select icon
        if menu.menu_select == save_index {
          draw_sprite_ext(
            smenu_file_round, 0,
            s_x, s_y,
            menu.file_sub, menu.file_sub, 0, c_white,
            transparency
          )
        }

        -- next save file
        save_index += 1

        -- skip every other for the last column and middle columns
        y += (x == 7 or x == 3) + 1
      }
      x += 1
    }

    ---
    --- save preview
    ---

    -- lerp the save preview
    let target_x = global.game_width * (
        if menu.substate == 1 {
          0.5
        } else if menu.menu_select >= 25 {
          0.25
        } else { 0.75 }
    ) + (menu.gb_x + 180) * 4
    if self.preview_x == undefined {
      self.preview_x = target_x
    } else {
      self.preview_x = round(lerp(self.preview_x, target_x, 0.25))
    }

    let xx = self.preview_x
    let yy = global.game_height * 0.53 - 16
    -- 1/2 width of the save preview
    let ww = 100
    -- height of the save preview label (back, save XX, etc)
    let hh = 64

    -- preview label
    draw_rectangle_ca(
      xx - ww - 1, yy - hh - 4,
      xx + ww + 1, yy - hh - 32 - 4,
      4870488, 1
    )

    if menu.menu_select != 6 {
      -- save box background
      draw_set_color(0xECF5F5)
      draw_set_alpha(0.95)
      draw_rectangle(xx - ww, yy - hh, xx + ww, yy + hh + 12, false)
      draw_set_color(0x4A5158)
      draw_rectangle(xx - ww, yy - hh, xx + ww, yy + hh + 12, true)

      -- "data" separator
      draw_set_alpha(0.6)
      draw_line(xx - ww + 8, yy - hh + 17, xx + ww - 8, yy - hh + 17)
      draw_set_alpha(1)

      if global.more_saves.save_exists[menu.menu_select] {
        let save_data = global.more_saves.save_data[menu.menu_select]

        -- make label (with padded zero)
        let s = ui_load_entry("menu_no_file_exists", 3)
        s = string_copy(s, 1, string_length(s) - 1)
        if menu.menu_select < 9 { s += "0" }

        scribble(s + string(menu.menu_select + 1))
            .align(1, 0)
            .transform(2, 2, 0)
            .blend(13427188, 1)
            .draw(xx, yy - hh - 30)
        scribble(ui_load_entry("menu_no_file_exists", 4))
            .blend(4870488, 1)
            .align(1, 0)
            .draw(xx, yy - hh + 4)

        let info = [
          global.more_saves.hook_difficulty_names[save_data[1]],
          float_to_time(save_data[2]),
          string(save_data[3]) + "/" + string(38),
          string(save_data[4]) + "%",
          string(save_data[5]) + "/" + string(84),
          string(save_data[6])
        ]

        -- character
        scribble("Character")
            .blend(4870488, 1)
            .align(0, 0)
            .draw(xx - ww + 4, yy - hh + 26)
        scribble(global.more_saves.hook_character_names[save_data[0]])
            .blend(4870488, 0.7)
            .align(2, 0)
            .draw(xx + ww - 4, yy - hh + 26)

        let data = ui_load_text("menu_save_data")
        let i = 0
        while i < 6 {
          scribble(data[i])
              .blend(4870488, 1)
              .align(0, 0)
              .draw(xx - ww + 4, yy + i * 16 - hh + 42)
          scribble(info[i])
              .blend(4870488, 0.7)
              .align(2, 0)
              .draw(xx + ww - 4, yy + i * 16 - hh + 42)
          i += 1
        }
      } else {
        let s = ui_load_entry("menu_no_file_exists", 1)
        s += if menu.menu_select < 9 { " 0" } else { " " }
        scribble(s + string(menu.menu_select + 1))
            .align(1, 0)
            .transform(2, 2, 0)
            .blend(13427188, 1)
            .draw(xx, yy - hh - 30)
        scribble(ui_load_entry("menu_no_file_exists", 2))
            .blend(4870488, 1)
            .align(1, 0)
            .draw(xx, yy - hh + 4)
      }
    } else {
      scribble(ui_load_text("gen_back"), 14)
          .align(1, 0)
          .transform(2, 2, 0)
          .blend(13427188, 1)
          .draw(xx, yy - hh - 30)
    }

    ---
    --- substate 1 (save options)
    ---

    if menu.substate == 1 {
      -- input selection
      if !global.controlled_by_mouse_ {
        menu.sub_select = loopclamp(menu.sub_select + oinput.right[1] - oinput.left[1], 0, 2)
      } else {
        menu.sub_select = if global.mouse_gui_x_ < 165 { 0 } else if global.mouse_gui_x_ < 279 { 1 } else { 2 }
      }

      if b1p and (
        -- insensitive buttons
        !global.more_saves.hook_save_select_sensitive_buttons
        -- or "hovering" the buttons
        or global.mouse_gui_y_ > 190
      ) {
        match menu.sub_select {
          -- load save
          case 0 {
            next_state = 8
            audio_play_sound_pitch(snd_menu_comfirm, 0.9, 0.7, 0)
          }
          -- delete
          case 1 {
            next_substate = 2
            -- use existing delete menu
            next_state = 21
            menu.sub_select = 0
          }
          -- back
          case 2 {
            next_substate = 0
            menu.sub_select = 0
          }
        }
      }

      -- override yy
      -- keep xx (so the lerping stays)
      let yy = global.game_height * 0.81 + 18

      let options = ui_load_text("menu_save_select")
      menu.box_sub = lerp(menu.box_sub, menu.sub_select, 0.25)
      draw_set_color(0x4A5158)
      draw_rectangle(
        round(xx - 158 + menu.box_sub * 110 - 2),
        yy - 10 - 2,
        round(xx - 62 + menu.box_sub * 110 + 2),
        yy + 10 + 2,
        true
      )
      draw_set_color(c_white)

      let i = 0
      while i < 3 {
        draw_rectangle_ca(
          xx - 158 + i * 110, yy - 10,
          xx - 62 + i * 110, yy + 10,
          4870488, if i == menu.sub_select { 1 } else { 0.8 }
        )
        scribble(options[i])
            .align(0, 0)
            .blend(13427188, 1)
            .draw(xx + i * 110 - 154, yy - 5)
        i += 1
      }
    }

    menu.state = next_state
    menu.substate = next_substate
    draw_set_color(col)
  }
}
```
