import pytest
from engine.weight_solver import WeightSolver

def test_breguet_range_fraction():
    """
    Verification against standard Breguet Range equation behavior.
    """
    solver = WeightSolver(
        category="Jet Transport",
        payload_lbs=5000,
        crew_weight_lbs=400,
        range_nm=2000,
        cruise_mach=0.8,
        sfc=0.5,
        ld_ratio=14.0
    )
    
    ff = solver.calculate_cruise_fuel_fraction()
    # Ensure it returns a fraction between 0 and 1
    assert 0.0 < ff < 1.0
    # A standard jet over 2000nm should burn roughly 10-20% of its weight
    assert 0.80 < ff < 0.95

def test_iterative_convergence():
    """
    Validation of the iterative solver convergence logic.
    """
    solver = WeightSolver(
        category="Fighter",
        payload_lbs=2000,
        crew_weight_lbs=200,
        range_nm=1000,
        cruise_mach=0.9,
        sfc=0.8,
        ld_ratio=10.0
    )
    
    results = solver.solve()
    assert results["converged"] == True
    assert results["W0"] > 0
    assert results["We"] > 0
    assert results["Wf"] > 0
    
    # Check physical mass balance: W0 = We + Wf + W_payload + W_crew
    # Account for 6% trapped fuel margin built into the solver
    W_fixed = solver.W_payload + solver.W_crew
    assert abs(results["W0"] - (results["We"] + results["Wf"] + W_fixed)) < 5.0

def test_impossible_design():
    """
    Test that the solver catches physically impossible designs 
    (e.g., L/D too low, causing fuel fraction to exceed 1.0)
    """
    solver = WeightSolver(
        category="Jet Transport",
        payload_lbs=50000,
        crew_weight_lbs=400,
        range_nm=10000, # Massive range
        cruise_mach=0.8,
        sfc=1.0,        # Terrible efficiency
        ld_ratio=5.0    # Terrible aero
    )
    
    with pytest.raises(ValueError):
        solver.solve()
