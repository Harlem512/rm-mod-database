```sp
ini_open("mods/rmml/grapple_preview/config.ini")
global.grapple_preview = ini_read_real("grapple_preview", "show_preview", 1)
ini_close()
```

# controller

## draw

```sp
-- don't draw hook preview
if global.hook_type__ == 0 or !global.grapple_preview { return }

with oplayer {
  -- only show preview if
  -- we're hooking AND can hook (frame delay) AND can hook (touched ground) 
  if self.state == 6 or self.can_hook_delay or self.hook_air_cancel { return }

  let adr = point_direction(self.x, self.y - 24, global.mousex, global.mousey)
  draw_set_alpha(choose(0.5, 0.55, 0.6) * wave(1, 1.4, 3, 0))
  draw_line_color(
    self.x + lengthdir_x(40, adr),
    self.y - 24 + lengthdir_y(40, adr),
    self.x + lengthdir_x(125, adr),
    self.y - 24 + lengthdir_y(125, adr),
    c_dkgray, c_orange
  )
  draw_circle_color(
    self.x + lengthdir_x(140, adr),
    self.y - 24 + lengthdir_y(140, adr),
    7,
    c_orange, c_orange, true
  )
  draw_set_alpha(1)
}
```

## draw_gui_end

```sp
-- grapple settings gamestate
if global.gamestate != 28 or global.hook_type__ == 0 { return }

let col = draw_get_color()
draw_set_color(c_black)
if global.component.button(
  2, 226, 132, 22, if global.grapple_preview { "Show Grapple Preview" } else { "Hide Grapple Preview" }
) {
  let enable = !global.grapple_preview
  global.grapple_preview = enable
  ini_open("mods/rmml/grapple_preview/config.ini")
  ini_write_real("grapple_preview", "show_preview", enable)
  ini_close()
}
draw_set_color(col)
```
