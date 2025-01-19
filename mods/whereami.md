# controller

## draw_gui_end

```sp
if global.gamestate == 2 and instance_number(omenu_new) == 0 {
  draw_text(0, 200, room_get_name(room_get()))
  draw_text(0, 210, string([global.player_map_x_ , global.player_map_y_]))
}
```