# Historical Data based on Nicolai / Raymer Textbooks
# Equation: W_e / W_0 = A * W_0^C

AIRCRAFT_CONSTANTS = {
    "Jet Transport": {
        "A": 1.02,
        "C": -0.06
    },
    "Fighter": {
        "A": 2.34,
        "C": -0.13
    },
    "General Aviation (Twin)": {
        "A": 0.86,
        "C": -0.05
    },
    "UAV": {
        # Using typical small twin-engine bounds as approximation
        "A": 0.90,
        "C": -0.05
    }
}

# Standard Mission Segment Fuel Fractions (W_i / W_i-1)
MISSION_SEGMENTS = {
    "warmup": 0.990,
    "taxi": 0.990,
    "takeoff": 0.995,
    "climb": 0.980,
    "descent": 0.990,
    "landing": 0.992
}
