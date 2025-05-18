```sp
let pal_folder = "mods/rmml/ameli_palette/"

-- load palette
let palette = sprite_add(pal_folder + "palette.png", 1, false, false, 0, 0)

-- read hair color from sprite
let surf = surface_create(1, 1)
surface_set_target(surf)
draw_sprite(palette, 0, -1, -55)
let buff = buffer_create(8, buffer_fixed, 1)
buffer_get_surface(buff, surf, 0)
global.__ameli_hair = buffer_peek(buff, 0, buffer_u32)
surface_reset_target()
surface_free(surf)
buffer_delete(buff)

-- start the shader
shader_replace_simple_set_hook(shd_palette)
-- init shader values if they haven't been already
if !global.player_use_shader {
  -- col_num = sprite_height
  shader_set_uniform_f(shader_get_uniform(shd_palette, "col_num"), 56)
  -- pal_num = sprite_width
  shader_set_uniform_f(shader_get_uniform(shd_palette, "pal_num"), 2)
  -- index = 1
  shader_set_uniform_f(shader_get_uniform(shd_palette, "pal_index"), 1)
  -- palette_uvs = sprite_get_uvs(palette)
  shader_set_uniform_f_array(shader_get_uniform(shd_palette, "palette_uvs"), [0,0, 1,1])
}
texture_set_stage(shader_get_sampler_index(shd_palette, "palette"), sprite_get_texture(palette, 0))

-- temp output
let out_dir = temp_directory_get() + "rmap/"

-- replace sprites
let f = file_find_first(pal_folder + "DO_NOT_TOUCH/*.png", 0)
while true {
  if f == "" {
    break
  }
  -- sprite variables
  let name = string_split(f, ".png")[0]
  let index = asset_get_index(name)
  let width = sprite_get_width(index)
  let height = sprite_get_height(index)
  let subimage_number = sprite_get_number(index)
  let xoffset = sprite_get_xoffset(index)
  let yoffset = sprite_get_yoffset(index)
  let dest_img = out_dir + f

  -- add palette version
  let pal_sprite = sprite_add(pal_folder + "DO_NOT_TOUCH/" + f, 1, false, false, 0, 0)

  -- surface draw
  let surf = surface_create(width * subimage_number, height)
  surface_set_target(surf)

  -- draw sprite using shader
  draw_sprite(pal_sprite, 0, 0, 0)

  -- delete surface
  surface_reset_target()
  surface_save(surf, dest_img)
  surface_free(surf)

  -- delete sprite
  sprite_delete(pal_sprite)

  -- replace sprite with paletted version
  -- the matched sprites are used for other objects, so we can't replace them
  match index {
    case smaya_legs_idle {
      global.__ameli_idle = sprite_add(dest_img, subimage_number, false, false, xoffset, yoffset)
    }
    case smaya_legs_run {
      global.__ameli_run = sprite_add(dest_img, subimage_number, false, false, xoffset, yoffset)
    }
    case splayer_maya_legs_crouching {
      global.__ameli_crouch = sprite_add(dest_img, subimage_number, false, false, xoffset, yoffset)
    }
    else {
      sprite_replace(index, dest_img, subimage_number, false, false, xoffset, yoffset)
    }
  }

  f = file_find_next()
}

-- fix purple square
if !global.player_use_shader {
  shader_set_uniform_f_array(shader_get_uniform(shd_palette, "palette_uvs"), [0,0, 0,0])
}

-- stop the shader
shader_replace_simple_reset_hook()

-- delete palette sprite
sprite_delete(palette)
```

# controller

## room_start

```sp
shader_replace_simple_set_hook(shd_palette)
shader_set_uniform_f_array(
  shader_get_uniform(shd_palette, "palette_uvs"),
  if global.ameli_mode_ { [0,0, 0,0] } else { [0,0, 1,1] }
)
shader_replace_simple_reset_hook()
```

## draw_begin

```sp
if !global.ameli_mode_ or instance_number(oplayer) == 0 {
  return
}

-- set player data
let plr = instance_find(oplayer, 0)
plr.sprite_legs_idle = global.__ameli_idle
plr.sprite_legs_run = global.__ameli_run
plr.sprite_legs_crouching = global.__ameli_crouch
plr.hair_start_col = global.__ameli_hair
plr.hair_end_col = global.__ameli_hair
```
