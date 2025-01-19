```sp
-- don't run the sprite creation multiple times
if global.__scarf_uncharged != undefined {
  return
}

let pal_folder = "mods/rmml/maya_palette/"

-- load palette
let palette = sprite_add(pal_folder + "palette.png", 1, false, false, 0, 0)

-- read scarf colors from sprite
let surf = surface_create(1, 2)
surface_set_target(surf)
draw_sprite(palette, 0, -1, -54)
let buff = buffer_create(8, buffer_fixed, 1)
buffer_get_surface(buff, surf, 0)
global.__scarf_uncharged = buffer_peek(buff, 0, buffer_u32)
global.__scarf_charged = buffer_peek(buff, 4, buffer_u32)
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

let out_dir = temp_directory_get() + "rmmp/"

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
  let pal_sprite = sprite_add(pal_folder + "DO_NOT_TOUCH/" + f, subimage_number, false, false, 0, 0)

  -- surface draw
  let surf = surface_create(width * subimage_number, height)
  surface_set_target(surf)

  -- draw sprites using shader
  let img_index = 0
  while img_index < subimage_number {
    draw_sprite(pal_sprite, img_index, img_index * width, 0)
    img_index += 1
  }

  -- delete surface
  surface_reset_target()
  surface_save(surf, dest_img)
  surface_free(surf)

  -- replace sprite with paletted version
  sprite_replace(index, dest_img, subimage_number, false, false, xoffset, yoffset)

  f = file_find_next()
}

-- stop the shader
shader_replace_simple_reset_hook()

-- delete palette sprite
sprite_delete(palette)
```

# controller

## draw_begin

```sp
if !global.maya_mode or instance_number(oplayer) == 0 {
  return
}

let plr = instance_find(oplayer, 0)

-- apply scarf colors
if global.current_weapon_ != 0 and global.clip_[global.current_weapon_] != 0 {
  -- charged
  plr.hair_alt_start_col = global.__scarf_charged
  plr.hair_alt_end_col = global.__scarf_charged
} else {
  -- uncharged
  plr.hair_alt_start_col = global.__scarf_uncharged
  plr.hair_alt_end_col = global.__scarf_uncharged
}
```