```sp
-- [ [ face (id), expression (frame), text ], [ ... ], ... ]
global.__gimmick_dialogue = fun (ar_) {
  let t = instance_create_depth(0, 0, 0, odialogue_box)
  t.dialouge_data = []
  let len = array_length(ar_)
  let i = 0
  while i < len {
    let sar_ = ar_[i]
    t.dialouge_data[i] = dialouge_create(sar_[0], sar_[1], sar_[2])
    i += 1
  }
  return t
}

-- checks for player collision with an active hook refresher
global.__gimmick_check_refresh = fun () {
  with ohook_refresh {
    -- check if the hook refresher was just activated
    if self.state == 1 and self.cooldown == 120 and place_meeting(self.x, self.y, oplayer) {
      return true
    }
  }
}
```

# controller

## room_start

```sp
match room_get() {
  -- intro room
  case rm_start_0 {
    -- checks if intro dialogue should be played
    if instance_exists(ospawn_point) and global.gamestate != 29 and !global.spayer_spawned {
      -- intro dialogue manager
      alarm_set(0, 1)
    }
  }
  -- bonnie fight
  case rm_boss_test {
    -- dialogue manager
    instance_create_depth(0,0, 0, omod_instance)
    -- block entrance into tutorial area (it's unbeatable)
    let foreground_tiles = layer_tilemap_get_id("Tiles_1")
    tilemap_set(foreground_tiles, 8, 0, 9)
    tilemap_set(foreground_tiles, 8, 0, 10)
    tilemap_set(foreground_tiles, 8, 0, 11)
    tilemap_set(foreground_tiles, 8, 0, 12)
  }
  -- elfhame bell room
  case rm_underhang_tunnel_start {
    -- dialogue manager
    instance_create_depth(0,0, 0, omod_instance)
  }
  -- hard switch room
  case rext_f33 {
    with otarget_wall {
      -- make the switch possible
      self.duration *= 1.5
    }
  }
  -- hardmode climb room
  case rext_j03 {
    -- dialogue manager
    instance_create_depth(0,0, 0, omod_instance)
  }
}
```

## alarm_0

```sp
-- destroy original dialogue
with odialogue_box {
  instance_destroy(self)
}
-- custom intro dialogue
global.__gimmick_dialogue([
  [sface_orb, 0, "Hey, wake up!"],
  [sface_player, 0, "Ugh.. my.. wait a minute.."],
  [sface_climb, 7, "[wave]Hey guys :3[/wave]"],
  [sface_player, 4, ".[delay].[delay].[delay]"],
  [sface_player, 13, "Who are you? And why are you in my head?"],
  [sface_climb, 5, "I thought you might want a [wave]challenge![/wave]"],
  [sface_climb, 6, "Most of your weapons are lame, so I replaced them with something more [wave]fun![/wave]"],
  [sface_player, 4, ".[delay].[delay].[delay]"],
  [sface_player, 29, "Why?"],
  [sface_climb, 8, "[shake]Because I can.[/shake]"],
  [sface_climb, 3, "I also told Bonnie to give you something more [wave]fun![/wave] It'll get more [shake]powerful[/shake] as you collect upgrades, too!"],
  [sface_player, 4, ".[delay].[delay].[delay]"],
  [sface_player, 26, "If you're trying to stop me, it won't work."],
  [sface_climb, 7, "Good luck with your plans! [wave]Everything is possible![/wave]"],
  [sface_orb, 0, ".[delay].[delay].[delay]"],
  [sface_orb, 1, "Are you even [shake]LISTENING[/shake] to me? And [shake]who[/shake] were you talking to?"],
  [sface_player, 12, "Shut up. I know where I'm going."],
]).back_dark = 1
```

## draw_begin

```sp
if global.clip_ != undefined {
  -- reset clips to prevent hot swapping
  global.clip_[4] = 0
  global.clip_[1] = 0
  -- forces you to use the best gun :3
  global.current_weapon_ = 2

  -- reduce the max reload timer because 1200 is a bit excessive
  -- run in draw_begin because otherwise the charge bar jumps
  -- (gun code runs in step_end)
  if global.reload_[2] > 800 {
    global.reload_[2] = 800
  }
}
```

## step

