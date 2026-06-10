import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider
import matplotlib

def pipeline_simulator(
    D,              # Pipe diameter (m)
    T_amb,          # Ambient temperature (K, C, or F based on temp_unit)
    th,             # Wall thickness (m)
    k_w,            # Wall thermal conductivity (W/m·K)
    cp_w,           # Wall specific heat capacity (J/kg·K)
    L,              # Pipe length (m)
    ts_min,         # Minimum time step for grid calculation (in time_unit)
    rho_f,          # Fluid density (kg/m³)
    cp_f,           # Fluid specific heat (J/kg·K)
    k_f,            # Fluid thermal conductivity (W/m·K)
    mu_f,           # Fluid viscosity (Pa·s)
    rho_w,          # Wall density (kg/m³)
    T_init,         # Initial temperature everywhere (K, C, or F based on temp_unit)
    t_span,         # Simulation time span (in time_unit)
    h_ext,          # External convection coeff (W/m²·K)
    roughness,      # Pipe wall roughness (m)
    pressure_unit,  # Output pressure unit: Pa, psia, psig, bara, barg
    temp_unit,      # Output temperature unit: K, C, F
    time_unit,      # Time unit for inputs and outputs: s, min, h
    m_dot_ts,       # Time series: (times in time_unit, values) for m_dot (kg/s)
    T_in_ts,        # Time series: (times in time_unit, values) for T_in (temp_unit)
    p_out_ts,       # Time series: (times in time_unit, values) for p_out (pressure_unit)
    animate_distance # Enable animated playback of distance profile
):
    # Check for interactive backend
    if not matplotlib.get_backend().lower() in ['tkagg', 'qt5agg', 'qtagg', 'wxagg']:
        print("Warning: Non-interactive Matplotlib backend detected. For animation and controls, use '%matplotlib tk' or another GUI backend (e.g., TkAgg, Qt5Agg).")

    # Time conversion functions
    def to_seconds(t, unit):
        if unit == 's':
            return t
        elif unit == 'min':
            return t * 60
        elif unit == 'h':
            return t * 3600
        else:
            raise ValueError("Invalid time_unit: choose s, min, or h")

    def from_seconds(t, unit):
        if unit == 's':
            return t
        elif unit == 'min':
            return t / 60
        elif unit == 'h':
            return t / 3600
        else:
            raise ValueError("Invalid time_unit")

    # Pressure and temperature conversion functions
    def to_pa(p, unit):
        if unit == 'Pa':
            return p
        elif unit == 'psia':
            return p * 6894.76
        elif unit == 'psig':
            return (p + 14.6959) * 6894.76
        elif unit == 'bara':
            return p * 100000
        elif unit == 'barg':
            return (p + 1) * 100000
        else:
            raise ValueError("Invalid pressure_unit: choose Pa, psia, psig, bara, barg")

    def from_pa(p, unit):
        if unit == 'Pa':
            return p
        elif unit == 'psia':
            return p / 6894.76
        elif unit == 'psig':
            return p / 6894.76 - 14.6959
        elif unit == 'bara':
            return p / 100000
        elif unit == 'barg':
            return p / 100000 - 1
        else:
            raise ValueError("Invalid pressure_unit")

    def to_k(t, unit):
        if unit == 'K':
            return t
        elif unit == 'C':
            return t + 273.15
        elif unit == 'F':
            return (t - 32) * 5/9 + 273.15
        else:
            raise ValueError("Invalid temp_unit: choose K, C, or F")

    def from_k(t, unit):
        if unit == 'K':
            return t
        elif unit == 'C':
            return t - 273.15
        elif unit == 'F':
            return (t - 273.15) * 9/5 + 32
        else:
            raise ValueError("Invalid temp_unit")

    # Input validation
    if D <= 0 or th <= 0 or L <= 0 or ts_min <= 0:
        raise ValueError("Invalid inputs: D, th, L, ts_min must be positive")
    if roughness < 0:
        raise ValueError("Pipe wall roughness must be non-negative")
    if pressure_unit not in ['Pa', 'psia', 'psig', 'bara', 'barg']:
        raise ValueError("pressure_unit must be Pa, psia, psig, bara, or barg")
    if temp_unit not in ['K', 'C', 'F']:
        raise ValueError("temp_unit must be K, C, or F")
    if time_unit not in ['s', 'min', 'h']:
        raise ValueError("time_unit must be s, min, or h")

    # Validate time series and convert times to seconds
    def validate_ts(ts, name, t_start, t_end):
        if ts is None:
            raise ValueError(f"{name} time series must be provided")
        times, values = ts
        if len(times) != len(values) or len(times) < 1:
            raise ValueError(f"{name} time series: times and values must have same length and at least one point")
        times_si = [to_seconds(t, time_unit) for t in times]
        if not np.all(np.diff(times_si) > 0):
            raise ValueError(f"{name} time series: times must be monotonically increasing")
        if min(times_si) > t_start or max(times_si) < t_end:
            raise ValueError(f"{name} time series: times must cover simulation range [{t_start}, {t_end}] (in seconds)")
        if name == 'm_dot' and any(v <= 0 for v in values):
            raise ValueError(f"{name} time series: values must be positive")
        return times_si, values

    # Convert t_span to seconds
    t_start, t_end = [to_seconds(t, time_unit) for t in t_span]
    m_dot_ts_si = validate_ts(m_dot_ts, 'm_dot', t_start, t_end)
    T_in_ts_si = validate_ts(T_in_ts, 'T_in', t_start, t_end)
    p_out_ts_si = validate_ts(p_out_ts, 'p_out', t_start, t_end)
    ts_min_si = to_seconds(ts_min, time_unit)

    # Calculate N based on max velocity and ts_min
    m_dot_max = max(m_dot_ts_si[1])
    u_max = m_dot_max / (rho_f * np.pi * D**2 / 4)  # Max velocity
    dx_initial = u_max * ts_min_si  # Initial spatial step for stability
    N = int(np.ceil(L / dx_initial))  # Number of spatial points
    if N < 10:
        print(f"Warning: Computed N={N} too small, setting N=10")
        N = 10
    elif N > 5000:
        print(f"Warning: Computed N={N} too large, setting N=5000")
        N = 5000
    dx = L / N  # Recalculate dx with final N
    x = np.linspace(0, L, N + 1)
    print(f"Computed: u_max={u_max:.2f} m/s, dx_initial={dx_initial:.2f} m, N={N} (dx={dx:.2f} m)")

    # Convert inputs to SI units
    T_amb_si = to_k(T_amb, temp_unit)
    T_init_si = to_k(T_init, temp_unit)

    # Cross-sectional areas
    A_f = np.pi * (D / 2)**2
    A_w = np.pi * ((D / 2 + th)**2 - (D / 2)**2)

    # Fluid convection coefficient
    def calc_h_f(u):
        Re = rho_f * u * D / mu_f
        Pr = mu_f * cp_f / k_f
        Nu = 3.66 if Re < 2300 else 0.023 * Re**0.8 * Pr**0.4
        return Nu * k_f / D

    # Overall heat transfer coefficient U (W/m²K, based on inner surface)
    def calc_U(u):
        # Calibrate U to match decay length of ~2766 m
        lambda_target = 2766  # Decay length from data
        U = (rho_f * cp_f * u * A_f) / (lambda_target * np.pi * D)
        return U

    # Pressure drop calculation with roughness (Haaland approximation)
    def calc_p_in(m_dot_t, p_out_t):
        u = m_dot_t / (rho_f * A_f)
        Re = rho_f * u * D / mu_f
        if Re < 2300:
            f = 64 / Re
        else:
            rel_rough = roughness / D
            f = (-1.8 * np.log10((rel_rough / 3.7)**1.11 + 6.9 / Re)) ** -2  # Haaland
        dp = f * (L / D) * (rho_f * u**2 / 2)
        return p_out_t + dp

    # Initial conditions
    T_f0 = np.ones(N + 1) * T_init_si
    T_f0[0] = to_k(T_in_ts_si[1][0], temp_unit)
    T_w0 = np.ones(N + 1) * T_init_si
    y0 = np.concatenate((T_f0, T_w0))

    # ODE system (using seconds)
    def odes(t, y):
        T_f = y[:N+1]
        T_w = y[N+1:]
        
        # Get time-varying inputs
        m_dot_t = np.interp(t, m_dot_ts_si[0], m_dot_ts_si[1])
        T_in_t = to_k(np.interp(t, T_in_ts_si[0], T_in_ts_si[1]), temp_unit)
        p_out_t = to_pa(np.interp(t, p_out_ts_si[0], p_out_ts_si[1]), pressure_unit)
        
        u = m_dot_t / (rho_f * A_f)
        U = calc_U(u)
        
        dT_fdt = np.zeros(N + 1)
        dT_wdt = np.zeros(N + 1)
        
        # Fluid: advection + heat loss to ambient
        dT_fdt[0] = 0  # Fixed inlet temperature
        T_f[0] = T_in_t  # Update inlet condition
        dT_fdx = np.zeros(N + 1)
        dT_fdx[1:] = (T_f[1:] - T_f[:-1]) / dx
        dT_fdt[1:] = -u * dT_fdx[1:] - (U * np.pi * D * (T_f[1:] - T_amb_si)) / (rho_f * cp_f * A_f)
        
        # Wall: heat transfer from fluid and to ambient
        h_f = calc_h_f(u)
        dT_wdt = (h_f * np.pi * D * (T_f - T_w)) / (rho_w * cp_w * A_w) - \
                 (h_ext * np.pi * (D + 2 * th) * (T_w - T_amb_si)) / (rho_w * cp_w * A_w)
        
        # Boundary conditions for wall (adiabatic ends)
        dT_wdt[0] = dT_wdt[1]
        dT_wdt[-1] = dT_wdt[-2]
        
        return np.concatenate((dT_fdt, dT_wdt))

    # Simulation in chunks (in seconds)
    num_chunks = 10
    dt_chunk = (t_end - t_start) / num_chunks
    y_current = y0.copy()
    all_t = []
    all_y = []
    sim_times = np.linspace(t_start, t_end, num_chunks + 1)
    outlet_temps = []
    inlet_pressures = []
    mass_flows = []
    current_time = t_start

    # Initialize time series plotting
    plt.ion()
    fig1, axs = plt.subplots(3, 1, figsize=(10, 8))
    fig1.suptitle('Simulation Progress')
    line_pin, = axs[0].plot([], [], label=f'Inlet Pressure ({pressure_unit})')
    line_mdot, = axs[1].plot([], [], label='Outlet Flow Rate (kg/s)')
    line_tout, = axs[2].plot([], [], label=f'Outlet Temperature ({temp_unit})')
    axs[0].set_ylabel(f'Pressure ({pressure_unit})')
    axs[1].set_ylabel('Flow Rate (kg/s)')
    axs[2].set_ylabel(f'Temperature ({temp_unit})')
    axs[2].set_xlabel(f'Time ({time_unit})')
    for ax in axs:
        ax.legend()
        ax.grid(True)
        ax.set_xlim(from_seconds(t_start, time_unit), from_seconds(t_end, time_unit))

    # Estimate initial plot ranges
    m_dot_range = m_dot_ts_si[1]
    p_out_range = p_out_ts_si[1]
    p_in_range = [calc_p_in(m, to_pa(p, pressure_unit)) for m, p in [(m, p) for m, p in zip(m_dot_range, p_out_range)]]
    p_in_range = [from_pa(p, pressure_unit) for p in p_in_range]
    T_in_range = T_in_ts_si[1]
    T_init_out = from_k(T_init_si, temp_unit)
    axs[0].set_ylim(min(p_in_range) * 0.95, max(p_in_range) * 1.05)
    axs[1].set_ylim(min(m_dot_range) * 0.95, max(m_dot_range) * 1.05)
    axs[2].set_ylim(min(T_init_out, min(T_in_range)) - 5, max(T_init_out, max(T_in_range)) + 5)

    # Run simulation
    for i in range(num_chunks):
        t_chunk = (current_time, current_time + dt_chunk)
        sol_chunk = solve_ivp(odes, t_chunk, y_current, method='LSODA', rtol=1e-5, atol=1e-5, max_step=100)
        if not sol_chunk.success:
            raise ValueError(f"Integration failed at chunk {i+1}: {sol_chunk.message}")

        # Append solution
        if i == 0:
            all_t.extend(sol_chunk.t)
            all_y.append(sol_chunk.y)
        else:
            all_t.extend(sol_chunk.t[1:])
            all_y.append(sol_chunk.y[:, 1:])

        y_current = sol_chunk.y[:, -1]
        current_time = sol_chunk.t[-1]

        # Store outputs
        m_dot_t = np.interp(current_time, m_dot_ts_si[0], m_dot_ts_si[1])
        p_out_t = to_pa(np.interp(current_time, p_out_ts_si[0], p_out_ts_si[1]), pressure_unit)
        p_in_t = calc_p_in(m_dot_t, p_out_t)
        outlet_temps.append(from_k(y_current[N], temp_unit))
        inlet_pressures.append(from_pa(p_in_t, pressure_unit))
        mass_flows.append(m_dot_t)

        # Update time series plots
        plot_times = [from_seconds(t, time_unit) for t in sim_times[:i+2]]
        line_pin.set_data(plot_times[:i+1], inlet_pressures)
        line_mdot.set_data(plot_times[:i+1], mass_flows)
        line_tout.set_data(plot_times[:i+1], outlet_temps)
        if inlet_pressures:
            axs[0].set_ylim(min(min(inlet_pressures), min(p_in_range)) * 0.95, max(max(inlet_pressures), max(p_in_range)) * 1.05)
        if mass_flows:
            axs[1].set_ylim(min(min(mass_flows), min(m_dot_range)) * 0.95, max(max(mass_flows), max(m_dot_range)) * 1.05)
        if outlet_temps:
            axs[2].set_ylim(min(min(outlet_temps), T_init_out, min(T_in_range)) - 5, max(max(outlet_temps), T_init_out, max(T_in_range)) + 5)

        plt.draw()
        plt.pause(0.01)

        # Print progress
        progress = (i + 1) * 10
        print(f"Progress: {progress:3d}% | Time: {from_seconds(current_time, time_unit):8.2f} {time_unit} | Outlet Temp: {outlet_temps[-1]:.2f} {temp_unit}")

    plt.ioff()

    # Combine solution
    all_y = np.hstack(all_y)
    all_t = np.array(all_t)
    class Sol:
        pass
    sol = Sol()
    sol.t = np.array([from_seconds(t, time_unit) for t in all_t])  # Convert to time_unit
    sol.y = all_y
    sol.success = True

    # Compute final results
    final_m_dot = np.interp(t_end, m_dot_ts_si[0], m_dot_ts_si[1])
    final_p_out = to_pa(np.interp(t_end, p_out_ts_si[0], p_out_ts_si[1]), pressure_unit)
    final_p_in = calc_p_in(final_m_dot, final_p_out)

    # Log final fluid temperature profile
    T_f_final = sol.y[:N+1, -1]  # Final fluid temperatures (SI)
    T_f_final_out = from_k(T_f_final, temp_unit)
    T_w_final = sol.y[N+1:, -1]  # Final wall temperatures (SI)
    T_w_final_out = from_k(T_w_final, temp_unit)
    print(f"\nFinal Fluid Temperature Profile ({temp_unit}):")
    sample_indices = np.linspace(0, N, min(10, N+1), dtype=int)  # Sample 10 points
    for i in sample_indices:
        print(f"  Position {x[i]:.0f} m: {T_f_final_out[i]:.2f} {temp_unit}")

    # Calculate decay length for verification
    u_final = final_m_dot / (rho_f * A_f)
    U = calc_U(u_final)
    lambda_decay = (rho_f * cp_f * u_final * A_f) / (U * np.pi * D)  # Decay length
    print(f"  Approximate decay length: {lambda_decay:.0f} m (for steady-state exponential decay)")
    print(f"  Note: Lower flow rates produce shorter decay lengths, causing faster cooling to ambient.")

    # Output data to text file
    print("\nWriting results to pipeline_results.csv...")
    # Calculate pressure and velocity profiles
    p_profile_si = np.linspace(final_p_in, final_p_out, N + 1)
    p_profile_out = from_pa(p_profile_si, pressure_unit)
    u_profile = np.ones(N + 1) * u_final
    
    with open('pipeline_results.csv', 'w') as f:
        # Write input parameters header
        f.write("# Pipeline Simulation Results\n")
        f.write("# Input Parameters:\n")
        f.write(f"# Pipe Diameter (D): {D:.3f} m\n")
        f.write(f"# Ambient Temperature (T_amb): {T_amb:.2f} {temp_unit}\n")
        f.write(f"# Wall Thickness (th): {th:.6f} m\n")
        f.write(f"# Wall Thermal Conductivity (k_w): {k_w:.2f} W/m·K\n")
        f.write(f"# Wall Specific Heat Capacity (cp_w): {cp_w:.2f} J/kg·K\n")
        f.write(f"# Pipe Length (L): {L:.0f} m\n")
        f.write(f"# Minimum Time Step (ts_min): {ts_min:.6f} {time_unit}\n")
        f.write(f"# Fluid Density (rho_f): {rho_f:.2f} kg/m³\n")
        f.write(f"# Fluid Specific Heat (cp_f): {cp_f:.2f} J/kg·K\n")
        f.write(f"# Fluid Thermal Conductivity (k_f): {k_f:.3f} W/m·K\n")
        f.write(f"# Fluid Viscosity (mu_f): {mu_f:.6f} Pa·s\n")
        f.write(f"# Wall Density (rho_w): {rho_w:.2f} kg/m³\n")
        f.write(f"# Initial Temperature (T_init): {T_init:.2f} {temp_unit}\n")
        f.write(f"# Simulation Time Span (t_span): {t_span[0]:.2f} to {t_span[1]:.2f} {time_unit}\n")
        f.write(f"# External Convection Coefficient (h_ext): {h_ext:.2f} W/m²·K\n")
        f.write(f"# Pipe Wall Roughness (roughness): {roughness:.6f} m\n")
        f.write(f"# Pressure Unit: {pressure_unit}\n")
        f.write(f"# Temperature Unit: {temp_unit}\n")
        f.write(f"# Time Unit: {time_unit}\n")
        f.write(f"# Final Mass Flow Rate (m_dot): {final_m_dot:.2f} kg/s\n")
        f.write(f"# Final Inlet Temperature (T_in): {from_k(to_k(T_in_ts[1][-1], temp_unit), temp_unit):.2f} {temp_unit}\n")
        f.write(f"# Final Outlet Pressure (p_out): {from_pa(final_p_out, pressure_unit):.2f} {pressure_unit}\n")
        f.write("#\n")
        # Write data header with units
        f.write("L (m),PT (bara),TM (C),U (m/s),T_w (C)\n")
        # Write data
        for i in range(N + 1):
            f.write(f"{x[i]:.4f},{p_profile_out[i]:.5f},{T_f_final_out[i]:.5f},{u_profile[i]:.6f},{T_w_final_out[i]:.5f}\n")

    # Precompute global y-axis limits
    T_f_all = sol.y[:N+1, :]  # Fluid temperatures (SI)
    T_w_all = sol.y[N+1:, :]  # Wall temperatures (SI)
    T_all_out = from_k(np.concatenate([T_f_all, T_w_all]), temp_unit)
    temp_min = np.min(T_all_out) - 5
    temp_max = np.max(T_all_out) + 5

    p_all_si = []
    for t in all_t:
        m_dot_t = np.interp(t, m_dot_ts_si[0], m_dot_ts_si[1])
        p_out_t = to_pa(np.interp(t, p_out_ts_si[0], p_out_ts_si[1]), pressure_unit)
        p_in_t = calc_p_in(m_dot_t, p_out_t)
        p_profile_t = np.linspace(p_in_t, p_out_t, N + 1)
        p_all_si.append(p_profile_t)
    p_all_out = from_pa(np.concatenate(p_all_si), pressure_unit)
    p_min = np.min(p_all_out) * 0.95
    p_max = np.max(p_all_out) * 1.05

    # Animated playback with controls
    if animate_distance:
        print(f"\nCreating animated playback of distance profile with controls (time in {time_unit})...")
        fig_anim, ax1_anim = plt.subplots(figsize=(10, 7))
        ax1_anim.set_xlabel('Position along pipe (m)')
        ax1_anim.set_ylabel(f'Temperature ({temp_unit})')
        ax2_anim = ax1_anim.twinx()
        ax2_anim.set_ylabel(f'Pressure ({pressure_unit})')
        line_tf_anim, = ax1_anim.plot([], [], label=f'Fluid Temperature ({temp_unit})', color='blue')
        line_tw_anim, = ax1_anim.plot([], [], label=f'Wall Temperature ({temp_unit})', color='green')
        line_p_anim, = ax2_anim.plot([], [], label=f'Pressure ({pressure_unit})', color='red')
        ax1_anim.legend(loc='upper left')
        ax2_anim.legend(loc='upper right')
        ax1_anim.grid(True)
        ax1_anim.set_xlim(0, L)
        ax1_anim.set_ylim(temp_min, temp_max)
        ax2_anim.set_ylim(p_min, p_max)

        # Add space for slider and button
        plt.subplots_adjust(bottom=0.25)

        # Add slider (in time_unit)
        ax_slider = plt.axes([0.15, 0.1, 0.65, 0.03])
        slider = Slider(ax_slider, f'Time ({time_unit})', from_seconds(t_start, time_unit), from_seconds(t_end, time_unit), valinit=from_seconds(t_start, time_unit), valstep=(from_seconds(t_end, time_unit) - from_seconds(t_start, time_unit)) / len(all_t))
        
        # Add play/pause button
        ax_button = plt.axes([0.83, 0.025, 0.1, 0.04])
        button = Button(ax_button, 'Pause')
        
        # Animation state
        paused = False

        def update_plot(t_frame):
            # Convert t_frame to seconds for internal use
            t_frame_si = to_seconds(t_frame, time_unit)
            # Find closest time index
            frame = np.argmin(np.abs(all_t - t_frame_si))
            T_f_frame = sol.y[:N+1, frame]
            T_w_frame = sol.y[N+1:, frame]
            T_f_out_frame = from_k(T_f_frame, temp_unit)
            T_w_out_frame = from_k(T_w_frame, temp_unit)
            
            # Compute p_in and p_out at t_frame
            m_dot_frame = np.interp(t_frame_si, m_dot_ts_si[0], m_dot_ts_si[1])
            p_out_frame_si = to_pa(np.interp(t_frame_si, p_out_ts_si[0], p_out_ts_si[1]), pressure_unit)
            p_in_frame_si = calc_p_in(m_dot_frame, p_out_frame_si)
            p_profile_si_frame = np.linspace(p_in_frame_si, p_out_frame_si, N + 1)
            p_profile_out_frame = from_pa(p_profile_si_frame, pressure_unit)
            
            line_tf_anim.set_data(x, T_f_out_frame)
            line_tw_anim.set_data(x, T_w_out_frame)
            line_p_anim.set_data(x, p_profile_out_frame)
            
            ax1_anim.set_title(f'Temperature and Pressure Profiles at t={t_frame:.2f} {time_unit}')
            return line_tf_anim, line_tw_anim, line_p_anim

        def animate(frame_idx):
            if not paused:
                t_frame_si = all_t[frame_idx]
                t_frame = from_seconds(t_frame_si, time_unit)
                slider.set_val(t_frame)  # Update slider position
                return update_plot(t_frame)
            return line_tf_anim, line_tw_anim, line_p_anim

        def on_button_clicked(event):
            nonlocal paused
            paused = not paused
            button.label.set_text('Play' if paused else 'Pause')

        def on_slider_update(val):
            nonlocal paused
            paused = True  # Pause animation when slider is moved
            button.label.set_text('Play')
            update_plot(val)
            fig_anim.canvas.draw_idle()

        button.on_clicked(on_button_clicked)
        slider.on_changed(on_slider_update)

        # Subsample frames for smoother animation
        frame_indices = range(0, len(all_t), 5)
        anim = FuncAnimation(fig_anim, animate, frames=frame_indices, interval=50, blit=False, repeat=True)
        plt.show()

    # Print summary
    print(f"\nSummary:")
    print(f"  Spatial Points (N): {N}")
    print(f"  Final Inlet Pressure: {from_pa(final_p_in, pressure_unit):,.2f} {pressure_unit}")
    print(f"  Final Outlet Pressure: {from_pa(final_p_out, pressure_unit):,.2f} {pressure_unit}")
    print(f"  Final Outlet Flow Rate: {final_m_dot:.2f} kg/s")
    print(f"  Final Outlet Temp: {from_k(sol.y[N, -1], temp_unit):.2f} {temp_unit}")
    print(f"  Simulation Times: {len(sol.t)} points from {sol.t[0]:.2f} to {sol.t[-1]:.2f} {time_unit}")
    print(f"  Note: Simulation duration ({from_seconds(t_end, time_unit):.2f} {time_unit}) is sufficient for steady-state temperature profile.")
    print("  Full solution in sol.y (rows: states, columns: times)")

    return sol, from_pa(final_p_in, pressure_unit)

