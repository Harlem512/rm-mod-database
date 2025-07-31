# controller

## step_begin

```sp
let has_elicia = instance_number(oboss_sword)
with oboss_sword_sword {
  if self.active and self.index == 1 and !has_elicia and self.timer < 40 {
    instance_destroy(self)
  }
}
```
