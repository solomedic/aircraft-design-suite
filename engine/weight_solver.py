import math
from .aircraft_constants import AIRCRAFT_CONSTANTS, MISSION_SEGMENTS

class WeightSolver:
    def __init__(self, category: str, payload_lbs: float, crew_weight_lbs: float, 
                 range_nm: float, cruise_mach: float, sfc: float, ld_ratio: float):
        self.category = category
        self.W_payload = payload_lbs
        self.W_crew = crew_weight_lbs
        self.R = range_nm
        self.M = cruise_mach
        self.SFC = sfc
        self.LD = ld_ratio
        
        # Get historical constants
        if category not in AIRCRAFT_CONSTANTS:
            raise ValueError(f"Unknown category: {category}")
        self.A = AIRCRAFT_CONSTANTS[category]["A"]
        self.C = AIRCRAFT_CONSTANTS[category]["C"]
        
    def calculate_cruise_fuel_fraction(self) -> float:
        """
        Breguet Range Equation for Jets.
        W_final / W_initial = e^(-(R * SFC) / (V * L/D))
        Note: V is roughly 573.6 knots at Mach 1 (Standard Atmosphere at 36k ft).
        """
        V_knots = self.M * 573.6
        exponent = (self.R * self.SFC) / (V_knots * self.LD)
        return math.exp(-exponent)
        
    def get_total_mission_fraction(self) -> float:
        """Multiplies all mission segment fuel fractions."""
        ff = 1.0
        ff *= MISSION_SEGMENTS["warmup"]
        ff *= MISSION_SEGMENTS["taxi"]
        ff *= MISSION_SEGMENTS["takeoff"]
        ff *= MISSION_SEGMENTS["climb"]
        ff *= self.calculate_cruise_fuel_fraction()
        ff *= MISSION_SEGMENTS["descent"]
        ff *= MISSION_SEGMENTS["landing"]
        return ff

    def solve(self, initial_guess=10000.0, tolerance=0.5, max_iterations=100):
        """
        Iteratively solves for W0.
        W0 = W_crew + W_payload + W_fuel + W_empty
        W0 = W_fixed / (1 - Wf/W0 - We/W0)
        """
        W_fixed = self.W_payload + self.W_crew
        
        # Wf/W0 = 1.06 * (1 - total_mission_fraction)
        # The 1.06 factor accounts for 6% reserve/trapped fuel standard.
        mission_fraction = self.get_total_mission_fraction()
        Wf_W0 = 1.06 * (1 - mission_fraction)
        
        W0 = initial_guess
        iteration_log = []
        
        for i in range(max_iterations):
            # Calculate Empty Weight Fraction based on current W0
            We_W0 = self.A * (W0 ** self.C)
            
            # Calculate new W0
            denominator = 1.0 - Wf_W0 - We_W0
            
            if denominator <= 0:
                raise ValueError("Design impossible with given parameters (Denominator <= 0). Try increasing L/D or reducing Payload.")
                
            W0_new = W_fixed / denominator
            
            iteration_log.append({
                "iteration": i + 1,
                "W0_guess": round(W0, 1),
                "We_W0": round(We_W0, 4),
                "W0_new": round(W0_new, 1)
            })
            
            # Check convergence
            if abs(W0_new - W0) < tolerance:
                W0 = W0_new
                break
                
            W0 = W0_new
            
        We = W0 * (self.A * (W0 ** self.C))
        Wf = W0 * Wf_W0
        
        return {
            "converged": abs(W0_new - W0) < tolerance,
            "W0": round(W0, 1),
            "We": round(We, 1),
            "Wf": round(Wf, 1),
            "log": iteration_log
        }
