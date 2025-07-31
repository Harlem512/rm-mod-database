# controller

## create

```sp
if !global.rmml.__mod_controllers.archipelago or !global.rmml.__mod_controllers.more_saves {
  global.rmml.warn("MS Archipelago requires Archipelago and More Saves enabled")
  global.rmml.unload("ms_archipelago")
  return
}

global.more_saves.hook_save_select_sensitive_buttons = true
self.depth = -1001
self.last_arch = -1
self.last_arch_json = -1
```

## draw

```sp
let menu = instance_find(omenu_new)
if !instance_exists(menu) {
  global.rmml.unload()
  return
}

if menu.state != -516 or menu.substate != 1 { return }

let save_index = menu.menu_select

if save_index != self.last_arch {
  self.last_arch = save_index
  let path = "f_save_" + string(self.last_arch) + ".archipelago.save"
  if file_exists(path) {
    let save_file = file_text_open_read(path)
    self.last_arch_json = json_parse(file_text_readln(save_file))
    file_text_close(save_file)
  } else {
    self.last_arch_json = -1
  }
}

if self.last_arch_json == -1 { return }

let col = draw_get_color()
draw_set_color(c_black)

draw_text(0,0, self.last_arch_json.slotName)
draw_text(0,12, self.last_arch_json.port)

draw_set_color(col)
```