```sp
-- turn the invulnerable grapple enemies into cool puppets
with oenemy_swamp_wall {
  let puppet = instance_create_depth(
    self.x, self.y, self.depth,
    oenemy_puppet_small
  )
  -- keeps the arenas working properly
  puppet.arena_spawn = self.arena_spawn
  -- reduces their hp, because otherwise it's a little too hard
  puppet.hp /= 2.5
  instance_destroy(self)
}

-- replace the verse 2 box with fun :)
with oenemy_box_boss {
  if self.ani_timer > 330 {
    let inst = instance_create_depth(
      self.x, self.y, self.depth,
      oenemy_puppet_big
    )
    -- keeps the arena working properly
    inst.arena_spawn = true
    -- boss-level hp
    inst.hp *= 3
    -- remove the hyper shield
    inst.hyper_shield = false
    instance_destroy(self)
    -- fix the camera
    with ocamera {
      self.camera_state = 1
    }
  }
}

-- make shielded enemies vulnerable
with par_enemy {
  if self.hyper_shield and self.arena_spawn {
    -- remove hyper shield
    self.hyper_shield = false
    -- boost hp
    self.hp = 800
  }
}

-- apply jumps
with oplayer {
  let x = self.x
  let y = self.y

  -- disable the grapple
  self.can_hook_delay = 1000

  -- use script_execute because otherwise the pointers are used as numbers
  -- platform detection
  let on_plat = script_execute(self.gen_col_sort, x, y + 2, self.layer_col, 2)
  -- checks for platforms intersecting with the player hitbox
  -- lets you jump even when "inside" a platform
  let alt_col = !script_execute(self.gen_col_sort, x, y, self.layer_col, 2) and on_plat
  -- true if the player is "grounded"
  let gr = self.vsp >= 0 and (
    script_execute(self.gen_col, x, y + 1) or alt_col)

  -- reset jump counter on the ground
  -- OR if not initialized
  -- OR if ledge grabbing (5)
  -- OR colliding with an active (0) hook refresher
  if gr or self.__gimmick_cd == undefined or self.state == 5 or global.__gimmick_check_refresh() {
    self.__gimmick_jumps =
      -- ... if the hook is unlocked
      global.HOOK_UNLOCKED_
      -- ... if retraction grapple is unlocked
      + global.HOOK_UPGRADE_0_
      -- ... if shotgun is unlocked
      + global.weapon_data[1].found
      -- ... if rocket launcher is unlocked
      + global.weapon_data[4].found
    -- infinite jumps if infinite upgrade
    if self.endless_hook { self.__gimmick_jumps = infinity }
    -- reset cooldown
    self.__gimmick_cd = 0
    return
  }
  -- decrement jump cooldown
  self.__gimmick_cd += 1

  -- check if jumps are available and not on cooldown
  if self.__gimmick_cd < 10 or !self.__gimmick_jumps {
    return
  }

  -- check if we can input
  if !self.can_input or global.input_skip_ > 8 {
    return
  }

  -- check if the jump button is pressed
  let input = instance_find(oinput)
  if !(input.button_3[1] or (global.tap_jump_active and input.up[1])) {
    return
  }

  -- prevent double jumping when trying to fall through a platform
  if on_plat and input.down[0] {
    return
  }

  -- normal gravity, use standard double jump
  if global.world_grav_ >= 0.8 {
    -- normal jump uses +0, which "feels" too weak
    let power = 1
    -- heavy ammo = heavy jumps
    if global.trinket_active_[24] {
      power = 1.5
    }

    -- apply the jump velocity
    self.vsp = -(self.jump_pwr + power) * lerp(global.world_grav_, 1, 0.3)
  } else {
    let wind = instance_place(x, y, owind_spawner)
    if wind == noone {
      -- if no wind, do nothing
      return
    }
    -- fight the wind
    self.hsp -= lengthdir_x(self.jump_pwr, wind.image_angle)
    self.vsp -= lengthdir_y(self.jump_pwr, wind.image_angle)
  }

  -- jump colors
  let col = match self.__gimmick_jumps {
    case 4 { merge_color(c_dkgray, #F00, 0.2) }
    case 3 { merge_color(c_dkgray, #8F0, 0.1) }
    case 2 { merge_color(c_dkgray, #0FF, 0.1) }
    case 1 { merge_color(c_dkgray, #80F, 0.1) }
    else { merge_color(c_dkgray, #FFF, 0.5) }
  }

  -- sound and vfx !!!
  play_walk_sound(1.2, 0.9)
  let i = 14
  while i > 0 {
    let inst = instance_create_depth(x, y, -1, osmoke_fx)
    inst.image_blend = col
    i -= 1
  }
  i = 4
  while i > 0 {
    instance_create_depth(x, y, -1, ospark_alt)
    i -= 1
  }
  i = 2
  while i > 0 {
    instance_create_depth(x, y, -1, osmoke)
    i -= 1
  }
  global.shake++
  audio_play_sound_pitch(66, 0.75, random_range(0.9, 1.1), 0)

  -- reset cooldown, subtract jump counter
  self.__gimmick_cd = 0
  self.__gimmick_jumps -= 1
}
```

