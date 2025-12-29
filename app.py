import streamlit as st
import math
import matplotlib.pyplot as plt
import time

# ---------------- Title ----------------
st.title("Leaning Ladder Stability Tool")
st.write(
    "This tool analyzes ladder stability using equilibrium principles "
    "and provides an animated graphical simulation with force visualization."
)

# ---------------- Input Parameters ----------------
st.header("Input Parameters")

angle = st.slider("Ladder Angle (degrees)", 20, 80, 30)
length = st.number_input("Ladder Length (m)", value=5.0, min_value=1.0)
weight = st.number_input("Ladder Weight (N)", value=1500.0, min_value=1.0)
mu = st.number_input("Coefficient of Friction", value=1.0, min_value=0.0)

# ---------------- Stability Analysis ----------------
st.header("Stability Analysis")

if st.button("Generate Result"):

    theta = math.radians(angle)

    # -------- Corrected equilibrium-based friction model --------
    required_friction = (weight / 2) * (math.cos(theta) / math.sin(theta))  # W/2 * cot(theta)
    max_friction = mu * weight

    st.write(f"Required Friction Force: {required_friction:.2f} N")
    st.write(f"Maximum Available Friction: {max_friction:.2f} N")

    is_stable = required_friction <= max_friction

    if is_stable:
        st.success("The ladder is STABLE ✅")
        ladder_color = "green"
    else:
        st.error("The ladder is UNSTABLE ❌ (Ladder will fall)")
        ladder_color = "red"

    # ---------------- Animated Simulation ----------------
    st.subheader("Ladder Simulation with Forces")

    placeholder = st.empty()
    steps = 15

    # If unstable → ladder falls
    final_angle = theta if is_stable else math.radians(5)

    for i in range(1, steps + 1):

        theta_step = final_angle * i / steps

        x_top = length * math.cos(theta_step)
        y_top = length * math.sin(theta_step)

        fig, ax = plt.subplots()

        # Ladder
        ax.plot(
            [0, x_top],
            [0, y_top],
            linewidth=6,
            color=ladder_color,
            solid_capstyle="round"
        )

        # Ground & Wall
        ax.plot([-1, length + 1], [0, 0], linestyle="--", color="gray")
        ax.plot([0, 0], [0, length + 1], linestyle="--", color="gray")

        # Center of Gravity
        x_cg = x_top / 2
        y_cg = y_top / 2
        ax.scatter(x_cg, y_cg, color="black")
        ax.text(x_cg, y_cg, "  C.G.", fontsize=9)

        # Forces
        ax.arrow(x_cg, y_cg, 0, -0.8, head_width=0.08, color="red")
        ax.text(x_cg, y_cg - 1.0, "W", color="red")

        ax.arrow(0, 0, 0, 0.8, head_width=0.08, color="blue")
        ax.text(0.05, 0.9, "Ng", color="blue")

        ax.arrow(0, 0, 0.8, 0, head_width=0.08, color="purple")
        ax.text(0.9, 0.05, "F", color="purple")

        ax.arrow(x_top, y_top, -0.8, 0, head_width=0.08, color="blue")
        ax.text(x_top - 0.9, y_top + 0.05, "Nw", color="blue")

        # Formatting
        ax.set_aspect("equal")
        ax.set_xlim(-1, length + 1)
        ax.set_ylim(0, length + 1)
        ax.set_title("Leaning Ladder Simulation (With Forces)")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        placeholder.pyplot(fig)
        plt.close(fig)

        time.sleep(0.12)
