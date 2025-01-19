# controller

## create

```sp
if (global.minify == undefined) {
  global.minify = {}
  global.minify.matrix_shrunk = false
  global.minify.mask_shrunk = false
  -- evicting queue to store player y
  global.minify.last_y = [undefined, undefined, undefined,undefined,undefined,undefined, undefined, undefined, undefined, undefined]
  global.minify.last_y_index = 0

  global.minify.mask_names = [
    splayer_mask,
    splayer_mask_bullet,
    splayer_mask_bullet_crouch,
    splayer_mask_crouch,
    splayer_mask_platform,
    splayer_legde_mask,
  ]
  -- left,top right,bottom
  -- off-x, off-y
  global.minify.mask_small = [
    [7,-3,15,13,  11,27],
    [9,1,13,10,  11,27],
    [9,2,13,11,  11,27],
    [7,2,15,13,  11,27],
    [7,12,15,13,  11,27],
    [23,7,25,7,  11,27],
  ]
  global.minify.mask_normal = [
    [2,0,19,31,  11,32],
    [6,-22,15,-4,  11,3],
    [6,-19,15,-1,  11,3],
    [2,-19,19,2,  11,3],
    [2,0,19,2,  11,3],
    [23,-22,25,-22,  11,3],
  ]

  global.minify.apply = fun (mask_data) {
    let i = 0
    while i < array_length(global.minify.mask_names) {
      let spr = global.minify.mask_names[i]
      let data = mask_data[i]

      sprite_set_bbox(spr, data[0],data[1], data[2],data[3])
      sprite_set_offset(spr, data[4],data[5])
      i += 1
    }
  }
}

global.minify.apply(global.minify.mask_normal)
global.minify.mask_shrunk = false
```

## room_start

```sp
if !global.minify.mask_shrunk {
  global.minify.apply(global.minify.mask_small)
  global.minify.mask_shrunk = true
}

instance_create_depth(0, 0, -43, omod_instance)
instance_create_depth(0, 0, -45, omod_instance)
```

## step_begin

```sp
if instance_number(oplayer) > 0 {
  let p = instance_find(oplayer, 0)
  -- maybe game-destroying? no clue
  global.trinket_active_[24] = true
  -- sandwich the player between our mod instances
  p.depth = -44
  -- p.grav = 0.1
  p.base_walk_spd = 0.45
  p.base_jump_pwr = 5
  p.jump_pwr = 5

  -- un-sticker
  if p.vsp > 3 and instance_number(oroom_transition) > 0 {
    -- initial check
    if p.y == global.minify.last_y[0] {
      let i = 1
      let good = false
      -- check if all positions are the same
      while i < 10 {
        if p.y != global.minify.last_y[i] {
          good = true
          break
        }
        i += 1
      }

      -- we're stuck, pull the transition towards us
      if !good {
        let rtrans = instance_nearest(p.x, p.y, oroom_transition)
        rtrans.y -= 1
      }
    }
  }

  -- update evicting queue
  global.minify.last_y[global.minify.last_y_index] = p.y
  global.minify.last_y_index = (global.minify.last_y_index + 1) % 10
}
```

## draw_begin

```sp
-- any non-player object at this depth should be put somewhere else
-- because otherwise they'll also be shrunk (-44 "should" be safe)
-- with(all)
with -3 {
  if self.depth == -44 and self.object_index != oplayer {
    self.depth = 0
  }
}
```

## draw

```sp
-- draws the cool wings (its just the ledge drift wings but small)
if instance_number(oplayer) > 0 {
  let p = instance_find(oplayer, 0)
  -- bm_add
  gpu_set_blendmode(1)
  draw_sprite_ext(stutor_wing, 0,
    p.x - p.draw_xscale * 3, p.y - 24,
    -0.3 * p.draw_xscale, 0.3,
    wave(-20, 20, 1, 0),
    c_white, random_range(0.6, 0.9))
  draw_sprite_ext(stutor_wing, 0,
    p.x - p.draw_xscale * 3, p.y - 24,
    -0.15 * p.draw_xscale, 0.15,
    wave(-20, 20, 1, 0.45) + 80 * p.draw_xscale,
    c_white, random_range(0.6, 0.9))
  -- bm_normal
  gpu_set_blendmode(0)
}
```

# instance

## draw

```sp
-- our instances run between the player renderer, so apply the matrix and
-- reapply it after
if instance_number(oplayer) == 1 {
  let p = instance_find(oplayer, 0)
  if global.minify.matrix_shrunk {
    matrix_set(2, global.minify.world_matrix)
  } else {
    global.minify.world_matrix = matrix_get(2)
    matrix_set(2, [ 0.5,0,0,0, 0,0.5,0,0, 0,0,1,0, p.x / 2,(p.y / 2)-13,0,1 ])
  }
}
global.minify.matrix_shrunk = !global.minify.matrix_shrunk
```
