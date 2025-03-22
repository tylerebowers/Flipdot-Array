numbers_5x3 = [
    [31,17,31], #0
    [18,31,16],
    [29,21,23],
    [21,21,31],
    [7,4,31],
    [23,21,29],
    [31,21,29],
    [1,29,3],
    [31,21,31],
    [23,21,31], #9
]

numbers_7x4 = [
    [62,65,65,62], #0
    [0,66,127,64],
    [98,81,73,70],
    [34,65,73,54],
    [7,8,8,127],
    [39,73,73,49],
    [54,73,73,48],
    [1,97,25,7],
    [54,73,73,54],
    [38,73,73,62], #9
]

numbers_7x3 = [
    [62,65,62], #0
    [66,127,64],
    [98,81,78],
    [34,73,54],
    [7,8,127],
    [79,73,49],
    [62,73,50],
    [97,25,7],
    [54,73,54],
    [6,9,126], #9
]

ascii_5 = {
    " ": [0],
    "!": [23],
    "\"": [3,0,3],
    "#": [10,4,10],
    "$": [10,31,10],
    "%": [25,4,19],
    "&": [25,4,19], 
    "\'": [1], 
    "(": [14,17],
    ")": [17,14],
    "*": [3,3],
    "+": [4,14,4],
    ",": [24],
    "-": [4,4],
    ".": [16],
    "/": [16,14,1],
    "0": [31,17,31],
    "1": [18,31,16],
    "2": [29,21,23],
    "3": [21,21,31],
    "4": [7,4,31],
    "5": [23,21,29],
    "6": [31,21,29],
    "7": [1,29,3],
    "8": [31,21,31],
    "9": [23,21,31],
    ":": [10],
    ";": [26],
    "<": [4,10],
    "=": [10,10],
    ">": [10,4],    
    "?": [2,25,6],
    "@": [4,10,14], 
    "A": [30,5,30],
    "B": [31,21,10],
    "C": [14,17,17],
    "D": [31,17,14],
    "E": [31,21,21],
    "F": [31,5,5],
    "G": [31,17,29],
    "H": [31,4,31],
    "I": [17,31,17],
    "J": [9,17,15],
    "K": [31,4,27],
    "L": [31,16],
    "M": [31,1,14,1,30],
    "N": [31,1,30],
    "O": [31,17,31],
    "P": [31,5,2],
    "Q": [31,17,15,16],
    "R": [31,5,26],
    "S": [23,21,29],
    "T": [1,31,1],
    "U": [31,16,31],
    "V": [15,16,15],
    "W": [15,16,14,16,15],
    "X": [27,4,27],
    "Y": [3,28,3],
    "Z": [25,21,19],       
    "[": [31,17],
    "\\": [1,14,16],
    "]": [17,31],
    "^": [2,1,2],
    "_": [16,16],
    "`": [1,2],
    "a": [13,21,30],
    "b": [31,20,8],
    "c": [8,20],
    "d": [8,20,31],
    "e": [12,22,20],
    "f": [30,5,1],
    "g": [18,21,15],
    "h": [31,4,24],
    "i": [26],
    "j": [16,13],
    "k": [31,8,20],
    "l": [31],
    "m": [30,2,28,2,28],
    "n": [30,2,28],
    "o": [12,18,12],
    "p": [28,10,4],
    "q": [4,10,28],
    "r": [28,4],
    "s": [18,21,9],
    "t": [2,15,18],
    "u": [12,16,28],
    "v": [12,16,12],
    "w": [12,16,12,16,12],
    "x": [20,8,20],
    "y": [22,20,30],
    "z": [26,22],
    "{": [14,17],
    "|": [31],
    "}": [17,14],
    "~": [4],
}

