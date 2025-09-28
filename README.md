# FBX Forearm Animator

<img width="1032" height="576" alt="image" src="https://github.com/user-attachments/assets/4a463344-1548-47e6-a30b-6f7fc4f10ff9" />


A simple Node.js web application that loads the `human_model_sit_possition_001.glb` file and provides interactive controls to animate the forearm bones.

## Features

- ✅ Loads FBX model with complete rig detection
- 🎮 Interactive controls for forearm.L and forearm.R bones  
- 🔄 XYZ Euler rotation with -50° to +50° range
- 🎯 Real-time animation preview
- 🌐 Web-based interface using Three.js

## Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the server:**
   ```bash
   npm start
   ```

3. **Open browser:**
   Navigate to `http://localhost:3000`

## Controls

### Left Forearm (forearm.L)
- **Rotate X**: -50° to +50°
- **Rotate Y**: -50° to +50°  
- **Rotate Z**: -50° to +50°

### Right Forearm (forearm.R)
- **Rotate X**: -50° to +50°
- **Rotate Y**: -50° to +50°
- **Rotate Z**: -50° to +50°

### Additional Features
- **Reset Pose**: Restore all bones to default position
- **Orbit Controls**: Mouse to rotate, zoom, and pan camera
- **Real-time Updates**: Sliders update rotations immediately

## Technical Details

### Architecture
- **Backend**: Node.js + Express server
- **Frontend**: Three.js + FBXLoader
- **Model Format**: Binary FBX with rigged character
- **Bone Detection**: Automatic scanning for forearm.L and forearm.R

### File Structure
```
trial_001/
├── server.js              # Node.js server
├── package.json           # Dependencies
├── public/
│   └── index.html        # Web interface
├── human_model_sit_possition_001.glb  # Primary 3D model (with sit pose)
├── human_model_sit_possition.fbx      # Original FBX model
└── human_model_sit_possition.glb      # Alternative GLB format
```

### Dependencies
- **express**: Web server framework
- **three.js**: 3D graphics library
- **FBXLoader**: Three.js FBX file loader
- **OrbitControls**: Camera control system

## Model Information

### Detected Rig Data
- **Total Bones**: 63 joints
- **Target Bones**: forearm.L, forearm.R
- **Bone Hierarchy**: Complete humanoid skeleton
- **Animation System**: Keyframe-based with curves
- **File Size**: 562KB (FBX), 186KB (GLB)

### Bone Names Found
- head, neck, chest, spine, hips
- shoulder.L/R, upper_arm.L/R, forearm.L/R, hand.L/R
- thumb.01-03.L/R, foot.L/R
- Plus 40+ additional bones

## Usage Instructions

1. **Load the model**: The FBX file loads automatically on page load
2. **Wait for processing**: Model parsing may take a few seconds
3. **Use controls**: Adjust sliders to rotate forearms
4. **View changes**: Rotations apply in real-time
5. **Reset pose**: Click "Reset Pose" to return to default

## Browser Compatibility

✅ **Supported Browsers:**
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Troubleshooting

### Model Not Loading
- Check that `human_model_sit_possition.fbx` exists in the root directory
- Verify server is running on port 3000
- Check browser console for error messages

### Bones Not Detected
- Model may use different bone naming convention
- Check browser console for bone names found
- Modify bone detection logic in `findBones()` function

### Performance Issues
- Model is scaled down for better performance
- Reduce quality settings in renderer if needed
- Close other browser tabs for better performance

## Development

### Adding New Bones
1. Identify bone names in browser console
2. Add bone detection in `findBones()` function
3. Create new slider controls in HTML
4. Add rotation logic in `updateForearmRotation()`

### Customizing Animation
- Modify rotation ranges in HTML sliders (min/max attributes)
- Add easing/interpolation for smoother animations
- Implement preset poses or animation sequences

## License

MIT License - Feel free to modify and distribute.

---

**Created**: September 28, 2025  
**Model**: human_model_sit_possition.fbx (63 bones detected)  
**Status**: ✅ Fully functional forearm animation system
