# controller

## step

```sp
-- with oplayer {
--   -- reset jump counter
--   if self.jump_delay == 8 {
--     self.__gimmick = map_return_safe("_gimmick", 1)
--   } else if self.__gimmick > 0 and global.jump_buffer_ == 0 {
--     -- check for jumps
--     let input = instance_find(oinput)
--     if input != undefined {
--       if input.button_3[1]
--           or (global.tap_jump_active and input.up[1]) {
--         global.rmml.log("jump!")
--         self.vsp = (-((self.jump_pwr + 3))) * (lerp(global.world_grav_, 1, 0.3))
--         self.land_y = 0
--         self.__gimmick -= 1
--       }
--     }
--   }
-- }

with oplayer {
  let alt_col = !script_execute(self.gen_col_sort, self.x, self.y, self.layer_col, 2)
    and script_execute(self.gen_col_sort, self.x, self.y + 2, self.layer_col, 2)

  let gr = self.vsp >= 0 and (
    script_execute(self.gen_col, self.x, self.y + 1) or alt_col)

  -- reset jump counter on the ground
  if gr or self.__gimmick_cd == undefined {
    self.__gimmick_jumps = map_return_safe("_gimmick", 4)
    self.__gimmick_cd = 0
    return
  -- check if jumps are available
  }
  self.__gimmick_cd += 1

  if self.__gimmick_cd > 10 and self.__gimmick_jumps {
    let input = instance_find(oinput)
    let jump_press = 0
    if self.can_input and global.input_skip_ <= 8 {
      jump_press = input.button_3[1] or (global.tap_jump_active and input.up[1])
    }

    if jump_press {
      global.rmml.log("JUMP")
      -- self.vsp = (-((self.jump_pwr + 3))) * (lerp(global.world_grav_, 1, 0.3))
      self.vsp = (-((self.jump_pwr + 0.5))) * (lerp(global.world_grav_, 1, 0.3))

      self.__gimmick_cd = 0
      self.__gimmick_jumps -= 1
    }
  }
}
```

## step_begin

```sp

with oplayer {
  let alt_col = !script_execute(self.gen_col_sort, self.x, self.y, self.layer_col, 2)
    and script_execute(self.gen_col_sort, self.x, self.y + 2, self.layer_col, 2)

  let gr = self.vsp >= 0 and (
    script_execute(self.gen_col, self.x, self.y + 1) or alt_col)

  draw_text(0,0, string(self.__gimmick))
  let input = instance_find(oinput)
  if input != undefined {
    draw_text(0, 10, string(input.button_3))
  }

  let vv = 0
  let jump_press = 0
  if self.can_input and global.input_skip_ <= 8 {
    vv = input.down[0] - input.up[0] 
    jump_press = input.button_3[1] or (global.tap_jump_active and input.up[1])
  }


  draw_text(0, 20, string([gr, self.jump_delay, self.jump_buffer, vv]))

  let jumping =
      (gr and vv != 1 and (jump_press or global.jump_buffer_))
      or (!gr and self.jump_delay and jump_press)

  -- old
  --       (gr and vv != 1 and global.jump_buffer_)
  -- or (!gr and self.jump_delay and global.jump_buffer_)

  self.__data = [gr, vv, global.jump_buffer_, self.jump_delay, jump_press]
  if jumping {
    global.rmml.log("jump!")
    global.rmml.log(self.__data)
  }

  -- if jump_press and  !jumping {
  --   global.rmml.log("press")
  --   global.rmml.log(self.__data)
  -- }





  -- draw_text(0,0, string([self.state, global.jump_buffer_, alt_col, gr]))
  -- draw_text(0,10, string([global.jump_buffer_, global.jump_charge__, global.jump_charge_buffer__, self.jump_delay]))
}
```

## draw_gui_end

```sp
with oplayer {
  draw_text(0, 0, string(self.__data))
}
```