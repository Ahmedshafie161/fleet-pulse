# FleetPulse Demo GIFs

Place your recorded GIF files in this directory. The README expects the following files:

- `overview.gif` - Dashboard overview and features
- `registration.gif` - User registration flow
- `login.gif` - User login and authentication
- `vehicles.gif` - Vehicle management (add, list, edit)
- `driver.gif` - Driver management
- `trip.gif` - Trip creation and tracking
- `alert.gif` - Alert creation and monitoring
- `telemetry.gif` - Telemetry data posting and querying
- `maintenance.gif` - Maintenance scheduling
- `config.gif` - Fleet configuration settings

## How to Create GIFs:

1. **Record**: Use DU Recorder Mac, Gyroflow Toolbox, or ScreenFlow to record screen interactions
2. **Convert**: Use ezgif.com, Giphy, or FFmpeg to convert MP4 → GIF
3. **Optimize**: Reduce file size (aim for <5MB per GIF for GitHub)
4. **Place**: Add .gif files to this directory

## Tools:
- macOS Screen Recording: Use built-in Screenshot app or third-party recorders
- Conversion: `ffmpeg -i video.mp4 -vf "scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif`
- Optimization: https://ezgif.com/ or ImageOptim
