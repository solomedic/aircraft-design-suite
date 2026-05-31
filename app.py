from pathlib import Path

import pandas as pd
import streamlit as st
from engine.weight_solver import WeightSolver

APP_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Aircraft Design Toolbox",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom minimal CSS for a "Dashboard" feel
st.markdown("""
    <style>
    .brand-shell {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 18px 20px;
        margin: 0 0 16px 0;
        border: 1px solid #D9E2EC;
        border-radius: 18px;
        background: linear-gradient(135deg, #F8FAFC 0%, #EEF4FF 100%);
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    }
    .brand-mark {
        width: 64px;
        height: 64px;
        flex: 0 0 64px;
        border-radius: 18px;
        background: linear-gradient(145deg, #0F172A 0%, #1E3A8A 100%);
        position: relative;
        overflow: hidden;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.12);
    }
    .brand-mark::before {
        content: "";
        position: absolute;
        inset: 13px 11px 17px 11px;
        background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(191,219,254,0.7));
        clip-path: polygon(0% 52%, 38% 48%, 56% 0%, 65% 14%, 83% 14%, 100% 30%, 67% 35%, 53% 54%, 100% 100%, 58% 74%, 45% 100%, 37% 61%, 0% 58%);
        transform: rotate(-8deg);
    }
    .brand-mark::after {
        content: "";
        position: absolute;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        right: 10px;
        top: 10px;
        background: rgba(255,255,255,0.9);
        box-shadow: 0 0 18px rgba(255,255,255,0.5);
    }
    .brand-copy h1 {
        margin: 0;
        font-size: 1.9rem;
        line-height: 1.1;
        color: #0F172A;
        letter-spacing: -0.02em;
    }
    .brand-copy p {
        margin: 4px 0 0 0;
        color: #475569;
        font-size: 0.98rem;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 600;
        color: #1E3A8A;
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        height: 100%;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #F1F5F9;
        border-radius: 5px 5px 0px 0px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown(
    """
    <div class="brand-shell">
        <div class="brand-mark" aria-hidden="true"></div>
        <div class="brand-copy">
            <h1>Aircraft Design Toolbox</h1>
            <p>Conceptual sizing, constraint analysis, and stability workflows for early-stage aerospace design.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="main-header">✈️ Automated Aircraft Conceptual Design Suite</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# LANDING DASHBOARD
# ---------------------------------------------------------
col1, col2 = st.columns([1.2, 1])

with col1:
    f16_image = APP_DIR / "f16.png"
    if f16_image.exists():
        st.image(str(f16_image), caption="System Ready | Unified Design Architecture", use_container_width=True)
    else:
        st.info("Aircraft reference image will appear here.")

with col2:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    bcol1, bcol2 = st.columns([1, 3])
    with bcol1:
        nicolai_book_image = APP_DIR / "nicolai_book.png"
        if nicolai_book_image.exists():
            st.image(str(nicolai_book_image), use_container_width=True)
    with bcol2:
        st.markdown("### 📘 Master Methodology")
        st.markdown("""
        This suite integrates the aerospace engineering standards of **Nicolai** (Systems & Weight), **Raymer** (Constraints & Layout), and **Sadraey** (Stability & Control) into a single automated pipeline.
        """)
    st.markdown("---")
    st.markdown("### 🚀 Master Engine Status")
    st.progress(0, text="Engine Idle. Awaiting Phase 1 Initialization...")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🛠️ Design Process Pipeline")

# ---------------------------------------------------------
# PIPELINE TABS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "1. Mission & Sizing (Nicolai)", 
    "2. Constraint Analysis (Raymer)", 
    "3. Wing Geometry (Sadraey)", 
    "4. Aerodynamics (Raymer)", 
    "5. Propulsion (Nicolai)", 
    "6. Tail & Stability (Sadraey)",
    "7. Global Optimization"
])