ascii_7 = {
    " ": [0],
    "!": [95],
    "\"": [3,0,3],
    "#": [20,62,20,62,20],
    "$": [46,127,58],
    "%": [18,8,36],
    "&": [94,33,82],
    "\'": [3],
    "(": [62,65],
    ")": [65,62],
    "*": [5,2,5],
    "+": [8,28,8],
    ",": [64,32],
    "-": [8,8],
    ".": [0,64],
    "/": [96,28,3],
    "0": [62,65,62],
    "1": [66,127,64],
    "2": [98,81,78],
    "3": [34,73,54],
    "4": [15,8,127],
    "5": [79,73,49],
    "6": [62,73,50],
    "7": [97,25,7],
    "8": [54,73,54],
    "9": [6,9,126],
    ":": [34],
    ";": [52],
    "<": [8,20],
    "=": [20,20],
    ">": [20,8],
    "?": [2,89,6],
    "@": [62,85,30],
    "A": [126,9,126],
    "B": [127,73,54],
    "C": [62,65,65],
    "D": [127,65,62],
    "E": [127,73,73],
    "F": [127,9,9],
    "G": [127,65,73,120],
    "H": [127,8,127],
    "I": [65,127,65],
    "J": [32,65,63],
    "K": [127,8,119],
    "L": [127,64,64],
    "M": [127,2,4,2,127],
    "N": [127,4,8,127],
    "O": [127,65,127],
    "P": [127,9,15],
    "Q": [127,81,127,32],
    "R": [127,25,111],
    "S": [79,73,121],
    "T": [1,127,1],
    "U": [127,64,127],
    "V": [63,64,63],
    "W": [63,64,56,64,63],
    "X": [119,8,119],
    "Y": [7,120,7],
    "Z": [113,73,71],
    "[": [127,65],
    "\\": [3,28,96],
    "]": [65,127],
    "^": [2,1,2],
    "_": [64,64],
    "`": [1,2],
    "a": [116,84,120],
    "b": [127,72,48],
    "c": [48,72,72],
    "d": [48,72,127],
    "e": [56,84,88],
    "f": [126,5],
    "g": [88,84,124],
    "h": [127,8,112],
    "i": [122],
    "j": [64,58],
    "k": [127,16,108],
    "l": [126],
    "m": [124,4,60,4,120],
    "n": [124,4,120],
    "o": [56,68,56],
    "p": [124,20,8],
    "q": [8,20,124],
    "r": [120,8],
    "s": [88,84,52],
    "t": [4,126,4],
    "u": [56,64,120],
    "v": [48,64,48],
    "w": [56,64,48,64,56],
    "x": [108,16,108],
    "y": [12,80,124],
    "z": [100,84,76],
    "{": [8,54,65],
    "|": [127],
    "}": [65,54,8],
    "~": [8,4,8,4],
} 

special = {
    "°": [2,5,2],
    "degrees_c": [2,5,2,120,72],
    "degrees_f": [2,5,2,124,20],
    "🙂": [62,81,101,97,101,81,62],
    "😐": [62,65,85,81,85,65,62],
    "🙁": [62,97,85,81,85,97,62],

}


"""
0	Clear sky
1, 2, 3	Mainly clear, partly cloudy, and overcast
45, 48	Fog and depositing rime fog
51, 53, 55	Drizzle: Light, moderate, and dense intensity
56, 57	Freezing Drizzle: Light and dense intensity
61, 63, 65	Rain: Slight, moderate and heavy intensity
66, 67	Freezing Rain: Light and heavy intensity
71, 73, 75	Snow fall: Slight, moderate, and heavy intensity
77	Snow grains
80, 81, 82	Rain showers: Slight, moderate, and violent
85, 86	Snow showers slight and heavy
95 *	Thunderstorm: Slight or moderate
96, 99 *	Thunderstorm with slight and heavy hail
"""
weather = {
    0: [0,42,28,62,28,42],
    1: [4,6,54,48,36,6,4],
    2: [4,6,54,48,36,6,4],
    3: [4,6,54,48,36,6,4],
    45: [0,42,0,42,0,42],
    48: [0,42,0,42,0,42],
    51: [0,20,6,38,6,20],
    53: [0,20,6,38,6,20],
    55: [0,20,6,38,6,20],
    56: [0,42,0,42,0,42],
    57: [0,42,0,42,0,42],
    61: [0,20,6,38,6,20],
    63: [0,20,6,38,6,20],
    65: [0,20,6,38,6,20],
    66: [0,20,6,38,6,20],
    67: [0,20,6,38,6,20],
    71: [80,36,86,6,86,36,80],
    73: [80,36,86,6,86,36,80],
    75: [80,36,86,6,86,36,80],
    77: [0,84,6,86,6,84],
    80: [0,4,118,6,118,4],
    81: [0,4,118,6,118,4],
    82: [0,4,118,6,118,4],
    85: [80,36,86,38,86,36,80],
    86: [80,36,86,38,86,36,80],
    95: [0,26,51,3,27,50],
    96: [0,52,54,6,54,52],
    99: [0,52,54,6,54,52]
}

screens = {
    "shutdown": [0,0,0,0,0,0,0,28,34,32,39,32,34,28,0,0,0,0,0,0,0],
    "sleep": [127,65,85,81,81,85,65,127,0,50,42,38,0,50,42,38,0,50,42,38,0],
    "reboot": [0,62,34,34,32,34,39,47,34,34,34,34,34,122,114,34,2,34,34,62,0],
}