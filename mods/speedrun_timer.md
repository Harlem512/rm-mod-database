# controller

## create

```sp
self.depth = 0
```

## room_start

```sp
-- disables speedrun timer when making a new normal mode game
if room_get() == rm_start_0 and !global.speedrun_mode_ {
  global.speedrun_timer_ = false
}
```

## draw_gui_end

```sp
if instance_number(ogame) == 0 { return }
let room = room_get()
-- hide timer when playing with level editor
if room == rm_editor_2 or room == rm_editor_1 { return }

-- show speedrun timer in normal mode (and if the game is playing)
if global.gamestate == 1 and !global.speedrun_mode_ and global.speedrun_timer_ {
  let str_ = float_to_time_decimals_hour(global.playtime_)
  draw_set_halign(fa_right)
  draw_set_font(global.number_font_big_)
  draw_set_color(c_black)
  draw_text((global.game_width - 4 + 1), (global.game_height - 16 + 1), str_)
  draw_set_color(c_white)
  draw_text((global.game_width - 4), (global.game_height - 16), str_)
  draw_set_font(fnt_text_old)
  draw_set_halign(fa_left)
}

-- if paused and game is playing ...
if global.gamestate != 2 { return }

-- and is fern or not speedrunning
if !(global.maya_mode or global.ameli_mode) or !global.speedrun_mode {
  let nnx = global.game_width - 32
  let nny = global.game_height - 128

  if !global.controlled_by_mouse_ or point_distance(nnx, nny, global.mouse_gui_x_, global.mouse_gui_y_) < 32 {
    let oinput = instance_find(oinput)
    draw_sprite_ext(stimer_eye, global.speedrun_timer_, nnx, nny, 1, 1, 0, c_orange, 1)
    if (mouse_check_button(mb_left) and oinput.button_1[1]) or oinput.button_3[1] {
      global.speedrun_timer_ = !global.speedrun_timer_
      audio_play_sound_pitch(89, 0.8, random_range(0.9, 1.1), 0)
    }
  } else {
    draw_sprite_ext(stimer_eye, global.speedrun_timer_, nnx, nny, 1, 1, 0, c_white, 1)
  }
}
```
