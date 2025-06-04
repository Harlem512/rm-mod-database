```sp
global.clippy = {
  help_text: fun (x, y, text) {
    let len = string_length(text)
    let label_y = y - wave(-2, 1, 2, 0) - 27
    let label_x = x + 10
    draw_sprite_part(
      sdark_orb_hp_blank, 0,
      5, 9,
      6, 18,
      label_x, label_y
    )
    draw_sprite_part(
      sdark_orb_hp_blank, 0,
      18, 9,
      6, 18,
      label_x + len * 6 + 5, label_y
    )
    let col = draw_get_color()
    draw_set_color(#F9E6CF)
    draw_rectangle(label_x + 6, label_y, label_x + len * 6 + 4, label_y + 13, false)
    draw_set_color(col)
    scribble(
      text
    )
      .align(0, 1)
      .blend(3700138, 1)
      .draw(x + 14, y - 12 - wave(4, 7, 2, 0))
  }
}
```

# controller

## draw

```sp
let orb = instance_find(odark_orb)
if !instance_exists(orb) { return }

with oplayer {
  let x = self.x
  let y = self.y

  let on_plat = script_execute(self.gen_col_sort, x, y + 2, self.layer_col, 2)

  if on_plat {
    global.clippy.help_text(orb.x, orb.y, "Down + Space")
    return
  }
}
```
