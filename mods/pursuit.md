# controller
<!-- MARK: Controller -->

## room_start

```sp
if global.save_data == -1 {
  return
}

-- 9999 dead instances
if !instance_exists(global.worm_manager) {
  -- set high depth so room_end for inst runs after worm
  let inst = instance_create_depth(0, 0, 9999, omod_instance)
  with inst {
    alarm_set(0, 30)
  }
  inst.persistent = true
  global.worm_manager = inst
}

if !global.disable_blackout and instance_number(ocatacombs_shadow) == 0 {
    let shadow = instance_create_depth(0, 0, 0, ocatacombs_shadow)
    shadow.persistent = true
}
```

## draw_gui_end

```sp
if instance_number(omenu_new) > 0 {
  self.depth = -9999
  let col = draw_get_color()
  if global.disable_blackout {
    draw_set_color(c_white)
    draw_rectangle(0, 0, 60, 10)
    draw_set_color(c_black)
    draw_text(0, 0, "Light On")
  } else {
    draw_set_color(c_black)
    draw_rectangle(0, 0, 60, 10)
    draw_set_color(c_white)
    draw_text(0, 0, "Light Off")
  }

  if mouse_check_button_pressed(mb_left) and point_in_rectangle(mouse_x_get(), mouse_y_get(), 0, 0, 60, 10) {
    global.disable_blackout = !global.disable_blackout
  }

  if global.worm_easy {
    draw_set_color(c_white)
    draw_rectangle(80, 0, 120, 10)
    draw_set_color(c_black)
    draw_text(80, 0, "Easy")
  } else {
    draw_set_color(c_black)
    draw_rectangle(80, 0, 120, 10)
    draw_set_color(c_white)
    draw_text(80, 0, "Hard")
  }

  if mouse_check_button_pressed(mb_left) and point_in_rectangle(mouse_x_get(), mouse_y_get(), 80, 0, 120, 10) {
    global.worm_easy = !global.worm_easy
  }

  draw_set_color(col)
}
```

# instance
<!-- MARK: Instance -->

## room_start

```sp
-- prevent total worm death
with oworm {
  alarm_set(3, -1)
}
```

## room_end

```sp
with oworm {
  self.transitioning = true
}
```

<!-- Fairness -->
## step

```sp
if global.worm_easy and global.invis {
  with oworm {
    self.attack_delay = 10
    self.attack_timer = 0
    self.state = 3
  }
}
```

<!-- Teleports -->
## alarm_0

```sp
alarm_set(0, 29)
let plr = instance_find(oplayer)
let worm = instance_find(oworm)

-- no player? no do thing
if !plr {
  return
}

-- no worm? make worm
if !worm {
  self.x = plr.x
  self.y = plr.y
  worm = instance_create_depth(self.x, self.y, 0, oworm)
  -- prevent total worm death
  with worm {
    alarm_set(3, -1)
  }
  return
}

-- worm teleport
-- how far moved since last check
let d1 = point_distance(self.x, self.y, worm.x, worm.y)
-- how far from player
let d2 = point_distance(plr.x, plr.y, worm.x, worm.y)

-- warp speed, worm needs to not attack (2) and be moving (3)
if worm.state == 3 and self.last != 2 and (d2 > 200 or (d1 < 32 and d2 > 64)) {
  let mx = plr.x + worm.x
  let my = plr.y + worm.y
  worm.x = mx / 2
  worm.y = my / 2
}

self.x = worm.x
self.y = worm.y
self.last = worm.state
```
