# controller

## room_start

```sp
while i >= 0 {
  let npc = instance_find(par_npc, i)
  if !npc.__punt {
    npc.__punt = true
    let punt = instance_create_depth(npc.x, npc.y, npc.depth, omod_enemy)
    punt.sprite_index = npc.sprite_index
    punt._parent = npc
    punt.hp = 100000
    punt.can_be_killed_by_hazard = false
    punt.fall_death = false
  }
  i -= 1
}
```

# enemy

## create

```sp
event_inherited()
```

## step

```sp
event_inherited()
if instance_exists(self) {
  self._parent.x = self.x
  self._parent.y = self.y
}
```
