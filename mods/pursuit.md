# controller
<!-- MARK: Controller -->

## room_start

```sp
self.depth = -1
if global.save_data == -1 { return }

-- 9999 dead instances
if !instance_exists(global.worm_manager) {
  global.worm_manager = instance_create_depth(0, 0, 0, omod_basic)
}

if !global.disable_blackout and instance_number(ocatacombs_shadow) == 0 {
  let shadow = instance_create_depth(0, 0, 0, ocatacombs_shadow)
  shadow.persistent = true
}
```

## draw_end

```sp
let menu = instance_find(omenu_new)
if !instance_exists(menu) { return }

let col = draw_get_color()
draw_set_color(c_black)

if menu.state == 14 {
  -- pursuit menu
  draw_set_color(c_black)
  if global.component.button(
    418, 50, 22, 22, "Pr", "Pursuit"
  ) {
    menu.state = -515
  }
} else if menu.state == -515 {
  draw_sprite(slab_cage_0, 0, 222, 60)

  -- screen darken
  if global.component.button(
    2, 2, 64, 22, if global.disable_blackout { "Light On" } else { "Light Off" },
    "Enables/disables a global screen darken."
  ) {
    global.disable_blackout = !global.disable_blackout
  }

  -- easy mode
  if global.component.button(
    82, 2, 38, 22, if global.worm_easy { "Easy" } else { "Hard" },
    "Adds an attack cooldown after being hit."
  ) {
    global.worm_easy = !global.worm_easy
  }

  -- back button
  if global.component.button(
    418, 2, 22, 22,
  ) {
    menu.state = 14
  }
  draw_sprite_ext(
    smenu_bar, 5, 429, 13,
    1, 1, 0, c_black, 1
  )
}
draw_set_color(col)
```

<!-- MARK: Basic -->
# basic

## create
```sp
-- prevent crashing in the wind area
self.windable = false
self.persistent = true
alarm_set(0, 30)
```

## alarm_0

```sp
alarm_set(0, 29)

let plr = instance_find(oplayer)
-- no player? no do thing
if !instance_exists(plr) { return }

-- create the worm
if !self.pursuit {
  event_perform_object(oworm, ev_create, 0)
  self.x = plr.x
  self.y = plr.y
  self.last_x = plr.x
  self.last_y = plr.y
  self.pursuit = true
  -- 100 depth is needed to prevent the winter dlc from making the worm invisible
  self.depth = if instance_number(obg_render_test) > 0 { 100 } else { -10 }
  return
}

-- worm teleport
-- how far moved since last check
let d1 = point_distance(self.last_x, self.last_y, self.x, self.y)
-- how far from player
let d2 = point_distance(plr.x, plr.y, self.x, self.y)

-- warp speed, worm needs to not attack (2) and be moving (3)
if self.state == 3 and self.last_state != 2 and (d2 > 200 or (d1 < 32 and d2 > 64)) {
  self.x = (plr.x + self.x) / 2
  self.y = (plr.y + self.y) / 2
}

self.last_x = self.x
self.last_y = self.y
self.last_state = self.state
```

## step
```sp
if !self.pursuit { return }
event_perform_object(oworm, ev_step, ev_step_normal)
if global.worm_easy and global.invis {
  self.attack_delay = 10
  self.attack_timer = 0
  self.state = 3
}
```

## room_end
```sp
if !self.pursuit { return }
event_perform_object(oworm, ev_other, ev_room_end)
self.transitioning = true
```

## room_start
```sp
if !self.pursuit { return }
if instance_number(oworm) > 0 {
  instance_destroy(oworm)
  return
}
-- 100 depth is needed to prevent the winter dlc from making the worm invisible
self.depth = if instance_number(obg_render_test) > 0 { 100 } else { -10 }
event_perform_object(oworm, ev_other, ev_room_start)
```

## draw
```sp
if !self.pursuit { return }
event_perform_object(oworm, ev_draw, 0)
```
