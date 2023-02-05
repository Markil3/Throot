from collections import namedtuple

SpriteImage = namedtuple("SpriteImage", ["image", "collision", "width", "height"])

# BITMAP: width: 8, height: 8
skull = SpriteImage(
    bytearray([0,28,102,126,38,30,28,0]),
    None,
    8,
    8
)
# BITMAP: width: 8, height: 8
pizza = SpriteImage(
    bytearray([0,0,64,96,80,104,124,0]),
    None,
    8,
    8
)
# BITMAP: width: 10, height: 10
boulder = SpriteImage(
    bytearray([224,80,136,72,148,4,140,248,240,224,0,1,2,3,2,3,3,3,3,1]),
    None,
    10,
    10
)
# BITMAP: width: 10, height: 10
ball = SpriteImage(
    bytearray([120,212,170,85,131,1,133,26,132,120,0,0,1,3,2,3,2,1,0,0]),
    None,
    10,
    10
)
# BITMAP: width: 10, height: 10
steve = SpriteImage(
    bytearray([255,1,225,249,185,121,121,185,249,225,1,255,15,8,11,11,8,9,9,8,11,11,8,15]),
    None,
    12,
    12
)
# BITMAP: width: 11, height: 8
spaceinv = SpriteImage(
    bytearray([112,24,125,182,188,60,188,182,125,24,112,7,152,125,54,60,60,60,54,125,152,7]),
    None,
    11,
    8
)
# BITMAP: width: 11, height: 8
mathroot = SpriteImage(
    bytearray([0,0,16,48,96,192,254,62,6,6,0]),
    None,
    11,
    8
)
#/ = bytearray([255,255,239,239,72,10,192,10,72,239,239])
# BITMAP: width: 11, height: 8
robot = SpriteImage(
    bytearray([0,16,16,183,245,63,245,183,16,16,0]),
    None,
    11,
    8
)
# BITMAP: width: 11, height: 8
dinoskull = SpriteImage(
    bytearray([15,9,9,10,17,18,36,34,20,8,0]),
    None,
    11,
    8
)
# BITMAP: width: 11, height: 8
dinojaw = SpriteImage(
    bytearray([62,65,65,193,137,13,129,6,168,16,224]),
    None,
    11,
    8
)
# BITMAP: width: 11, height: 8
dinospine = SpriteImage(
    bytearray([56,68,40,68,56,56,68,40,68,56,0]),
    None,
    11,
    8
)
# BITMAP: width: 11, height: 8
bone = SpriteImage(
    bytearray([40,84,68,40,40,40,40,40,68,84,40]),
    None,
    11,
    8
)
# BITMAP: width: 70, height: 40
bigdinohead = SpriteImage(
    bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,128,128,128,128,128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,24,62,98,131,1,137,12,12,30,30,12,96,97,115,2,102,12,8,48,96,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,6,5,8,9,11,10,12,10,12,10,12,10,12,10,4,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
    None,
    70,
    40
)
# BITMAP: width: 70, height: 40
bigboneddiag = SpriteImage(
    bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,128,128,192,32,32,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            3,4,4,4,8,16,33,66,132,8,16,32,64,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,1,14,16,16,12,4,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
    None,
    70,
    40
)
# BITMAP: width: 70, height: 40
bigdoritoobstacle = SpriteImage(
    bytearray([1,11,2,36,4,8,80,48,32,32,32,64,192,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,32,0,8,0,0,0,6,0,16,1,1,3,3,6,36,12,72,88,16,48,32,64,192,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,128,0,128,64,160,64,160,64,168,208,168,208,104,80,100,104,52,40,20,24,20,24,20,24,20,24,20,24,21,9,10,14,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,128,128,128,128,192,64,64,64,
            5,6,7,2,3,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,128,128,128,128,128,128,128,64,64,96,32,32,32,32,32,16,16,16,16,16,16,24,24,12,132,4,2,1,1,1,1,0,16,4,0,0,0,0,4,0,2,4,1,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,6,4,4,4,10,12,18,20,26,20,40,52,32,40,52,40,33,36,52,42,52,40,48,40,48,40,32,48,40,48,40,96,104,80,72,84,72,80,72,64,96,200,128]),
    None,
    70,
    40
)
# BITMAP: width: 16, height: 16
leaf = SpriteImage(
    bytearray([127,254,254,254,252,252,252,184,120,240,240,224,192,0,0,0,
            0,1,3,7,15,15,31,31,63,62,61,59,55,111,254,192]),
    None,
    16,
    16
)

