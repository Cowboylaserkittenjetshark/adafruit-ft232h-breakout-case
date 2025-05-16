from openscad import *
from dataclasses import dataclass

@dataclass
class Rect:
    x: float
    y: float
    
@dataclass
class Standoffs:
    minRadius: float
    majRadius: float
    height: float

def millimeters(inches):
    return inches * 25.4

board = Rect(
    millimeters(1.5),
    millimeters(0.9),
)

holeSpacing = Rect(
    millimeters(1.3),
    millimeters(0.7),
)

switch = Rect(5, 8)

# Project name preprended to exported files
pname = "adafruit-ft232h-breakout-case"

# Plate thickness
thickness = 2

# Standoff parameters
minRadius = 1.3 # Screw hole radius
majRadius = 2   # Outer diameter
topStandoffs = Standoffs(minRadius, majRadius, 3) # The top plate needs extra clearance for the USB port
bottomStandoffs = Standoffs(minRadius, majRadius, 2)

fn = 60

def plate(standoffs):
    sr = standoffs.majRadius
    sh = standoffs.height + thickness

    p = square([board.x - sr * 2, board.y - sr * 2]) \
    .offset(sr) \
    .translate([sr, sr]) \
    .linear_extrude(thickness)
    
    s = []
    h = []
    for x in range(0, 2):
        for y in range(0, 2):
            holeVec = [
                ((board.x - holeSpacing.x) / 2) + holeSpacing.x * x,
                ((board.y - holeSpacing.y) / 2) + holeSpacing.y * y,
                0
            ]

            s.append(
                cylinder(r = sr, h = sh)
                .translate(holeVec)
            )

            h.append(
                cylinder(r = standoffs.minRadius, h = sh)
                .translate(holeVec)
            )
    
    return p.union(s).difference(h)

switchCutout = cube([switch.x, switch.y, thickness]).translate(
    [
        (board.x - holeSpacing.x) * 3 / 2,
        (board.y - switch.y) / 2,
        0
    ]
)

headerCutouts = [
    polygon([[-14,0],[14,0],[13,5],[-13,5]], paths=[[0,1,2,3]]) \
    .linear_extrude([0,0,thickness]) \
    .translate([board.x/2,0,0]),

    polygon([[-13,0],[13,0],[14,5],[-14,5]], paths=[[0,1,2,3]]) \
    .linear_extrude([0,0,thickness]) \
    .translate([board.x/2,board.y - 5,0])
]

topPlate = plate(topStandoffs).difference(switchCutout).difference(headerCutouts)
bottomPlate = plate(bottomStandoffs).difference(headerCutouts)

show([
    topPlate.back(30),
    bottomPlate
])

export(
    {
        "top-plate" : topPlate,
        "bottom-plate" : bottomPlate
    },
    pname + ".3mf"
)
