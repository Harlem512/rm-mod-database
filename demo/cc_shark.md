<!-- single # are used for object types -->

# controller

<!-- double ## are for event names -->

## room_start

<!-- ``` denotes a code block, which will be interpreted as catspeak
(or javascript-flavored catspeak) -->

```
i = instance_create_depth(200, 10, -2000, omod_instance)
i.sprite_index = sboss_maya_fish
i.image_angle = 0
```

<!-- a second object type -->

# instance

<!-- non-controller, non-player events only run for objects that were
created with this mod -->

## step

```
-- catspeak blocks use catspeak comments
self.image_angle -= 1
```

## draw_gui_end

<!-- ```js does some postprocessing, so text editors can do syntax highlighting
Use the following instead of catspeak:
| "js"          | catspeak    | description       |
| ------------- | ----------- | ----------------- |
| function(...) | fun(...)    | function          |
| type(...)     | typeof(...) | get variable type |
| &&            | and         | logical and       |
| ||            | or          | logical or        |
| //            | --          | comments          |
HOWEVER: this is not real javascript. If it doesn't work in catspeak, it
wont work here. This includes quote behavior (in catspeak, ' and " are VERY different) -->

```js
// javascript code blocks use javascript comments
draw_sprite_ext(
  self.sprite_index,
  0,
  self.x,
  self.y + 20,
  1,
  1,
  self.image_angle,
  c_white,
  1
)
```