annoydead = SpriteImage(
    bytearray([0,240,214,236,54,190,214,238,212,254,248,240,224,192,192,128,128,128,128,240,0,
            0,63,255,254,126,126,254,255,127,127,127,127,127,255,255,127,127,255,255,31,0,
            0,0,1,0,0,0,3,1,0,0,0,0,0,3,1,0,0,1,0,0,0]),
    None,
    21,
    19
)

flowerpetals = SpriteImage(
    bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,240,252,254,254,254,254,252,248,
            0,0,0,0,0,252,254,255,255,255,255,255,254,254,223,63,255,255,255,255,255,255,
            0,224,248,252,252,252,255,255,255,247,239,239,223,255,255,255,255,255,251,255,255,255]),
    None,
    22,
    24
)

flowerpetalanim = SpriteImage(
    bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,63,191,191,7,55,231,227,251,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,191,191,191,7,115,249,253,252,254,252,255,255,255,255,255,31,79,239,231,224,238,223,223,223,191,255,254,248,243,255,255,255,255,255,255,255,255,255,127,127,127,127,127,127,127,7,241,252,254,254,254,254,253,249,255,255,255,255,1,252,254,255,255,255,255,255,254,254,223,63,255,255,255,255,255,255,15,227,249,253,253,252,255,255,255,247,239,239,223,255,255,255,255,255,251,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,31,207,247,243,251,243,247,199,255,255,255,255,255,15,231,243,249,253,253,253,253,252,254,247,231,207,255,255,255,255,255,31,199,243,251,250,248,255,255,239,223,191,255,255,255,255,255,255,255,255,255,255]),
    None,
    22,
    24
)

lvl4wall = SpriteImage(
    bytearray([255,255,254,254,252,252,248,248,240,240,224,224,192,192,192,128,128,0,0,0,0,224,240,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,240,224,0,0,0,224,240,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,248,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,0,0,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,0,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,63,0,0,0,0,63,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,31,0,0,0,63,127,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,63,63,31,31,15,15,7,7,3,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
    None,
    72,
    30
)

ballobstaclelvl3 = SpriteImage(
    bytearray([0,0,0,0,0,0,0,0,192,224,240,240,248,252,252,252,254,254,254,254,254,254,252,252,252,248,240,240,224,192,0,0,0,0,0,0,0,0,0,0,192,224,240,240,248,252,252,252,254,254,254,254,254,254,252,252,252,248,240,240,224,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,240,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,240,0,0,0,0,240,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,240,0,0,0,0,0,0,0,0,0,0,0,0,3,31,63,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,63,31,3,0,0,0,0,3,31,63,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,63,31,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3,3,7,15,15,15,31,31,31,31,31,31,15,15,15,7,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,1,3,3,7,15,15,15,31,31,31,31,31,31,15,15,15,7,3,3,1,0,0,0,0,0,0,0,0,0,0,0]),
    None,
    72,
    30
)

Doritoobstaclelvl5 = SpriteImage(
    bytearray([254,254,254,254,254,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,248,248,248,248,248,248,248,248,248,248,248,248,248,240,224,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,192,224,224,240,248,248,252,252,254,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,63,31,31,15,7,3,3,3,3,1,0,0,0,0,0,0,128,128,192,224,224,240,240,248,252,252,254,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,63,63,31,31,31,15,15,7,7,7,3,3,1,1,1,0,0,0,0,0,0,0,0,128,128,192,224,240,248,248,252,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,7,3,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15]),
    None,
    72,
    30
)

sprite_water =  SpriteImage(
    bytearray([224,240,240,248,252,248,240,240]),
    None,
    8,
    8
)

OBSTACLES = [skull, pizza, boulder, ball, steve, mathroot, leaf, robot, dinoskull, dinojaw, dinospine, bone, bigdinohead, bigboneddiag, bigdoritoobstacle, spaceinv,annoydead,lvl4wall,ballobstaclelvl3,Doritoobstaclelvl5]