# --- TAB 1: Initial Sizing ---
with tab1:
    st.markdown("#### Phase 1: Initial Takeoff Weight ($W_0$) Sizing")
    st.caption("Reference: Nicolai, Fundamentals of Aircraft Design (Chapter 2 & 3)")
    
    col_input, col_output = st.columns([1, 1])
    with col_input:
        category = st.selectbox("Aircraft Category", ["Jet Transport", "Fighter", "UAV", "General Aviation (Twin)"])
        payload = st.number_input("Payload Weight (lbs)", value=5000, step=100)
        crew = st.number_input("Crew Weight (lbs)", value=400, step=50, help="E.g., 2 crew members at 200 lbs each")
        range_nm = st.number_input("Range (nm)", value=2000, step=100)
        mach = st.number_input("Cruise Speed (Mach)", value=0.8, step=0.01)
        sfc = st.number_input("Specific Fuel Consumption (1/hr)", value=0.5, step=0.05, help="Typical Turbofan: 0.4 - 0.6")
        ld = st.number_input("Estimate L/D Ratio", value=14.0, step=0.5, help="Typical Subsonic Jet: 12 - 18")
        
        run_solver = st.button("Calculate Initial W0", type="primary", use_container_width=True)
    
    with col_output:
        st.markdown("##### Iteration Results")
        if run_solver:
            solver = WeightSolver(category, payload, crew, range_nm, mach, sfc, ld)
            try:
                results = solver.solve()
                st.metric(label="Converged Takeoff Weight (W0)", value=f"{results['W0']:,.1f} lbs")
                st.metric(label="Empty Weight (We)", value=f"{results['We']:,.1f} lbs")
                st.metric(label="Fuel Weight (Wf)", value=f"{results['Wf']:,.1f} lbs")
                
                st.success("Solver converged successfully!")
                
                with st.expander("View Iteration Log"):
                    df = pd.DataFrame(results['log'])
                    st.dataframe(df, use_container_width=True)
            except ValueError as e:
                st.error(str(e))
        else:
            st.metric(label="Converged Takeoff Weight (W0)", value="--- lbs")
            st.metric(label="Empty Weight (We)", value="--- lbs")
            st.metric(label="Fuel Weight (Wf)", value="--- lbs")

# --- TAB 2: Constraint Analysis ---
with tab2:
    st.markdown("#### Phase 2: Constraint Diagram ($T/W$ vs $W/S$)")
    st.caption("Reference: Raymer, Aircraft Design: A Conceptual Approach")
    
    col_plot, col_controls = st.columns([2, 1])
    with col_plot:
        st.info("📊 Interactive Constraint Plot (Takeoff, Climb, Cruise, Landing) will render here.")
        # Placeholder for matplotlib/altair chart
        st.line_chart({"Stall Limit": [0, 0], "Takeoff Limit": [0, 0], "Cruise Limit": [0, 0]}, height=300)
    
    with col_controls:
        st.markdown("##### Design Point Selection")
        st.slider("Select Wing Loading (W/S)", 20, 150, 80)
        st.slider("Select Thrust-to-Weight (T/W)", 0.1, 1.2, 0.3)
        st.button("Lock Design Point", use_container_width=True)

# --- TAB 3: Wing Geometry ---
with tab3:
    st.markdown("#### Phase 3: Detailed Wing Sizing")
    st.caption("Reference: Sadraey & Raymer")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.slider("Aspect Ratio (AR)", 2.0, 25.0, 8.0)
    with col2:
        st.slider("Sweep Angle (Λ) deg", 0, 60, 25)
    with col3:
        st.slider("Taper Ratio (λ)", 0.0, 1.0, 0.4)
    
    st.info("📐 3D Wing Planform visualization will render here based on selected W/S and W0.")

# --- TAB 4: Aerodynamics ---
with tab4:
    st.markdown("#### Phase 4: Drag Polar Estimation ($C_D = C_{D0} + K C_L^2$)")
    st.caption("Reference: Raymer (Component Build-up Method)")
    
    m1, m2 = st.columns(2)
    m1.metric("Estimated Parasite Drag ($C_{D0}$)", "---")
    m2.metric("Induced Drag Factor ($K$)", "---")
    st.info("📈 Drag Polar Curve ($C_L$ vs $C_D$) will render here.")

# --- TAB 5: Propulsion ---
with tab5:
    st.markdown("#### Phase 5: Propulsion Sizing & Integration")
    st.caption("Reference: Nicolai")
    
    st.selectbox("Engine Type", ["High-Bypass Turbofan", "Low-Bypass Turbofan", "Turboprop", "Turbojet"])
    st.number_input("Number of Engines", value=2, min_value=1, max_value=8)
    st.metric("Required Sea-Level Static Thrust (per engine)", "--- lbs")

# --- TAB 6: Stability & Tails ---
with tab6:
    st.markdown("#### Phase 6: Empennage Sizing & Stability")
    st.caption("Reference: Sadraey (Tail Volume Coefficients)")
    
    c1, c2 = st.columns(2)
    with c1:
        st.number_input("Horizontal Tail Volume Coefficient (c_HT)", value=0.9, step=0.05)
        st.metric("Horizontal Tail Area ($S_{HT}$)", "--- ft²")
    with c2:
        st.number_input("Vertical Tail Volume Coefficient (c_VT)", value=0.08, step=0.01)
        st.metric("Vertical Tail Area ($S_{VT}$)", "--- ft²")

# --- TAB 7: Global Optimization ---
with tab7:
    st.markdown("#### Phase 7: Automated Design Optimization")
    st.caption("Uses `scipy.optimize` to minimize Takeoff Weight across all phases.")
    
    st.multiselect("Select Variables to Optimize", ["Aspect Ratio", "Sweep Angle", "Cruise Altitude", "T/W", "W/S"], default=["Aspect Ratio", "Sweep Angle"])
    st.button("🔥 Run Global Optimizer", type="primary", use_container_width=True)
    st.info("Iteration logs and convergence history will appear here.")
