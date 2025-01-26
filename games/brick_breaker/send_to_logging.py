

    # Logging FSR events
    if fsr_value_left > FSR_THRESHOLD:
        print(f"FSR LEFT event detected: Value = {fsr_value_left}")
        handle_fsr_data(channel="LEFT", value=fsr_value_left, action="PRESS")

    if fsr_value_right > FSR_THRESHOLD:
        print(f"FSR RIGHT event detected: Value = {fsr_value_right}")
        handle_fsr_data(channel="RIGHT", value=fsr_value_right, action="PRESS")


