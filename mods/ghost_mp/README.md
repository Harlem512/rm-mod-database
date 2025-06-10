# Ghost Multiplayer

Technical details of how ghost multiplayer works.

# Operation Order

The following steps occur every frame, in order.

1. STEP_END Sync peers
   - For each player in lobby, create an instance to track that player
   - Delete any instances for players not in the lobby
1. STEP_END Receive packets
   - This needs to run after `step` so `osteam_handler` can run the steam sync
1. DRAW_BEGIN Simulate player movement
   - Runs after receiving packets, so the draw doesn't crash
1. DRAW Render ghost players
   - Render the ghost
   - Runs in draw so it renders before tiles
1. DRAW_GUI Broadcast the player's position
   - (also broadcasts other info)
   - runs late so player updates are sent immediately
1. DRAW_GUI_END UI rendering
   - emotes, map icons, debug info, etc

# Packets

## 0x01 player update

<!-- MARK: 0x01 plr pos-->

| Byte  | Data       | Desc             |
| ----- | ---------- | ---------------- |
| 0     | buffer_u8  | 0x01: plr update |
| 1,2   | buffer_u16 | room             |
| 3,4   | buffer_s16 | x-position       |
| 5,6   | buffer_s16 | y-position       |
| 7,8   | buffer_f16 | look angle       |
| 9,10  | buffer_s16 | grapple x        |
| 11,12 | buffer_s16 | grapple y        |
| 13    | buffer_u8  | data 1           |
| 14    | buffer_u8  | data 2           |

data 1

| Bit   | Desc         |
| ----- | ------------ |
| 0,1,2 | Emote, 0,1,2 |
| 3-7   | ...          |

data 2

| Bit | Desc                                            |
| --- | ----------------------------------------------- |
| 0,1 | 1: wall hug left 2: crouching 3: wall hug right |
| 2   | Player fell                                     |
| 3   | Is flying                                       |
| 4   | ...                                             |
| 5-7 | Weapon select                                   |

## 0x02 Palette

<!-- MARK: 0x02 palette -->

| Byte  | Data      | Desc                 |
| ----- | --------- | -------------------- |
| 0     | buffer_u8 | 0x02: palette update |
| 1-448 | ???       | palette color data   |
| 449   | buffer_u8 | data 1               |

data 1

| Bit | Desc                                         |
| --- | -------------------------------------------- |
| 0,1 | Character index (1: Fern, 2: Maya, 3: Ameli) |
| ... | ...                                          |
| 7   | 0 if palette is disabled/missing             |
