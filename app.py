import streamlit as st
import math
import sympy as sp

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="All-in-One Engineering & Science Hub",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- DATA & CONSTANTS ---
UNIT_CATEGORIES = {
    "Length": {
        "units": {
            "Meters (m)": 1.0, "Centimeters (cm)": 0.01, "Millimeters (mm)": 0.001,
            "Kilometers (km)": 1000.0, "Inches (in)": 0.0254, "Feet (ft)": 0.3048,
            "Yards (yd)": 0.9144, "Miles (mi)": 1609.34, "Micrometers (µm)": 1e-6,
            "Nanometers (nm)": 1e-9, "Angstroms (Å)": 1e-10, "Light Years (ly)": 9.461e15
        }, "icon": "📏"
    },
    "Mass": {
        "units": {
            "Kilograms (kg)": 1.0, "Grams (g)": 0.001, "Milligrams (mg)": 1e-6,
            "Tonnes (t)": 1000.0, "Pounds (lb)": 0.453592, "Ounces (oz)": 0.0283495,
            "Carats (ct)": 0.0002
        }, "icon": "⚖️"
    },
    "Area": {
        "units": {
            "Square Meters (m²)": 1.0, "Square Centimeters (cm²)": 1e-4, "Square Kilometers (km²)": 1e6,
            "Hectares (ha)": 10000.0, "Square Feet (ft²)": 0.092903, "Acres (ac)": 4046.86,
            "Square Miles (mi²)": 2.59e6
        }, "icon": "📐"
    },
    "Volume": {
        "units": {
            "Cubic Meters (m³)": 1.0, "Liters (L)": 0.001, "Milliliters (mL)": 1e-6,
            "Cubic Centimeters (cm³)": 1e-6, "Cubic Feet (ft³)": 0.0283168,
            "US Gallons (gal)": 0.00378541, "US Quarts (qt)": 0.000946353
        }, "icon": "🧊"
    },
    "Data": {
        "units": {
            "Bits (b)": 1.0, "Bytes (B)": 8.0, "Kilobits (kb)": 1000.0,
            "Kilobytes (kB)": 8000.0, "Megabits (Mb)": 1e6, "Megabytes (MB)": 8e6,
            "Gigabits (Gb)": 1e9, "Gigabytes (GB)": 8e9, "Terabits (Tb)": 1e12,
            "Terabytes (TB)": 8e12
        }, "icon": "💾"
    },
    "Force": {
        "units": {
            "Newtons (N)": 1.0, "Kilonewtons (kN)": 1000.0, "Pounds-force (lbf)": 4.44822,
            "Dynes (dyn)": 1e-5, "Kilogram-force (kgf)": 9.80665
        }, "icon": "💪"
    },
    "Pressure": {
        "units": {
            "Pascals (Pa)": 1.0, "Kilopascals (kPa)": 1000.0, "Bar": 100000.0,
            "Atmospheres (atm)": 101325.0, "Millimeters of Mercury (mmHg)": 133.322,
            "Pounds per Square Inch (psi)": 6894.76
        }, "icon": "🎚️"
    },
    "Energy": {
        "units": {
            "Joules (J)": 1.0, "Kilojoules (kJ)": 1000.0, "Calories (cal)": 4.184,
            "Kilocalories (kcal)": 4184.0, "Watt-hours (Wh)": 3600.0,
            "Kilowatt-hours (kWh)": 3.6e6, "Electronvolts (eV)": 1.60218e-19,
            "British Thermal Unit (BTU)": 1055.06
        }, "icon": "🔋"
    },
    "Power": {
        "units": {
            "Watts (W)": 1.0, "Kilowatts (kW)": 1000.0, "Megawatts (MW)": 1e6,
            "Horsepower (hp)": 745.7, "BTU/hour": 0.293071
        }, "icon": "⚡"
    },
    "Voltage": {
        "units": { "Volts (V)": 1.0, "Millivolts (mV)": 0.001, "Kilovolts (kV)": 1000.0 },
        "icon": "⚡"
    },
    "Electric Current": {
        "units": { "Amperes (A)": 1.0, "Milliamperes (mA)": 0.001, "Kiloamperes (kA)": 1000.0 },
        "icon": "🔌"
    },
    "Resistance": {
        "units": { "Ohms (Ω)": 1.0, "Kiloohms (kΩ)": 1000.0, "Megaohms (MΩ)": 1e6 },
        "icon": "🔩"
    },
    "Frequency": {
        "units": { "Hertz (Hz)": 1.0, "Kilohertz (kHz)": 1000.0, "Megahertz (MHz)": 1e6, "Gigahertz (GHz)": 1e9 },
        "icon": "🎵"
    },
}

