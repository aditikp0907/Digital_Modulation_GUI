import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Digital Modulation Studio",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "random_seed" not in st.session_state:
    st.session_state.random_seed = 42


# ============================================================
# PROFESSIONAL DEPLOYMENT-SAFE DARK BLUE THEME
# ============================================================

st.markdown(
    """
    <style>

    /* MAIN APPLICATION */

    html,
    body,
    [data-testid="stAppViewContainer"],
    .stApp {
        background-color: #0B1120 !important;
        color: #E5E7EB !important;
    }

    [data-testid="stHeader"] {
        background-color: rgba(11, 17, 32, 0.96) !important;
    }

    [data-testid="stMainBlockContainer"] {
        background-color: #0B1120 !important;
    }


    /* MAIN PAGE TEXT */

    [data-testid="stMain"] h1 {
        color: #F8FAFC !important;
    }

    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3 {
        color: #DBEAFE !important;
    }

    [data-testid="stMain"] p,
    [data-testid="stMain"] label,
    [data-testid="stMain"] li {
        color: #CBD5E1 !important;
    }


    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #263449;
    }

    [data-testid="stSidebar"] h1 {
        color: #F8FAFC !important;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #BFDBFE !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #CBD5E1;
    }


    /* SELECT BOXES AND INPUTS */

    [data-baseweb="select"] > div {
        background-color: #182235 !important;
        border-color: #334155 !important;
        color: #F8FAFC !important;
    }

    [data-baseweb="select"] span {
        color: #F8FAFC !important;
    }

    [data-baseweb="popover"] {
        color: #E5E7EB !important;
    }

    [role="listbox"] {
        background-color: #182235 !important;
    }

    [role="option"] {
        color: #E5E7EB !important;
        background-color: #182235 !important;
    }

    [role="option"]:hover {
        background-color: #24324A !important;
    }

    [data-testid="stNumberInput"] input {
        background-color: #182235 !important;
        color: #F8FAFC !important;
        border-color: #334155 !important;
    }


    /* SLIDERS */

    [data-testid="stSlider"] label {
        color: #CBD5E1 !important;
    }

    [data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
        background-color: #3B82F6 !important;
    }


    /* CHECKBOX */

    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] p {
        color: #CBD5E1 !important;
    }


    /* BUTTON */

    div.stButton > button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;

        border: 1px solid #3B82F6 !important;
        border-radius: 8px;

        font-weight: 600;

        transition:
            background-color 0.2s ease,
            border-color 0.2s ease,
            transform 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;

        border-color: #60A5FA !important;

        transform: translateY(-1px);
    }

    div.stButton > button:focus {
        color: #FFFFFF !important;
        border-color: #93C5FD !important;
    }


    /* INFO BOX */

    [data-testid="stAlert"] {
        background-color: #111D33 !important;
        border: 1px solid #29466F !important;
        border-radius: 8px;
    }

    [data-testid="stAlert"] p {
        color: #DBEAFE !important;
    }

    [data-testid="stAlert"] svg {
        color: #60A5FA !important;
        fill: #60A5FA !important;
    }


    /* METRIC CARDS */

    [data-testid="stMetric"] {
        background-color: #111827 !important;

        border: 1px solid #263449;
        border-radius: 10px;

        padding: 18px;
    }

    [data-testid="stMetricLabel"] p {
        color: #94A3B8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
    }


    /* CODE BLOCK */

    [data-testid="stCodeBlock"] {
        border: 1px solid #334155;
        border-radius: 8px;
    }

    [data-testid="stCodeBlock"] pre {
        background-color: #111827 !important;
        color: #E2E8F0 !important;
    }


    /* DATAFRAME */

    [data-testid="stDataFrame"] {
        border: 1px solid #334155;
        border-radius: 8px;
        overflow: hidden;
    }


    /* EXPANDER */

    [data-testid="stExpander"] {
        background-color: #111827 !important;

        border: 1px solid #334155 !important;
        border-radius: 8px;
    }

    [data-testid="stExpander"] summary {
        color: #DBEAFE !important;
    }

    [data-testid="stExpander"] p {
        color: #CBD5E1 !important;
    }


    /* DIVIDERS */

    hr {
        border-color: #263449 !important;
    }


    /* LINKS */

    a {
        color: #60A5FA !important;
    }

    a:hover {
        color: #93C5FD !important;
    }


    /* SCROLLBAR */

    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #0B1120;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MATPLOTLIB THEME
# ============================================================

PLOT_BACKGROUND = "#111827"
PLOT_AREA = "#0F172A"
PLOT_TEXT = "#E5E7EB"
PLOT_GRID = "#475569"
PLOT_LINE = "#60A5FA"
PLOT_ACCENT = "#A78BFA"


def style_figure(figure):
    figure.patch.set_facecolor(PLOT_BACKGROUND)


def format_axis(
    axis,
    title,
    xlabel="Time (seconds)",
    ylabel="Amplitude",
):
    axis.set_facecolor(PLOT_AREA)

    axis.set_title(
        title,
        color=PLOT_TEXT,
        fontweight="bold",
        pad=12,
    )

    axis.set_xlabel(
        xlabel,
        color=PLOT_TEXT,
    )

    axis.set_ylabel(
        ylabel,
        color=PLOT_TEXT,
    )

    axis.tick_params(
        axis="both",
        colors=PLOT_TEXT,
    )

    axis.grid(
        True,
        alpha=0.28,
        color=PLOT_GRID,
    )

    for spine in axis.spines.values():
        spine.set_color(PLOT_GRID)


def display_figure(figure):
    style_figure(figure)

    figure.tight_layout()

    st.pyplot(
        figure,
        use_container_width=True,
    )

    plt.close(figure)


# ============================================================
# MODULATION INFORMATION
# ============================================================

TECHNIQUE_INFO = {
    "AM": {
        "name": "Amplitude Modulation (AM)",
        "description":
            "AM varies the amplitude of a high-frequency carrier according "
            "to the instantaneous amplitude of the message signal. "
            "AM is simple to implement but is vulnerable to amplitude noise.",
        "bits": "N/A",
        "efficiency": "Low",
        "robustness": "Low",
    },

    "FM": {
        "name": "Frequency Modulation (FM)",
        "description":
            "FM varies the instantaneous frequency of the carrier according "
            "to the message signal. FM provides better noise immunity than "
            "AM but generally requires more bandwidth.",
        "bits": "N/A",
        "efficiency": "Low",
        "robustness": "High",
    },

    "ASK": {
        "name": "Amplitude Shift Keying (ASK)",
        "description":
            "ASK represents binary information using changes in carrier "
            "amplitude. In On-Off Keying, bit 1 is represented by the "
            "carrier and bit 0 by the absence of the carrier.",
        "bits": "1",
        "efficiency": "Low",
        "robustness": "Low",
    },

    "BPSK": {
        "name": "Binary Phase Shift Keying (BPSK)",
        "description":
            "BPSK represents binary information using two carrier phases "
            "separated by 180 degrees. Its large signal-state separation "
            "provides excellent noise robustness.",
        "bits": "1",
        "efficiency": "Moderate",
        "robustness": "Very High",
    },

    "QPSK": {
        "name": "Quadrature Phase Shift Keying (QPSK)",
        "description":
            "QPSK maps pairs of bits to four different phase states. "
            "Each QPSK symbol carries two bits and provides greater "
            "bandwidth efficiency than BPSK.",
        "bits": "2",
        "efficiency": "High",
        "robustness": "High",
    },

    "16-QAM": {
        "name": "16-Quadrature Amplitude Modulation",
        "description":
            "16-QAM combines amplitude and phase variation using sixteen "
            "constellation points. Each symbol carries four bits, providing "
            "high spectral efficiency at the cost of increased sensitivity "
            "to noise.",
        "bits": "4",
        "efficiency": "Very High",
        "robustness": "Moderate",
    },

    "OFDM": {
        "name": "Orthogonal Frequency Division Multiplexing (OFDM)",
        "description":
            "OFDM divides a broadband channel into many narrowband "
            "orthogonal subcarriers. Frequency-domain symbols are converted "
            "into the transmitted time-domain signal using the IFFT.",
        "bits": "Depends",
        "efficiency": "Very High",
        "robustness": "High",
    },
}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def add_awgn(signal, snr_db, rng):
    signal_power = np.mean(np.abs(signal) ** 2)

    if signal_power == 0:
        return signal.copy()

    snr_linear = 10 ** (snr_db / 10)
    noise_power = signal_power / snr_linear

    if np.iscomplexobj(signal):
        noise = np.sqrt(noise_power / 2) * (
            rng.standard_normal(signal.shape)
            + 1j * rng.standard_normal(signal.shape)
        )

    else:
        noise = (
            np.sqrt(noise_power)
            * rng.standard_normal(signal.shape)
        )

    return signal + noise


# ============================================================
# MODULATION FUNCTIONS
# ============================================================

def generate_am(fs, duration, fm, fc, modulation_index):
    t = np.arange(0, duration, 1 / fs)

    message = np.cos(2 * np.pi * fm * t)
    carrier = np.cos(2 * np.pi * fc * t)

    modulated_signal = (
        1 + modulation_index * message
    ) * carrier

    return t, message, carrier, modulated_signal


def generate_fm(fs, duration, fm, fc, beta):
    t = np.arange(0, duration, 1 / fs)

    message = np.cos(2 * np.pi * fm * t)
    carrier = np.cos(2 * np.pi * fc * t)

    frequency_deviation = beta * fm

    integrated_message = np.cumsum(message) / fs

    phase = (
        2 * np.pi * fc * t
        + 2 * np.pi
        * frequency_deviation
        * integrated_message
    )

    modulated_signal = np.cos(phase)

    return t, message, carrier, modulated_signal


def generate_ask(fs, fc, bit_count, rng):
    samples_per_bit = 100

    bits = rng.integers(0, 2, bit_count)

    digital_signal = np.repeat(
        bits,
        samples_per_bit,
    )

    t = np.arange(len(digital_signal)) / fs

    carrier = np.cos(2 * np.pi * fc * t)

    modulated_signal = digital_signal * carrier

    return t, bits, digital_signal, modulated_signal


def generate_bpsk(fs, fc, bit_count, rng):
    samples_per_bit = 100

    bits = rng.integers(0, 2, bit_count)

    bipolar_bits = 2 * bits - 1

    digital_signal = np.repeat(
        bipolar_bits,
        samples_per_bit,
    )

    t = np.arange(len(digital_signal)) / fs

    carrier = np.cos(2 * np.pi * fc * t)

    modulated_signal = digital_signal * carrier

    return t, bits, digital_signal, modulated_signal


def generate_qpsk(bit_count, rng):
    if bit_count % 2 != 0:
        bit_count += 1

    bits = rng.integers(0, 2, bit_count)

    pairs = bits.reshape(-1, 2)

    mapping = {
        (0, 0): 1 + 1j,
        (0, 1): -1 + 1j,
        (1, 1): -1 - 1j,
        (1, 0): 1 - 1j,
    }

    symbols = np.array(
        [
            mapping[tuple(pair)]
            for pair in pairs
        ],
        dtype=complex,
    ) / np.sqrt(2)

    return bits, symbols


def generate_16qam(bit_count, rng):
    remainder = bit_count % 4

    if remainder != 0:
        bit_count += 4 - remainder

    bits = rng.integers(0, 2, bit_count)

    groups = bits.reshape(-1, 4)

    gray_map = {
        (0, 0): -3,
        (0, 1): -1,
        (1, 1): 1,
        (1, 0): 3,
    }

    symbols = []

    for group in groups:
        i_value = gray_map[tuple(group[:2])]
        q_value = gray_map[tuple(group[2:])]

        symbols.append(
            i_value + 1j * q_value
        )

    symbols = (
        np.asarray(symbols, dtype=complex)
        / np.sqrt(10)
    )

    return bits, symbols


def generate_ofdm(subcarriers, rng):
    bits = rng.integers(
        0,
        2,
        2 * subcarriers,
    )

    pairs = bits.reshape(-1, 2)

    qpsk_symbols = (
        (2 * pairs[:, 0] - 1)
        + 1j * (2 * pairs[:, 1] - 1)
    ) / np.sqrt(2)

    ofdm_signal = np.fft.ifft(qpsk_symbols)

    return bits, qpsk_symbols, ofdm_signal


# ============================================================
# PAGE HEADER
# ============================================================

st.title("📡 Digital Modulation Studio")

st.subheader(
    "Generation and Analysis of Digital Modulation Techniques"
)

st.write(
    "Interactive Python-based simulation and visualization of "
    "AM, FM, ASK, BPSK, QPSK, 16-QAM and OFDM signals."
)

st.info(
    "Select a modulation technique and adjust the parameters "
    "from the sidebar. The visualization updates dynamically."
)

st.divider()


# ============================================================
# SIDEBAR CONTROLS
# ============================================================

with st.sidebar:
    st.title("Signal Configuration")

    technique = st.selectbox(
        "Modulation Technique",
        [
            "AM",
            "FM",
            "ASK",
            "BPSK",
            "QPSK",
            "16-QAM",
            "OFDM",
        ],
    )

    st.subheader("General Parameters")

    sample_rate = st.number_input(
        "Sample Rate (Hz)",
        min_value=500,
        max_value=20000,
        value=2000,
        step=500,
    )

    duration = st.slider(
        "Duration (seconds)",
        min_value=0.2,
        max_value=3.0,
        value=1.0,
        step=0.1,
    )

    message_frequency = st.slider(
        "Message Frequency (Hz)",
        min_value=1.0,
        max_value=100.0,
        value=5.0,
        step=1.0,
    )

    carrier_frequency = st.slider(
        "Carrier Frequency (Hz)",
        min_value=10.0,
        max_value=500.0,
        value=50.0,
        step=10.0,
    )

    modulation_index = st.slider(
        "Modulation Index / FM Beta",
        min_value=0.1,
        max_value=5.0,
        value=0.7,
        step=0.1,
    )

    bit_count = st.slider(
        "Number of Bits",
        min_value=4,
        max_value=256,
        value=16,
        step=4,
    )

    ofdm_subcarriers = st.select_slider(
        "OFDM Subcarriers",
        options=[
            8,
            16,
            32,
            64,
            128,
            256,
        ],
        value=64,
    )

    st.subheader("Channel Configuration")

    noise_enabled = st.checkbox(
        "Add AWGN Noise"
    )

    snr_db = st.slider(
        "SNR (dB)",
        min_value=-10,
        max_value=50,
        value=20,
        step=1,
        disabled=not noise_enabled,
    )

    if st.button(
        "Generate New Random Data",
        use_container_width=True,
    ):
        st.session_state.random_seed += 1


# ============================================================
# VALIDATION
# ============================================================

if carrier_frequency >= sample_rate / 2:
    st.error(
        "Carrier frequency must be less than half of the "
        "sample rate to satisfy the Nyquist sampling requirement."
    )

    st.stop()


if (
    technique in ["AM", "FM"]
    and message_frequency >= carrier_frequency
):
    st.warning(
        "For a clearer analog modulation demonstration, "
        "keep the message frequency below the carrier frequency."
    )


# ============================================================
# TECHNIQUE INFORMATION
# ============================================================

info = TECHNIQUE_INFO[technique]

st.subheader(info["name"])

st.write(info["description"])

metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    "Bits per Symbol",
    info["bits"],
)

metric2.metric(
    "Bandwidth Efficiency",
    info["efficiency"],
)

metric3.metric(
    "Noise Robustness",
    info["robustness"],
)

st.divider()


# ============================================================
# RANDOM NUMBER GENERATOR
# ============================================================

rng = np.random.default_rng(
    st.session_state.random_seed
)


# ============================================================
# SIGNAL VISUALIZATION
# ============================================================

st.header("Interactive Signal Visualization")


# ---------------- AM ----------------

if technique == "AM":
    t, message, carrier, clean_signal = generate_am(
        sample_rate,
        duration,
        message_frequency,
        carrier_frequency,
        modulation_index,
    )

    signal = (
        add_awgn(clean_signal, snr_db, rng)
        if noise_enabled
        else clean_signal
    )

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(12, 8),
    )

    axes[0].plot(
        t,
        message,
        color=PLOT_LINE,
    )

    format_axis(
        axes[0],
        "Message Signal",
    )

    axes[1].plot(
        t,
        carrier,
        color=PLOT_ACCENT,
    )

    format_axis(
        axes[1],
        "Carrier Signal",
    )

    axes[2].plot(
        t,
        signal,
        color=PLOT_LINE,
    )

    format_axis(
        axes[2],
        "AM Modulated Signal",
    )

    display_figure(fig)


# ---------------- FM ----------------

elif technique == "FM":
    t, message, carrier, clean_signal = generate_fm(
        sample_rate,
        duration,
        message_frequency,
        carrier_frequency,
        modulation_index,
    )

    signal = (
        add_awgn(clean_signal, snr_db, rng)
        if noise_enabled
        else clean_signal
    )

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(12, 8),
    )

    axes[0].plot(
        t,
        message,
        color=PLOT_LINE,
    )

    format_axis(
        axes[0],
        "Message Signal",
    )

    axes[1].plot(
        t,
        carrier,
        color=PLOT_ACCENT,
    )

    format_axis(
        axes[1],
        "Reference Carrier Signal",
    )

    axes[2].plot(
        t,
        signal,
        color=PLOT_LINE,
    )

    format_axis(
        axes[2],
        "FM Modulated Signal",
    )

    display_figure(fig)


# ---------------- ASK ----------------

elif technique == "ASK":
    t, bits, data, clean_signal = generate_ask(
        sample_rate,
        carrier_frequency,
        bit_count,
        rng,
    )

    signal = (
        add_awgn(clean_signal, snr_db, rng)
        if noise_enabled
        else clean_signal
    )

    st.code(
        "Binary Data: "
        + "".join(map(str, bits))
    )

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(12, 7),
    )

    axes[0].plot(
        t,
        data,
        color=PLOT_ACCENT,
    )

    format_axis(
        axes[0],
        "Binary Data",
    )

    axes[1].plot(
        t,
        signal,
        color=PLOT_LINE,
    )

    format_axis(
        axes[1],
        "ASK Modulated Signal",
    )

    display_figure(fig)


# ---------------- BPSK ----------------

elif technique == "BPSK":
    t, bits, data, clean_signal = generate_bpsk(
        sample_rate,
        carrier_frequency,
        bit_count,
        rng,
    )

    signal = (
        add_awgn(clean_signal, snr_db, rng)
        if noise_enabled
        else clean_signal
    )

    st.code(
        "Binary Data: "
        + "".join(map(str, bits))
    )

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(12, 7),
    )

    axes[0].plot(
        t,
        data,
        color=PLOT_ACCENT,
    )

    format_axis(
        axes[0],
        "Bipolar Binary Data",
    )

    axes[1].plot(
        t,
        signal,
        color=PLOT_LINE,
    )

    format_axis(
        axes[1],
        "BPSK Modulated Signal",
    )

    display_figure(fig)


# ---------------- QPSK ----------------

elif technique == "QPSK":
    bits, clean_symbols = generate_qpsk(
        bit_count,
        rng,
    )

    symbols = (
        add_awgn(clean_symbols, snr_db, rng)
        if noise_enabled
        else clean_symbols
    )

    st.code(
        "Binary Data: "
        + "".join(map(str, bits))
    )

    fig, ax = plt.subplots(
        figsize=(8, 7),
    )

    ax.scatter(
        symbols.real,
        symbols.imag,
        s=80,
        alpha=0.85,
        color=PLOT_LINE,
    )

    ax.axhline(
        0,
        linewidth=1,
        color=PLOT_GRID,
    )

    ax.axvline(
        0,
        linewidth=1,
        color=PLOT_GRID,
    )

    format_axis(
        ax,
        "QPSK Constellation Diagram",
        "In-Phase Component (I)",
        "Quadrature Component (Q)",
    )

    ax.set_aspect(
        "equal",
        adjustable="box",
    )

    display_figure(fig)


# ---------------- 16-QAM ----------------

elif technique == "16-QAM":
    bits, clean_symbols = generate_16qam(
        bit_count,
        rng,
    )

    symbols = (
        add_awgn(clean_symbols, snr_db, rng)
        if noise_enabled
        else clean_symbols
    )

    st.code(
        "Binary Data: "
        + "".join(map(str, bits))
    )

    fig, ax = plt.subplots(
        figsize=(8, 7),
    )

    ax.scatter(
        symbols.real,
        symbols.imag,
        s=75,
        alpha=0.85,
        color=PLOT_ACCENT,
    )

    ax.axhline(
        0,
        linewidth=1,
        color=PLOT_GRID,
    )

    ax.axvline(
        0,
        linewidth=1,
        color=PLOT_GRID,
    )

    format_axis(
        ax,
        "16-QAM Constellation Diagram",
        "In-Phase Component (I)",
        "Quadrature Component (Q)",
    )

    ax.set_aspect(
        "equal",
        adjustable="box",
    )

    display_figure(fig)


# ---------------- OFDM ----------------

elif technique == "OFDM":
    bits, qpsk_symbols, clean_signal = generate_ofdm(
        ofdm_subcarriers,
        rng,
    )

    signal = (
        add_awgn(clean_signal, snr_db, rng)
        if noise_enabled
        else clean_signal
    )

    samples = np.arange(
        ofdm_subcarriers
    )

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(12, 9),
    )

    markerline, stemlines, baseline = axes[0].stem(
        samples,
        np.abs(qpsk_symbols),
        basefmt=" ",
    )

    plt.setp(
        markerline,
        color=PLOT_LINE,
    )

    plt.setp(
        stemlines,
        color=PLOT_LINE,
    )

    format_axis(
        axes[0],
        "Frequency-Domain QPSK Subcarrier Symbols",
        "Subcarrier Index",
        "Magnitude",
    )

    axes[1].plot(
        samples,
        signal.real,
        color=PLOT_ACCENT,
    )

    format_axis(
        axes[1],
        "OFDM Time-Domain Signal - Real Component",
        "Sample Index",
        "Amplitude",
    )

    axes[2].plot(
        samples,
        np.abs(signal),
        color=PLOT_LINE,
    )

    format_axis(
        axes[2],
        "OFDM Time-Domain Signal Magnitude",
        "Sample Index",
        "Magnitude",
    )

    display_figure(fig)


# ============================================================
# COMPARISON TABLE
# ============================================================

st.divider()

st.header(
    "Bandwidth Efficiency and Noise Robustness Comparison"
)

comparison_data = {
    "Technique": [
        "AM",
        "FM",
        "ASK",
        "BPSK",
        "QPSK",
        "16-QAM",
        "OFDM",
    ],

    "Type": [
        "Analog",
        "Analog",
        "Digital",
        "Digital",
        "Digital",
        "Digital",
        "Multi-Carrier",
    ],

    "Bits / Symbol": [
        "N/A",
        "N/A",
        "1",
        "1",
        "2",
        "4",
        "Depends",
    ],

    "Bandwidth Efficiency": [
        "Low",
        "Low",
        "Low",
        "Moderate",
        "High",
        "Very High",
        "Very High",
    ],

    "Noise Robustness": [
        "Low",
        "High",
        "Low",
        "Very High",
        "High",
        "Moderate",
        "High",
    ],

    "Observation": [
        "Sensitive to amplitude noise.",
        "Better noise immunity but uses more bandwidth.",
        "Simple but vulnerable to amplitude noise.",
        "Excellent noise robustness.",
        "Good balance of efficiency and robustness.",
        "High spectral efficiency but requires higher SNR.",
        "Resistant to frequency-selective fading.",
    ],
}

st.dataframe(
    comparison_data,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# ANALYSIS AND CONCLUSION
# ============================================================

st.divider()

with st.expander(
    "Practical Analysis and Conclusion",
    expanded=False,
):
    st.write(
        """
        The simulation demonstrates the major trade-offs among analog,
        digital, and multi-carrier modulation techniques.

        AM is simple but sensitive to amplitude noise, whereas FM provides
        improved noise immunity at the cost of increased bandwidth.

        ASK is easy to implement but vulnerable to amplitude disturbances.
        BPSK provides excellent noise robustness because its two signal
        states have large Euclidean separation.

        QPSK improves bandwidth efficiency by carrying two bits per symbol.
        16-QAM carries four bits per symbol and provides greater spectral
        efficiency, but its more closely spaced constellation points make
        it more sensitive to noise.

        OFDM maps symbols onto multiple orthogonal subcarriers and applies
        the IFFT to produce the transmitted time-domain waveform. Its
        multi-carrier structure provides resistance to frequency-selective
        fading and makes it suitable for modern broadband wireless systems.
        """
    )