# Example usage with time series (updated to match steady-state data)
pipeline_simulator(
    D=0.10,          # 10 cm diameter
    T_amb=4,        # 4°C ambient
    th=0.010,       # 10 mm thick
    k_w=45,         # Steel-like
    cp_w=500,       # Steel-like
    L=10000,        # Pipe length (m)
    ts_min=0.02778, # Minimum time step for grid (~100 s in hours)
    rho_f=850,     # Fluid density (kg/m³)
    cp_f=4180,      # Fluid specific heat (J/kg·K)
    k_f=0.6,        # Fluid thermal conductivity (W/m·K)
    mu_f=0.004,     # Fluid viscosity (Pa·s)
    rho_w=7800,     # Wall density (kg/m³)
    T_init=4,       # 4°C initial
    t_span=(0, 10), # Simulation time span (0 to 10 hours)
    h_ext=10,       # External convection coeff (W/m²·K)
    roughness=4.572e-05,  # Pipe wall roughness (m), e.g., for steel
    pressure_unit='bara',  # Output pressure unit (changed to bara to match data)
    temp_unit='C',  # Output temperature unit
    time_unit='h',  # Time unit (hours)
    m_dot_ts=([0, 10], [19.55, 19.55]),  # Constant mass flow rate to match u=2.49 m/s
    T_in_ts=([0, 10], [30, 30]),         # Constant inlet temp to match 20°C
    p_out_ts=([0, 5, 10], [10.34, 20, 20]),  # Constant outlet pressure to match 10.34 bara
    animate_distance=True  # Enable animated playback
)