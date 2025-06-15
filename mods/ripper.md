# controller

## create

```sp
global.ripper = {}
global.ripper.type = 0
global.ripper.saved_index = 0
global.ripper.max = 100

-- find parents
global.ripper.parent = {}
let i = 0
while i <= 752 {
  global.ripper.parent[i] = object_get_parent(i)
  i += 1
}
global.rmml.log(global.ripper.parent)
```

## step

```sp
let log = file_text_open_append(global.rmml.log_name)

let i = 0
while i < global.ripper.max {
  let name
  let next
  let exists = false
  match global.ripper.type {
    case 0 {
      name = sprite_get_name(global.ripper.saved_index)
      exists = sprite_exists(global.ripper.saved_index)
      next = "room"
    }
    case 1 {
      name = room_get_name(global.ripper.saved_index)
      exists = room_exists(global.ripper.saved_index)
      next = "object"
    }
    case 2 {
      name = object_get_name(global.ripper.saved_index)
      exists = object_exists(global.ripper.saved_index)
      next = "audio"
    }
    case 4 {
      name = audio_get_name(global.ripper.saved_index)
      exists = audio_exists(global.ripper.saved_index)
      next = "script"
    }
    case 5 {
      name = script_get_name(global.ripper.saved_index)
      exists = is_string(name) and name != "<unknown>"
      next = "END"
    }
    case 6 {
      file_text_close(log)
      global.rmml.throw("done")
    }
  }

  if !exists {
    file_text_write_string(log, next + "\n")
    global.ripper.saved_index = -1
    global.ripper.type += 1
  } else {
    file_text_write_string(log, string(global.ripper.saved_index) + "\t:" + name + "\n")
  }
  i += 1
  global.ripper.saved_index += 1
}

file_text_close(log)
```