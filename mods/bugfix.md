# controller

## room_start

```sp
if global.ameli_mode_ and global.player_map_x_ > 109 {
  with obullet_9slice_library {
    let copy = instance_create_depth(self.x, self.y, 25, obullet_9slice_hazard, {
      image_xscale: self.image_xscale,
      image_yscale: self.image_yscale,
      image_angle: self.image_angle,
      dmg: self.dmg,
      sprite_index: self.sprite_index,
    })

    instance_destroy(self)
  }
}
```

## draw

```sp
if global.ameli_mode_ and global.player_map_x_ > 109 {
  with oenemy_voidwretch {
    self.depth = 25
  }
}
```

## step_begin

```sp
let has_elicia = instance_number(oboss_sword)
with oboss_sword_sword {
  if self.active and self.index == 1 and !has_elicia and self.timer < 40 {
    instance_destroy(self)
  }
}
```