# --- ENGINEERING DATA WITH UNITS AND DYNAMIC FORMULAS ---
ENGINEERING_DATA = {
    "Chemical": {
        "Heat Transfer": {
            "Physical Quantities": {
                "Heat Flux": {"units": {"W/m²": 1.0, "cal/cm²·s": 0.0239, "Btu/ft²·h": 0.3171}, "icon": "🔥"},
                "Heat Transfer Rate": {"units": {"W": 1.0, "cal/s": 0.2388, "Btu/h": 3.412}, "icon": "🔥"},
                "Thermal Conductivity": {"units": {"W/m·K": 1.0, "cal/cm·s·K": 0.0002388, "Btu/ft·h·F": 0.5778}, "icon": "🌡️"},
                "Specific Heat Capacity": {"units": {"J/kg·K": 1.0, "cal/g·K": 0.239, "Btu/lb·F": 0.239}, "icon": "🌡️"},
                "Thermal Diffusivity": {"units": {"m²/s": 1.0, "cm²/s": 1e4, "ft²/h": 1.076e-4}, "icon": "🌡️"},
                "Temperature Gradient": {"units": {"K/m": 1.0, "C/cm": 100.0, "F/ft": 1.8}, "icon": "🌡️"},
                "Convection Coefficient": {"units": {"W/m²·K": 1.0, "cal/cm²·s·C": 0.0239, "Btu/ft²·h·F": 0.3171}, "icon": "🌡️"},
                "Emissivity": {"units": {"-": 1.0}, "icon": "🌡️"},
                "Area": {"units": {"m²": 1.0, "cm²": 1e4, "ft²": 10.764}, "icon": "📐"},
                "Mass Flow Rate": {"units": {"kg/s": 1.0, "g/s": 1000.0, "lb/h": 7936.64}, "icon": "⚗️"},
                "Latent Heat": {"units": {"kJ/kg": 1.0, "cal/g": 0.239, "Btu/lb": 0.4299}, "icon": "🔥"},
                "Temperature Difference": {"units": {"K": 1.0, "C": 1.0, "F": 1.8}, "icon": "🌡️"}
            },
            "Laws": {
                "Fourier's Law": {"formula": "q = -k * A * dT_dx", "unit": "W", "variables": ["k", "A", "dT_dx"], "description": "Describes heat conduction."},
                "Newton's Law of Cooling": {"formula": "Q = h * A * (Ts - T_inf)", "unit": "W", "variables": ["h", "A", "Ts", "T_inf"], "description": "Describes heat transfer by convection."},
                "Stefan-Boltzmann Law": {"formula": "P = ε * σ * A * T**4", "unit": "W", "variables": ["ε", "σ", "A", "T"], "description": "Describes heat radiation. σ is the Stefan-Boltzmann constant (5.67e-8 W/m²K⁴)."},
                "LMTD": {"formula": "LMTD = (deltaT1 - deltaT2) / log(deltaT1 / deltaT2)", "unit": "K", "variables": ["deltaT1", "deltaT2"], "description": "Log Mean Temperature Difference for heat exchangers."}
            },
            "Dimensionless Numbers": {
                "Nusselt Number": {"formula": "h * L / k", "variables": ["h", "L", "k"]},
                "Biot Number": {"formula": "h * Lc / k", "variables": ["h", "Lc", "k"]},
                "Prandtl Number": {"formula": "ν / α", "variables": ["ν", "α"]},
            }
        },
        "Mass Transfer": {
            "Physical Quantities": {
                "Mass Flux": {"units": {"kg/m²·s": 1.0, "g/cm²·s": 0.1, "lb/ft²·s": 0.2048}, "icon": "⚗️"},
                "Diffusion Coefficient": {"units": {"m²/s": 1.0, "cm²/s": 1e4, "ft²/h": 1.076e-4}, "icon": "⚗️"},
                "Concentration Gradient": {"units": {"kg/m³·m": 1.0, "g/cm³·cm": 0.001, "lb/ft³·ft": 0.0624}, "icon": "⚗️"},
                "Mass Transfer Coefficient": {"units": {"m/s": 1.0, "cm/s": 100.0, "ft/h": 1.076}, "icon": "⚗️"},
                "Concentration": {"units": {"kg/m³": 1.0, "g/cm³": 0.001, "lb/ft³": 0.0624}, "icon": "⚗️"},
                "Density": {"units": {"kg/m³": 1.0, "g/cm³": 0.001, "lb/ft³": 0.0624}, "icon": "⚗️"},
            },
            "Laws": {
                "Fick's First Law": {"formula": "J = -D * dC_dx", "unit": "kg/m²·s", "variables": ["D", "dC_dx"], "description": "Describes molecular diffusion."},
                "Henry's Law": {"formula": "p = H * xA", "unit": "Pa", "variables": ["H", "xA"], "description": "Relates partial pressure to mole fraction in a liquid."}
            },
            "Dimensionless Numbers": {
                "Sherwood Number": {"formula": "k * L / D", "variables": ["k", "L", "D"]},
                "Schmidt Number": {"formula": "ν / D", "variables": ["ν", "D"]},
                "Peclet Number": {"formula": "V * L / D", "variables": ["V", "L", "D"]},
            }
        },
    },
    "Electrical": {
        "Circuit": {
            "Physical Quantities": {
                "Voltage": {"units": {"V": 1.0, "mV": 0.001, "kV": 1000.0}, "icon": "⚡"},
                "Current": {"units": {"A": 1.0, "mA": 0.001, "kA": 1000.0}, "icon": "⚡"},
                "Resistance": {"units": {"Ω": 1.0, "kΩ": 1000.0, "MΩ": 1e6}, "icon": "⚡"},
                "Power": {"units": {"W": 1.0, "kW": 1000.0, "MW": 1e6}, "icon": "⚡"},
                "Energy": {"units": {"J": 1.0, "kWh": 3.6e6, "cal": 4.184}, "icon": "⚡"},
                "Capacitance": {"units": {"F": 1.0, "µF": 1e-6, "pF": 1e-12}, "icon": "⚡"},
                "Inductance": {"units": {"H": 1.0, "mH": 0.001, "µH": 1e-6}, "icon": "⚡"},
                "Frequency": {"units": {"Hz": 1.0, "kHz": 1000.0, "MHz": 1e6}, "icon": "⚡"}
            },
            "Laws": {
                "Ohm's Law": {"formula": "V = I * R", "unit": "V", "variables": ["I", "R"], "description": "Relates voltage, current, and resistance."},
                "Power Law": {"formula": "P = V * I", "unit": "W", "variables": ["V", "I"], "description": "Calculates power in a DC circuit."},
                "Capacitor Energy": {"formula": "E = 0.5 * C * V**2", "unit": "J", "variables": ["C", "V"], "description": "Energy stored in a capacitor."},
                "Inductor Energy": {"formula": "E = 0.5 * L * I**2", "unit": "J", "variables": ["L", "I"], "description": "Energy stored in an inductor."}
            },
            "Dimensionless Numbers": {
                "Quality Factor (Q)": {"formula": "ω * L / R", "variables": ["ω", "L", "R"]},
                "Power Factor": {"formula": "cos(phi)", "variables": ["phi"]},
            }
        }
    }
}