# instance

## draw

```sp
with oboss_mech {
  if self.state == 11 and self.dead_state == 2 {
    -- replace dialogue
    with odialogue_box {
      instance_destroy(self)
    }
    global.__gimmick_dialogue([
      [sface_tutor, 1, "Hiya guys! You freed me, so how about a blessing?"],
      [sface_orb, 0, "Woah! That's a.[delay].[delay].[delay]"],
      [sface_orb, 1, "[shake]What is this.[/shake]"],
      [sface_tutor, 0, "Normally, I'd give you my grappling power, but a really nice fae wanted me to give you something [wave]fun[/wave] instead!"],
      [sface_climb, 7, ";3"],
      [sface_player, 13, ".[delay].[delay].[delay]"],
      [sface_player, 17, "I think we're gonna have to kill that fae, Puck."],
      [sface_orb, 14, "Damn."],
      [sface_tutor, 1, "Just press the JUMP key in the air to double jump!"],
      [sface_player, 1, "I'd prefer to grapple. But let's try this out."],
    ])
  }
}

with obell_handler {
  if self.state == 1 and self.timer == 20 {
    global.__gimmick_dialogue([
      [sface_climb, 7, "Hey again :3"],
      [sface_player, 4, ".[delay].[delay].[delay]"],
      [sface_player, 3, "What now?"],
      [sface_climb, 5, "I thought you might want a hint for this next part!"],
      [sface_climb, 6, "Your DOUBLE JUMP doesn't work the same in Elfhame, but it's still useful!"],
      [sface_player, 26, "Just as I was getting [shake]used[/shake] to it."],
      [sface_climb, 7, "Try JUMPING when you get blown away by an [wave]owind_spawner![/wave]"],
      [sface_orb, 0, ".[delay].[delay].[delay]"],
      [sface_orb, 3, "Fern, why are you talking to yourself [shake]again.[/shake]"],
      [sface_player, 6, "Stupid fae changed the rules on us."],
    ])
  }
}

with onpc_climb {
  -- track talking from last frame
  let last = self.__last
  self.__last = self.talking_done
  -- we're on the second dialogue
  if last { return }
  let dialogue = instance_find(odialogue_box)
  -- speedrun mode check
  if dialogue == noone and self.speedrun_delay != 30 { return }
  if dialogue != noone {
    -- we've already replaced dialogue, exit
    if dialogue.__gimmick { return }
    -- delete old dialogue
    instance_destroy(dialogue)
  }

  -- victory dialogue
  global.__gimmick_dialogue([
    [sface_climb, 0, "Hello, took you a while, didn't it?"],
    [sface_climb, 7, "Hope you had some [wave]fun![/wave]"],
    [sface_climb, 0, "Rusted Moss is a flawed game, but its flaws are perfection, to a certain type of person."],
    [sface_climb, 1, "I'm one of those people."],
    [sface_climb, 2, "This is my favorite game, a perfect blend of glitch-like sequence breaking and tricky platforming."],
    [sface_climb, 3, "There are so many little stories in every detail, from the characters and graphics to the rooms and abilities."],
    [sface_climb, 4, "I'm just glad I got to play it."],
    [sface_player, 0, ".[delay].[delay].[delay]"],
    [sface_orb, 0, ".[delay].[delay].[delay]"],
    [sface_player, 4, "Who are you talking to?"],
    [sface_climb, 9, if true { "No one important." } else { "The pesky cheaters reading the source code ;)" }],
  ]).__gimmick = true
}
```
