import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


# ============================================================
# DIGITAL MODULATION STUDIO
# Practical 1: Generation and Analysis of Digital Modulation
# Techniques (AM, FM, ASK, PSK, QAM, OFDM)
# ============================================================


class DigitalModulationStudio:

    def __init__(self, root):

        self.root = root

        # ----------------------------------------------------
        # MAIN WINDOW
        # ----------------------------------------------------

        self.root.title("Digital Modulation Studio")

        self.root.geometry("1400x850")

        self.root.minsize(1100, 700)

        self.root.configure(bg="#EAF4FF")

        # ----------------------------------------------------
        # BLUE THEME
        # ----------------------------------------------------

        self.COLORS = {
            "navy": "#082A4A",
            "dark_blue": "#0B3D66",
            "primary": "#1565C0",
            "secondary": "#1976D2",
            "accent": "#42A5F5",
            "light_blue": "#EAF4FF",
            "very_light": "#F7FBFF",
            "white": "#FFFFFF",
            "text": "#16324F",
            "muted": "#607D8B",
            "success": "#2E7D32",
            "warning": "#ED6C02",
            "danger": "#C62828",
            "border": "#B8D7F0"
        }

        # ----------------------------------------------------
        # APPLICATION STATE VARIABLES
        # ----------------------------------------------------

        self.modulation_var = tk.StringVar(value="AM")

        self.message_frequency_var = tk.DoubleVar(value=5.0)

        self.carrier_frequency_var = tk.DoubleVar(value=50.0)

        self.modulation_index_var = tk.DoubleVar(value=0.7)

        self.sample_rate_var = tk.IntVar(value=2000)

        self.duration_var = tk.DoubleVar(value=1.0)

        self.snr_var = tk.DoubleVar(value=20.0)

        self.bit_count_var = tk.IntVar(value=16)

        self.ofdm_subcarriers_var = tk.IntVar(value=64)

        self.noise_enabled_var = tk.BooleanVar(value=False)

        self.status_var = tk.StringVar(
            value="Ready. Select a modulation technique and generate a signal."
        )

        self.last_signal = None

        self.last_time = None

        self.last_clean_signal = None

        self.last_title = ""

        # ----------------------------------------------------
        # CONFIGURE STYLE
        # ----------------------------------------------------

        self.configure_styles()

        # ----------------------------------------------------
        # CREATE GUI
        # ----------------------------------------------------

        self.create_header()

        self.create_scrollable_area()

        self.create_control_panel()

        self.create_information_panel()

        self.create_plot_panel()

        self.create_comparison_panel()

        self.create_status_bar()

        # Generate initial AM plot
        self.root.after(300, self.generate_selected_signal)


    # ========================================================
    # STYLE CONFIGURATION
    # ========================================================

    def configure_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Blue.TCombobox",
            padding=6
        )

        style.configure(
            "Blue.Horizontal.TScale",
            background=self.COLORS["white"],
            troughcolor=self.COLORS["border"]
        )

        style.configure(
            "Treeview",
            background=self.COLORS["white"],
            foreground=self.COLORS["text"],
            rowheight=32,
            fieldbackground=self.COLORS["white"],
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=self.COLORS["primary"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

        style.map(
            "Treeview",
            background=[("selected", self.COLORS["accent"])]
        )


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.COLORS["navy"],
            height=105
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="DIGITAL MODULATION STUDIO",
            font=("Segoe UI", 25, "bold"),
            bg=self.COLORS["navy"],
            fg=self.COLORS["white"]
        )

        title.pack(
            pady=(18, 2)
        )

        subtitle = tk.Label(
            header,
            text=(
                "Interactive Generation, Visualization and Analysis "
                "of AM, FM, ASK, PSK, QAM and OFDM"
            ),
            font=("Segoe UI", 11),
            bg=self.COLORS["navy"],
            fg="#B9DCFF"
        )

        subtitle.pack()


    # ========================================================
    # SCROLLABLE MAIN AREA
    # ========================================================

    def create_scrollable_area(self):

        outer_frame = tk.Frame(
            self.root,
            bg=self.COLORS["light_blue"]
        )

        outer_frame.pack(
            fill="both",
            expand=True
        )

        self.main_canvas = tk.Canvas(
            outer_frame,
            bg=self.COLORS["light_blue"],
            highlightthickness=0
        )

        vertical_scrollbar = ttk.Scrollbar(
            outer_frame,
            orient="vertical",
            command=self.main_canvas.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            outer_frame,
            orient="horizontal",
            command=self.main_canvas.xview
        )

        self.main_canvas.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )

        horizontal_scrollbar.pack(
            side="bottom",
            fill="x"
        )

        self.main_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollable_frame = tk.Frame(
            self.main_canvas,
            bg=self.COLORS["light_blue"]
        )

        self.canvas_window = self.main_canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.scrollable_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.main_canvas.bind(
            "<Configure>",
            self.resize_canvas_frame
        )

        self.root.bind_all(
            "<MouseWheel>",
            self.mouse_wheel_scroll
        )


    def update_scroll_region(self, event=None):

        self.main_canvas.configure(
            scrollregion=self.main_canvas.bbox("all")
        )


    def resize_canvas_frame(self, event):

        required_width = max(event.width, 1150)

        self.main_canvas.itemconfigure(
            self.canvas_window,
            width=required_width
        )


    def mouse_wheel_scroll(self, event):

        self.main_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


    # ========================================================
    # REUSABLE CARD
    # ========================================================

    def create_card(self, parent, title):

        card = tk.Frame(
            parent,
            bg=self.COLORS["white"],
            highlightbackground=self.COLORS["border"],
            highlightthickness=1
        )

        title_label = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bg=self.COLORS["white"],
            fg=self.COLORS["dark_blue"],
            anchor="w"
        )

        title_label.pack(
            fill="x",
            padx=20,
            pady=(16, 10)
        )

        separator = tk.Frame(
            card,
            bg=self.COLORS["border"],
            height=1
        )

        separator.pack(
            fill="x",
            padx=20
        )

        content = tk.Frame(
            card,
            bg=self.COLORS["white"]
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        return card, content


    # ========================================================
    # CONTROL PANEL
    # ========================================================

    def create_control_panel(self):

        card, content = self.create_card(
            self.scrollable_frame,
            "Signal Configuration"
        )

        card.pack(
            fill="x",
            padx=25,
            pady=(25, 12)
        )

        # Technique selection

        tk.Label(
            content,
            text="Modulation Technique",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLORS["white"],
            fg=self.COLORS["text"]
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=8,
            pady=8
        )

        techniques = [
            "AM",
            "FM",
            "ASK",
            "BPSK",
            "QPSK",
            "16-QAM",
            "OFDM"
        ]

        modulation_box = ttk.Combobox(
            content,
            textvariable=self.modulation_var,
            values=techniques,
            state="readonly",
            width=18,
            style="Blue.TCombobox"
        )

        modulation_box.grid(
            row=1,
            column=0,
            padx=8,
            pady=4,
            sticky="ew"
        )

        modulation_box.bind(
            "<<ComboboxSelected>>",
            self.technique_changed
        )

        # Message frequency

        self.create_spin_control(
            content,
            "Message Frequency (Hz)",
            self.message_frequency_var,
            1,
            100,
            1,
            1
        )

        # Carrier frequency

        self.create_spin_control(
            content,
            "Carrier Frequency (Hz)",
            self.carrier_frequency_var,
            10,
            500,
            10,
            2
        )

        # Modulation index

        self.create_spin_control(
            content,
            "Modulation Index",
            self.modulation_index_var,
            0.1,
            5.0,
            0.1,
            3
        )

        # SNR

        self.create_spin_control(
            content,
            "SNR (dB)",
            self.snr_var,
            -10,
            50,
            1,
            4
        )

        # Number of bits

        self.create_spin_control(
            content,
            "Number of Bits",
            self.bit_count_var,
            4,
            256,
            4,
            5
        )

        # OFDM subcarriers

        self.create_spin_control(
            content,
            "OFDM Subcarriers",
            self.ofdm_subcarriers_var,
            8,
            256,
            8,
            6
        )

        # Noise checkbox

        noise_check = tk.Checkbutton(
            content,
            text="Add AWGN Noise",
            variable=self.noise_enabled_var,
            font=("Segoe UI", 10, "bold"),
            bg=self.COLORS["white"],
            fg=self.COLORS["text"],
            activebackground=self.COLORS["white"],
            selectcolor=self.COLORS["white"]
        )

        noise_check.grid(
            row=1,
            column=7,
            padx=12,
            pady=4
        )

        # Buttons

        button_frame = tk.Frame(
            content,
            bg=self.COLORS["white"]
        )

        button_frame.grid(
            row=2,
            column=0,
            columnspan=8,
            sticky="ew",
            pady=(18, 2)
        )

        self.create_button(
            button_frame,
            "Generate Signal",
            self.generate_selected_signal,
            self.COLORS["primary"]
        ).pack(
            side="left",
            padx=(0, 8)
        )

        self.create_button(
            button_frame,
            "Generate New Random Data",
            self.generate_selected_signal,
            self.COLORS["secondary"]
        ).pack(
            side="left",
            padx=8
        )

        self.create_button(
            button_frame,
            "Reset Parameters",
            self.reset_parameters,
            self.COLORS["muted"]
        ).pack(
            side="left",
            padx=8
        )

        for column in range(8):
            content.columnconfigure(
                column,
                weight=1
            )


    def create_spin_control(
        self,
        parent,
        text,
        variable,
        minimum,
        maximum,
        increment,
        column
    ):

        tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=self.COLORS["white"],
            fg=self.COLORS["text"]
        ).grid(
            row=0,
            column=column,
            sticky="w",
            padx=8,
            pady=8
        )

        spinbox = ttk.Spinbox(
            parent,
            textvariable=variable,
            from_=minimum,
            to=maximum,
            increment=increment,
            width=14
        )

        spinbox.grid(
            row=1,
            column=column,
            padx=8,
            pady=4,
            sticky="ew"
        )


    def create_button(
        self,
        parent,
        text,
        command,
        background
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=background,
            fg="white",
            activebackground=self.COLORS["accent"],
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=9
        )

        return button


    # ========================================================
    # INFORMATION PANEL
    # ========================================================

    def create_information_panel(self):

        card, content = self.create_card(
            self.scrollable_frame,
            "Technique Information"
        )

        card.pack(
            fill="x",
            padx=25,
            pady=12
        )

        self.technique_title_label = tk.Label(
            content,
            text="Amplitude Modulation (AM)",
            font=("Segoe UI", 15, "bold"),
            bg=self.COLORS["white"],
            fg=self.COLORS["primary"]
        )

        self.technique_title_label.pack(
            anchor="w"
        )

        self.technique_description_label = tk.Label(
            content,
            text="",
            font=("Segoe UI", 10),
            bg=self.COLORS["white"],
            fg=self.COLORS["text"],
            justify="left",
            anchor="w",
            wraplength=1200
        )

        self.technique_description_label.pack(
            fill="x",
            pady=(8, 0)
        )

        self.update_technique_information()


    # ========================================================
    # PLOT PANEL
    # ========================================================

    def create_plot_panel(self):

        card, content = self.create_card(
            self.scrollable_frame,
            "Interactive Signal Visualization"
        )

        card.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=12
        )

        self.figure = Figure(
            figsize=(12, 7),
            dpi=100,
            facecolor=self.COLORS["white"]
        )

        self.plot_canvas = FigureCanvasTkAgg(
            self.figure,
            master=content
        )

        self.plot_canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        toolbar_frame = tk.Frame(
            content,
            bg=self.COLORS["white"]
        )

        toolbar_frame.pack(
            fill="x"
        )

        self.toolbar = NavigationToolbar2Tk(
            self.plot_canvas,
            toolbar_frame
        )

        self.toolbar.update()


    # ========================================================
    # COMPARISON PANEL
    # ========================================================

    def create_comparison_panel(self):

        card, content = self.create_card(
            self.scrollable_frame,
            "Bandwidth Efficiency and Noise Robustness Comparison"
        )

        card.pack(
            fill="x",
            padx=25,
            pady=(12, 30)
        )

        columns = (
            "Technique",
            "Type",
            "Bits/Symbol",
            "Bandwidth Efficiency",
            "Noise Robustness",
            "Main Observation"
        )

        self.comparison_tree = ttk.Treeview(
            content,
            columns=columns,
            show="headings",
            height=7
        )

        widths = {
            "Technique": 100,
            "Type": 130,
            "Bits/Symbol": 100,
            "Bandwidth Efficiency": 170,
            "Noise Robustness": 150,
            "Main Observation": 380
        }

        for column in columns:

            self.comparison_tree.heading(
                column,
                text=column
            )

            self.comparison_tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        comparison_data = [

            (
                "AM",
                "Analog",
                "N/A",
                "Low",
                "Low",
                "Amplitude noise directly distorts the transmitted information."
            ),

            (
                "FM",
                "Analog",
                "N/A",
                "Low",
                "High",
                "Better amplitude-noise immunity but generally requires more bandwidth."
            ),

            (
                "ASK",
                "Digital",
                "1",
                "Low",
                "Low",
                "Simple implementation but strongly affected by amplitude noise."
            ),

            (
                "BPSK",
                "Digital",
                "1",
                "Moderate",
                "Very High",
                "Large constellation-point separation gives excellent noise immunity."
            ),

            (
                "QPSK",
                "Digital",
                "2",
                "High",
                "High",
                "Carries two bits per symbol with good bandwidth efficiency."
            ),

            (
                "16-QAM",
                "Digital",
                "4",
                "Very High",
                "Moderate",
                "Higher data rate but closely spaced symbols require higher SNR."
            ),

            (
                "OFDM",
                "Multi-Carrier",
                "Depends",
                "Very High",
                "High",
                "Orthogonal subcarriers provide resistance to frequency-selective fading."
            )
        ]

        for row in comparison_data:

            self.comparison_tree.insert(
                "",
                "end",
                values=row
            )

        self.comparison_tree.pack(
            fill="x"
        )


    # ========================================================
    # STATUS BAR
    # ========================================================

    def create_status_bar(self):

        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="w",
            bg=self.COLORS["dark_blue"],
            fg=self.COLORS["white"],
            font=("Segoe UI", 9),
            padx=15,
            pady=7
        )

        status_bar.pack(
            side="bottom",
            fill="x"
        )


    # ========================================================
    # TECHNIQUE INFORMATION
    # ========================================================

    def update_technique_information(self):

        technique = self.modulation_var.get()

        information = {

            "AM": (
                "Amplitude Modulation (AM)",
                "AM varies the amplitude of a high-frequency carrier according "
                "to the instantaneous amplitude of the message signal. "
                "It is simple to generate and detect, but amplitude noise can "
                "directly corrupt the transmitted information."
            ),

            "FM": (
                "Frequency Modulation (FM)",
                "FM varies the instantaneous frequency of the carrier according "
                "to the message signal while maintaining approximately constant "
                "carrier amplitude. FM provides better immunity to amplitude noise "
                "than AM but generally occupies more bandwidth."
            ),

            "ASK": (
                "Amplitude Shift Keying (ASK)",
                "ASK represents binary information using different carrier amplitudes. "
                "In the implemented on-off keying form, bit 1 is represented by the "
                "carrier and bit 0 by the absence of the carrier. ASK is simple but "
                "highly vulnerable to amplitude disturbances."
            ),

            "BPSK": (
                "Binary Phase Shift Keying (BPSK)",
                "BPSK represents binary information using two carrier phases separated "
                "by 180 degrees. Bit 1 and bit 0 are mapped to opposite signal phases. "
                "The large Euclidean distance between constellation points provides "
                "excellent noise robustness."
            ),

            "QPSK": (
                "Quadrature Phase Shift Keying (QPSK)",
                "QPSK maps pairs of bits to four phase states and therefore carries "
                "two bits per symbol. Its constellation contains four points in the "
                "in-phase and quadrature plane, providing higher bandwidth efficiency "
                "than BPSK."
            ),

            "16-QAM": (
                "16-Quadrature Amplitude Modulation",
                "16-QAM combines amplitude and phase variation using sixteen "
                "constellation points. Each symbol represents four bits. "
                "This improves spectral efficiency but requires a higher SNR because "
                "the constellation points are more closely spaced."
            ),

            "OFDM": (
                "Orthogonal Frequency Division Multiplexing (OFDM)",
                "OFDM divides a wideband channel into multiple narrowband orthogonal "
                "subcarriers. Symbols are mapped onto subcarriers and transformed into "
                "a time-domain waveform using the IFFT. OFDM provides strong resistance "
                "to frequency-selective fading and is widely used in WLAN, LTE and 5G."
            )
        }

        title, description = information[technique]

        self.technique_title_label.config(
            text=title
        )

        self.technique_description_label.config(
            text=description
        )


    def technique_changed(self, event=None):

        self.update_technique_information()

        self.status_var.set(
            f"{self.modulation_var.get()} selected. Adjust parameters and generate the signal."
        )


    # ========================================================
    # VALIDATION
    # ========================================================

    def validate_parameters(self):

        sample_rate = self.sample_rate_var.get()

        duration = self.duration_var.get()

        carrier_frequency = self.carrier_frequency_var.get()

        message_frequency = self.message_frequency_var.get()

        bit_count = self.bit_count_var.get()

        subcarriers = self.ofdm_subcarriers_var.get()

        if sample_rate <= 0:

            raise ValueError(
                "Sample rate must be greater than zero."
            )

        if duration <= 0:

            raise ValueError(
                "Duration must be greater than zero."
            )

        if carrier_frequency <= 0:

            raise ValueError(
                "Carrier frequency must be greater than zero."
            )

        if message_frequency <= 0:

            raise ValueError(
                "Message frequency must be greater than zero."
            )

        if carrier_frequency >= sample_rate / 2:

            raise ValueError(
                "Carrier frequency must be less than half of the sample rate."
            )

        if bit_count < 4:

            raise ValueError(
                "Number of bits must be at least 4."
            )

        if subcarriers < 8:

            raise ValueError(
                "OFDM requires at least 8 subcarriers."
            )


    # ========================================================
    # NOISE FUNCTION
    # ========================================================

    def add_awgn(self, signal, snr_db):

        signal_power = np.mean(np.abs(signal) ** 2)

        if signal_power == 0:

            return signal

        snr_linear = 10 ** (snr_db / 10)

        noise_power = signal_power / snr_linear

        if np.iscomplexobj(signal):

            noise = np.sqrt(noise_power / 2) * (
                np.random.randn(len(signal))
                + 1j * np.random.randn(len(signal))
            )

        else:

            noise = np.sqrt(noise_power) * np.random.randn(
                len(signal)
            )

        return signal + noise


    # ========================================================
    # MAIN GENERATION FUNCTION
    # ========================================================

    def generate_selected_signal(self):

        try:

            self.validate_parameters()

            technique = self.modulation_var.get()

            self.figure.clear()

            generators = {

                "AM": self.generate_am,

                "FM": self.generate_fm,

                "ASK": self.generate_ask,

                "BPSK": self.generate_bpsk,

                "QPSK": self.generate_qpsk,

                "16-QAM": self.generate_16qam,

                "OFDM": self.generate_ofdm
            }

            generators[technique]()

            self.figure.tight_layout(
                pad=2.5
            )

            self.plot_canvas.draw()

            self.status_var.set(
                f"{technique} signal generated successfully."
            )

            self.update_scroll_region()

        except Exception as error:

            messagebox.showerror(
                "Generation Error",
                str(error)
            )

            self.status_var.set(
                f"Error: {error}"
            )


    # ========================================================
    # AM
    # ========================================================

    def generate_am(self):

        fs = self.sample_rate_var.get()

        duration = self.duration_var.get()

        fm = self.message_frequency_var.get()

        fc = self.carrier_frequency_var.get()

        mu = self.modulation_index_var.get()

        t = np.arange(
            0,
            duration,
            1 / fs
        )

        message = np.cos(
            2 * np.pi * fm * t
        )

        carrier = np.cos(
            2 * np.pi * fc * t
        )

        modulated = (
            1 + mu * message
        ) * carrier

        clean_signal = modulated.copy()

        if self.noise_enabled_var.get():

            modulated = self.add_awgn(
                modulated,
                self.snr_var.get()
            )

        ax1 = self.figure.add_subplot(311)

        ax2 = self.figure.add_subplot(312)

        ax3 = self.figure.add_subplot(313)

        self.format_waveform_axis(
            ax1,
            t,
            message,
            "Message Signal"
        )

        self.format_waveform_axis(
            ax2,
            t,
            carrier,
            "Carrier Signal"
        )

        self.format_waveform_axis(
            ax3,
            t,
            modulated,
            "AM Modulated Signal"
        )

        self.store_signal(
            t,
            modulated,
            clean_signal,
            "AM"
        )


    # ========================================================
    # FM
    # ========================================================

    def generate_fm(self):

        fs = self.sample_rate_var.get()

        duration = self.duration_var.get()

        fm = self.message_frequency_var.get()

        fc = self.carrier_frequency_var.get()

        beta = self.modulation_index_var.get()

        t = np.arange(
            0,
            duration,
            1 / fs
        )

        message = np.cos(
            2 * np.pi * fm * t
        )

        carrier = np.cos(
            2 * np.pi * fc * t
        )

        # Correct numerical phase integration
        phase = (
            2 * np.pi * fc * t
            + 2 * np.pi
            * beta
            * fm
            * np.cumsum(message)
            / fs
        )

        modulated = np.cos(
            phase
        )

        clean_signal = modulated.copy()

        if self.noise_enabled_var.get():

            modulated = self.add_awgn(
                modulated,
                self.snr_var.get()
            )

        ax1 = self.figure.add_subplot(311)

        ax2 = self.figure.add_subplot(312)

        ax3 = self.figure.add_subplot(313)

        self.format_waveform_axis(
            ax1,
            t,
            message,
            "Message Signal"
        )

        self.format_waveform_axis(
            ax2,
            t,
            carrier,
            "Reference Carrier Signal"
        )

        self.format_waveform_axis(
            ax3,
            t,
            modulated,
            "FM Modulated Signal"
        )

        self.store_signal(
            t,
            modulated,
            clean_signal,
            "FM"
        )


    # ========================================================
    # ASK
    # ========================================================

    def generate_ask(self):

        fs = self.sample_rate_var.get()

        fc = self.carrier_frequency_var.get()

        bit_count = self.bit_count_var.get()

        samples_per_bit = 100

        bits = np.random.randint(
            0,
            2,
            bit_count
        )

        bit_stream = np.repeat(
            bits,
            samples_per_bit
        )

        t = np.arange(
            len(bit_stream)
        ) / fs

        carrier = np.cos(
            2 * np.pi * fc * t
        )

        modulated = bit_stream * carrier

        clean_signal = modulated.copy()

        if self.noise_enabled_var.get():

            modulated = self.add_awgn(
                modulated,
                self.snr_var.get()
            )

        ax1 = self.figure.add_subplot(211)

        ax2 = self.figure.add_subplot(212)

        self.format_waveform_axis(
            ax1,
            t,
            bit_stream,
            f"Binary Data: {''.join(map(str, bits))}"
        )

        self.format_waveform_axis(
            ax2,
            t,
            modulated,
            "ASK Modulated Signal"
        )

        self.store_signal(
            t,
            modulated,
            clean_signal,
            "ASK"
        )


    # ========================================================
    # BPSK
    # ========================================================

    def generate_bpsk(self):

        fs = self.sample_rate_var.get()

        fc = self.carrier_frequency_var.get()

        bit_count = self.bit_count_var.get()

        samples_per_bit = 100

        bits = np.random.randint(
            0,
            2,
            bit_count
        )

        bipolar_data = (
            2 * bits - 1
        )

        data_stream = np.repeat(
            bipolar_data,
            samples_per_bit
        )

        t = np.arange(
            len(data_stream)
        ) / fs

        carrier = np.cos(
            2 * np.pi * fc * t
        )

        modulated = data_stream * carrier

        clean_signal = modulated.copy()

        if self.noise_enabled_var.get():

            modulated = self.add_awgn(
                modulated,
                self.snr_var.get()
            )

        ax1 = self.figure.add_subplot(211)

        ax2 = self.figure.add_subplot(212)

        self.format_waveform_axis(
            ax1,
            t,
            data_stream,
            f"Bipolar Binary Data: {''.join(map(str, bits))}"
        )

        self.format_waveform_axis(
            ax2,
            t,
            modulated,
            "BPSK Modulated Signal"
        )

        self.store_signal(
            t,
            modulated,
            clean_signal,
            "BPSK"
        )


    # ========================================================
    # QPSK
    # ========================================================

    def generate_qpsk(self):

        bit_count = self.bit_count_var.get()

        if bit_count % 2 != 0:

            bit_count += 1

        bits = np.random.randint(
            0,
            2,
            bit_count
        )

        pairs = bits.reshape(
            -1,
            2
        )

        mapping = {

            (0, 0): (1, 1),

            (0, 1): (-1, 1),

            (1, 1): (-1, -1),

            (1, 0): (1, -1)
        }

        symbols = np.array(
            [
                complex(
                    *mapping[tuple(pair)]
                )

                for pair in pairs
            ],
            dtype=complex
        ) / np.sqrt(2)

        clean_symbols = symbols.copy()

        if self.noise_enabled_var.get():

            symbols = self.add_awgn(
                symbols,
                self.snr_var.get()
            )

        ax = self.figure.add_subplot(111)

        ax.scatter(
            symbols.real,
            symbols.imag,
            s=70,
            alpha=0.8
        )

        ax.axhline(
            0,
            linewidth=1
        )

        ax.axvline(
            0,
            linewidth=1
        )

        ax.set_title(
            "QPSK Constellation Diagram",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel(
            "In-Phase Component (I)"
        )

        ax.set_ylabel(
            "Quadrature Component (Q)"
        )

        ax.grid(
            True,
            alpha=0.3
        )

        ax.set_aspect(
            "equal",
            adjustable="box"
        )

        self.store_signal(
            np.arange(len(symbols)),
            symbols,
            clean_symbols,
            "QPSK"
        )


    # ========================================================
    # 16-QAM
    # ========================================================

    def generate_16qam(self):

        bit_count = self.bit_count_var.get()

        remainder = bit_count % 4

        if remainder != 0:

            bit_count += (
                4 - remainder
            )

        bits = np.random.randint(
            0,
            2,
            bit_count
        )

        groups = bits.reshape(
            -1,
            4
        )

        gray_map = {

            (0, 0): -3,

            (0, 1): -1,

            (1, 1): 1,

            (1, 0): 3
        }

        symbols = []

        for group in groups:

            i_value = gray_map[
                tuple(group[:2])
            ]

            q_value = gray_map[
                tuple(group[2:])
            ]

            symbols.append(
                complex(
                    i_value,
                    q_value
                )
            )

        symbols = np.array(
            symbols,
            dtype=complex
        ) / np.sqrt(10)

        clean_symbols = symbols.copy()

        if self.noise_enabled_var.get():

            symbols = self.add_awgn(
                symbols,
                self.snr_var.get()
            )

        ax = self.figure.add_subplot(111)

        ax.scatter(
            symbols.real,
            symbols.imag,
            s=65,
            alpha=0.8
        )

        ax.axhline(
            0,
            linewidth=1
        )

        ax.axvline(
            0,
            linewidth=1
        )

        ax.set_title(
            "16-QAM Constellation Diagram",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel(
            "In-Phase Component (I)"
        )

        ax.set_ylabel(
            "Quadrature Component (Q)"
        )

        ax.grid(
            True,
            alpha=0.3
        )

        ax.set_aspect(
            "equal",
            adjustable="box"
        )

        self.store_signal(
            np.arange(len(symbols)),
            symbols,
            clean_symbols,
            "16-QAM"
        )


    # ========================================================
    # OFDM
    # ========================================================

    def generate_ofdm(self):

        number_of_subcarriers = (
            self.ofdm_subcarriers_var.get()
        )

        # Generate QPSK symbols
        bits = np.random.randint(
            0,
            2,
            2 * number_of_subcarriers
        )

        pairs = bits.reshape(
            -1,
            2
        )

        qpsk_symbols = (
            (2 * pairs[:, 0] - 1)
            + 1j * (2 * pairs[:, 1] - 1)
        ) / np.sqrt(2)

        # Convert frequency-domain symbols
        # into time-domain OFDM waveform
        ofdm_signal = np.fft.ifft(
            qpsk_symbols
        )

        clean_signal = ofdm_signal.copy()

        if self.noise_enabled_var.get():

            ofdm_signal = self.add_awgn(
                ofdm_signal,
                self.snr_var.get()
            )

        samples = np.arange(
            number_of_subcarriers
        )

        ax1 = self.figure.add_subplot(311)

        ax2 = self.figure.add_subplot(312)

        ax3 = self.figure.add_subplot(313)

        ax1.stem(
            samples,
            np.abs(qpsk_symbols),
            basefmt=" "
        )

        ax1.set_title(
            "Frequency-Domain QPSK Subcarrier Symbols",
            fontweight="bold"
        )

        ax1.set_xlabel(
            "Subcarrier Index"
        )

        ax1.set_ylabel(
            "Magnitude"
        )

        ax1.grid(
            True,
            alpha=0.3
        )

        ax2.plot(
            samples,
            ofdm_signal.real
        )

        ax2.set_title(
            "OFDM Time-Domain Signal - Real Component",
            fontweight="bold"
        )

        ax2.set_xlabel(
            "Sample Index"
        )

        ax2.set_ylabel(
            "Amplitude"
        )

        ax2.grid(
            True,
            alpha=0.3
        )

        ax3.plot(
            samples,
            np.abs(ofdm_signal)
        )

        ax3.set_title(
            "OFDM Time-Domain Signal Magnitude",
            fontweight="bold"
        )

        ax3.set_xlabel(
            "Sample Index"
        )

        ax3.set_ylabel(
            "Magnitude"
        )

        ax3.grid(
            True,
            alpha=0.3
        )

        self.store_signal(
            samples,
            ofdm_signal,
            clean_signal,
            "OFDM"
        )


    # ========================================================
    # WAVEFORM FORMATTER
    # ========================================================

    def format_waveform_axis(
        self,
        axis,
        x_values,
        y_values,
        title
    ):

        axis.plot(
            x_values,
            y_values,
            linewidth=1.2
        )

        axis.set_title(
            title,
            fontweight="bold"
        )

        axis.set_xlabel(
            "Time (seconds)"
        )

        axis.set_ylabel(
            "Amplitude"
        )

        axis.grid(
            True,
            alpha=0.3
        )


    # ========================================================
    # STORE CURRENT SIGNAL
    # ========================================================

    def store_signal(
        self,
        time_values,
        signal,
        clean_signal,
        title
    ):

        self.last_time = time_values

        self.last_signal = signal

        self.last_clean_signal = clean_signal

        self.last_title = title


    # ========================================================
    # RESET
    # ========================================================

    def reset_parameters(self):

        self.modulation_var.set(
            "AM"
        )

        self.message_frequency_var.set(
            5.0
        )

        self.carrier_frequency_var.set(
            50.0
        )

        self.modulation_index_var.set(
            0.7
        )

        self.sample_rate_var.set(
            2000
        )

        self.duration_var.set(
            1.0
        )

        self.snr_var.set(
            20.0
        )

        self.bit_count_var.set(
            16
        )

        self.ofdm_subcarriers_var.set(
            64
        )

        self.noise_enabled_var.set(
            False
        )

        self.update_technique_information()

        self.generate_selected_signal()

        self.status_var.set(
            "Parameters reset to default values."
        )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    application = DigitalModulationStudio(
        root
    )

    root.mainloop()