# --- STYLES ---
def load_css():
    st.markdown("""
    <style>
        /* Main App background */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            background-attachment: fixed;
        }
        /* Sidebar styling */
        .css-1d391kg {
            background-color: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(10px);
        }
        /* Main content card */
        .main-container {
            background-color: rgba(255, 255, 255, 0.7);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        /* Result display box */
        .result-box {
            background-color: #e0f2f1; /* Light teal background */
            border-left: 6px solid #00796b; /* Darker teal border */
            color: #004d40; /* Dark teal text */
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
        }
        .result-text {
            font-size: 1.75rem;
            font-weight: 600;
        }
        /* Formula display */
        .formula-box {
            background-color: #f0f4f7;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 15px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 1.1em;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

# --- CONVERTER FUNCTIONS ---

def render_standard_converter(category_name):
    """Renders the UI for standard unit conversions."""
    category = UNIT_CATEGORIES.get(category_name)
    if not category:
        st.error(f"Category '{category_name}' not found.")
        return

    icon = category["icon"]
    st.header(f"{icon} {category_name} Converter")

    units = list(category["units"].keys())
    
    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        from_unit = st.selectbox("From Unit", units, key=f"from_{category_name}")
        value = st.number_input("Enter Value", value=1.0, format="%.6f", key=f"val_{category_name}")
        
    with col2:
        st.markdown("<div style='text-align: center; font-size: 2.5rem; margin-top: 45px;'>➡️</div>", unsafe_allow_html=True)
    
    with col3:
        to_unit = st.selectbox("To Unit", units, index=1, key=f"to_{category_name}")
    
    if from_unit and to_unit and value is not None:
        try:
            base_value = value * category["units"][from_unit]
            result = base_value / category["units"][to_unit]

            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(f'<p class="result-text">{value:.4f} {from_unit} = {result:.6g} {to_unit}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        except (ZeroDivisionError, KeyError):
            st.error("Invalid units selected.")


def render_temperature_converter():
    """Renders the UI for temperature conversion."""
    st.header("🌡️ Temperature Converter")
    
    temp_units = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        from_unit = st.selectbox("From Unit", temp_units, key="from_temp")
        value = st.number_input("Enter Temperature", value=0.0, format="%.2f", key="val_temp")
        
    with col2:
        st.markdown("<div style='text-align: center; font-size: 2.5rem; margin-top: 45px;'>➡️</div>", unsafe_allow_html=True)
    
    with col3:
        to_unit = st.selectbox("To Unit", temp_units, index=1, key="to_temp")

    if from_unit == to_unit:
        result = value
    else:
        if from_unit == "Fahrenheit (°F)":
            celsius = (value - 32) * 5.0 / 9.0
        elif from_unit == "Kelvin (K)":
            celsius = value - 273.15
        else:
            celsius = value
        
        if to_unit == "Fahrenheit (°F)":
            result = (celsius * 9.0 / 5.0) + 32
        elif to_unit == "Kelvin (K)":
            result = celsius + 273.15
        else:
            result = celsius
            
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f'<p class="result-text">{value:.2f} {from_unit} = {result:.2f} {to_unit}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_bmi_calculator():
    """Renders the UI for BMI calculation."""
    st.header("🏋️ Body Mass Index (BMI) Calculator")
    st.info("BMI is a measure of body fat based on height and weight.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight_unit = st.radio("Weight Unit", ["Kilograms (kg)", "Pounds (lb)"])
        weight = st.number_input("Enter Your Weight", min_value=0.0, value=70.0, format="%.2f")
        
    with col2:
        height_unit = st.radio("Height Unit", ["Centimeters (cm)", "Meters (m)", "Feet & Inches"])
        height_m = 0
        if height_unit == "Feet & Inches":
            h_ft = st.number_input("Feet", min_value=0, value=5)
            h_in = st.number_input("Inches", min_value=0, value=9)
            height_m = (h_ft * 12 + h_in) * 0.0254
        else:
            height = st.number_input(f"Enter Your Height in {height_unit.split(' ')[0]}", min_value=0.0, value=175.0 if height_unit == "Centimeters (cm)" else 1.75, format="%.2f")
            height_m = height / 100 if height_unit == "Centimeters (cm)" else height

    weight_kg = weight * 0.453592 if weight_unit == "Pounds (lb)" else weight
    
    if st.button("Calculate BMI", use_container_width=True):
        if height_m > 0 and weight_kg > 0:
            bmi = weight_kg / (height_m ** 2)
            
            if bmi < 18.5:
                category = "Underweight"
                color = "blue"
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
                color = "green"
            elif 25 <= bmi < 30:
                category = "Overweight"
                color = "orange"
            else:
                category = "Obese"
                color = "red"
            
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(f'<p class="result-text">Your BMI is {bmi:.2f}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:{color}; font-size:1.2rem; font-weight:bold;">Category: {category}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Please enter valid weight and height.")


def render_per_unit_calculator():
    """Renders the UI for Per Unit calculations in electrical engineering."""
    st.header("⚡ Per-Unit (PU) System Calculator")
    st.info("A tool for power system analysis. All calculations assume a three-phase system.")
    
    st.subheader("System Base Values")
    col1, col2 = st.columns(2)
    with col1:
        base_mva = st.number_input("Base MVA (S_base)", min_value=0.1, value=100.0, format="%.2f")
    with col2:
        base_kv = st.number_input("Base Voltage (V_base, Line-to-Line)", min_value=0.1, value=13.8, format="%.2f")

    if base_mva > 0 and base_kv > 0:
        z_base = (base_kv ** 2) / base_mva
        i_base = (base_mva * 1000) / (math.sqrt(3) * base_kv)
        
        with st.expander("Derived Base Values", expanded=True):
            st.metric(label="Base Impedance (Z_base)", value=f"{z_base:.4f} Ω")
            st.metric(label="Base Current (I_base)", value=f"{i_base:.4f} A")
    
    st.markdown("---")
    
    calc_type = st.selectbox("Choose Conversion Type", ["Actual Value to Per-Unit", "Per-Unit to Actual Value"])
    
    if calc_type == "Actual Value to Per-Unit":
        st.subheader("Convert Actual Value to PU")
        param_type = st.radio("Select Parameter", ["Impedance (Ω)", "Current (A)", "Voltage (kV)"])
        
        if param_type == "Impedance (Ω)":
            actual_val = st.number_input("Actual Impedance (Z_actual) in Ω", value=z_base*0.05 if 'z_base' in locals() else 5.0, format="%.4f")
            pu_val = actual_val / z_base if 'z_base' in locals() and z_base > 0 else 0
            st.success(f"Per-Unit Impedance = {pu_val:.6f} pu")
            
        elif param_type == "Current (A)":
            actual_val = st.number_input("Actual Current (I_actual) in A", value=i_base if 'i_base' in locals() else 10.0, format="%.4f")
            pu_val = actual_val / i_base if 'i_base' in locals() and i_base > 0 else 0
            st.success(f"Per-Unit Current = {pu_val:.6f} pu")
            
        elif param_type == "Voltage (kV)":
            actual_val = st.number_input("Actual Voltage (V_actual) in kV (L-L)", value=base_kv if 'base_kv' in locals() else 13.8, format="%.4f")
            pu_val = actual_val / base_kv if 'base_kv' in locals() and base_kv > 0 else 0
            st.success(f"Per-Unit Voltage = {pu_val:.6f} pu")

    else:
        st.subheader("Convert PU to Actual Value")
        param_type = st.radio("Select Parameter", ["Impedance (pu)", "Current (pu)", "Voltage (pu)"])

        if param_type == "Impedance (pu)":
            pu_val = st.number_input("Per-Unit Impedance (Z_pu)", value=0.05, format="%.6f")
            actual_val = pu_val * z_base if 'z_base' in locals() else 0
            st.success(f"Actual Impedance = {actual_val:.4f} Ω")

        elif param_type == "Current (pu)":
            pu_val = st.number_input("Per-Unit Current (I_pu)", value=1.0, format="%.6f")
            actual_val = pu_val * i_base if 'i_base' in locals() else 0
            st.success(f"Actual Current = {actual_val:.4f} A")

        elif param_type == "Voltage (pu)":
            pu_val = st.number_input("Per-Unit Voltage (V_pu)", value=1.0, format="%.6f")
            actual_val = pu_val * base_kv if 'base_kv' in locals() else 0
            st.success(f"Actual Voltage = {actual_val:.4f} kV (L-L)")


def render_engineering_tools():
    """Renders the UI for Chemical and Electrical engineering calculations."""
    st.header("🧪⚡ Engineering Calculators")
    st.info("A comprehensive hub for engineering-specific conversions and formula calculations.")

    eng_category = st.sidebar.selectbox("Choose Discipline", ["Chemical", "Electrical"])
    eng_section = st.sidebar.selectbox("Choose Section", list(ENGINEERING_DATA[eng_category].keys()))
    data = ENGINEERING_DATA[eng_category][eng_section]

    selection_type = st.sidebar.radio("Select Tool Type", ["Physical Quantity", "Law", "Dimensionless Number"])

    if selection_type == "Physical Quantity":
        st.subheader("Physical Quantity Conversion")
        pq = st.selectbox("Select Physical Quantity", list(data["Physical Quantities"].keys()))
        pq_data = data["Physical Quantities"][pq]
        
        col1, col2 = st.columns(2)
        with col1:
            value = st.number_input(f"Enter value of {pq}", value=1.0, format="%.6f")
            unit_from = st.selectbox("From Unit", list(pq_data["units"].keys()))
        with col2:
            unit_to = st.selectbox("To Unit", list(pq_data["units"].keys()))

        if value is not None and unit_from and unit_to:
            try:
                converted_value = value * pq_data["units"][unit_to] / pq_data["units"][unit_from]
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f'<p class="result-text">{value:.4f} {unit_from} = {converted_value:.6g} {unit_to}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            except (ZeroDivisionError, KeyError):
                st.error("Invalid units selected.")

    elif selection_type == "Law":
        st.subheader("Law Calculation")
        law = st.selectbox("Select Law", list(data["Laws"].keys()))
        law_data = data["Laws"][law]
        formula_str = law_data["formula"]
        var_names = law_data.get("variables", [])
        
        st.markdown(f'<div class="formula-box">**Formula:** {formula_str}</div>', unsafe_allow_html=True)
        st.info(f"**Description:** {law_data.get('description', 'No description provided.')}")
        
        if var_names:
            st.markdown("---")
            st.subheader("Input Variables")
            var_inputs = {}
            for var in var_names:
                var_inputs[var] = st.number_input(f"Enter value for **{var}**", value=1.0)
            
            if st.button("Calculate", key=f"calc_{law}"):
                try:
                    expr = sp.sympify(formula_str.replace("^", "**"))
                    # Special case for log
                    if "log" in formula_str:
                        expr = expr.subs({"log": sp.log})
                    
                    # Convert inputs to a dictionary for sympy
                    subs_dict = {sp.Symbol(var): val for var, val in var_inputs.items()}
                    result = expr.subs(subs_dict)
                    
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown(f'<p class="result-text">Result = {result:.6g} {law_data["unit"]}</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error: {e}. Please check the formula and inputs.")

    elif selection_type == "Dimensionless Number":
        st.subheader("Dimensionless Number Calculation")
        dn = st.selectbox("Select Dimensionless Number", list(data["Dimensionless Numbers"].keys()))
        dn_data = data["Dimensionless Numbers"][dn]
        formula_str = dn_data["formula"]
        var_names = dn_data.get("variables", [])
        
        st.markdown(f'<div class="formula-box">**Formula:** {formula_str}</div>', unsafe_allow_html=True)
        
        if var_names:
            st.markdown("---")
            st.subheader("Input Variables")
            var_inputs = {}
            for var in var_names:
                var_inputs[var] = st.number_input(f"Enter value for **{var}**", value=1.0)

            if st.button("Calculate", key=f"calc_{dn}"):
                try:
                    expr = sp.sympify(formula_str.replace("^", "**"))
                    
                    subs_dict = {sp.Symbol(var): val for var, val in var_inputs.items()}
                    dn_result = expr.subs(subs_dict)
                    
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown(f'<p class="result-text">Result = {dn_result:.6g} (Dimensionless)</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}. Please check the formula and inputs.")


# --- MAIN APP LAYOUT ---
load_css()
st.title("🌟 All-in-One Engineering & Science Hub")
st.markdown("Tagline: The only conversion hub engineers will ever need.")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio(
    "Choose a Tool",
    ["General Unit Converter", "🌡️ Temperature", "🏋️ BMI Calculator", "⚡ Per-Unit System", "🧪⚡ Engineering Calculators"]
)
st.sidebar.markdown("---")
st.sidebar.info(
    "This app provides a suite of tools for a wide range of conversions and calculations across various scientific and engineering disciplines."
)

# --- MAIN CONTENT AREA ---
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    if app_mode == "General Unit Converter":
        st.header("Select a Category")
        category_names = list(UNIT_CATEGORIES.keys())
        selected_category = st.radio(
            "Conversion Category:",
            category_names,
            horizontal=True,
            label_visibility="collapsed"
        )
        st.markdown("---")
        render_standard_converter(selected_category)
        
    elif app_mode == "🌡️ Temperature":
        render_temperature_converter()
        
    elif app_mode == "🏋️ BMI Calculator":
        render_bmi_calculator()
        
    elif app_mode == "⚡ Per-Unit System":
        render_per_unit_calculator()

    elif app_mode == "🧪⚡ Engineering Calculators":
        render_engineering_tools()
        
    st.markdown('</div>', unsafe_allow_html=True)
