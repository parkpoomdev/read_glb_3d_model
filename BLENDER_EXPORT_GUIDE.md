# Blender Export Guide: Preserving Poses in GLB/FBX

## 🎯 The Problem
When you set a pose in Blender and export to GLB/FBX, the model reverts to T-pose because export typically saves the **rest/bind pose**, not the current **posed state**.

## ✅ Solution 1: Apply Pose as Rest Pose (Destructive)

### Steps in Blender:
1. **Set your desired sitting pose**
2. **Select the armature** (bone structure)
3. **Enter Pose Mode** (`Ctrl+Tab` or select from dropdown)
4. **Select all bones** (`A`)
5. **Apply pose as rest pose**:
   - Go to `Pose > Apply > Apply Pose as Rest Pose`
   - OR press `Ctrl+A` > `Apply Pose as Rest Pose`
6. **Export GLB/FBX** - your pose will now be the default

### ⚠️ Warning:
- This permanently changes your rig's rest pose
- Make a backup before doing this
- Animation retargeting may be affected

## ✅ Solution 2: Export Animation with Pose (Recommended)

### Steps in Blender:
1. **Set your sitting pose**
2. **Create keyframes**:
   - Select all bones (`A` in Pose Mode)
   - Press `I` > `Rotation & Location`
   - This creates keyframes at frame 1
3. **Export with animation**:
   - File > Export > glTF 2.0 (.glb)
   - Check ✅ **"Animation"** in export settings
   - Check ✅ **"Export Deformation Bones Only"** (optional)
4. **In your web app**: Load and play the animation at frame 0

## ✅ Solution 3: Use Web App Pose System (Current Implementation)

### What I've Created:
- **Enhanced web interface** with pose presets
- **Programmatic sitting pose** application
- **Multiple bone controls** (hips, spine, legs, forearms)
- **Preset buttons** for instant pose changes

### Features:
- 🪑 **Sitting Pose Button** - Automatically applies realistic sitting pose
- 🕴️ **T-Pose Button** - Returns to default export pose
- 😌 **Relaxed Pose Button** - Subtle natural pose
- 🎛️ **Manual Controls** - Fine-tune any bone rotation

## 🚀 Try the New Pose System

I've created an enhanced version at: `http://localhost:3000/pose-system.html`

### What it includes:
1. **Automatic pose detection** - Finds all major bones
2. **Sitting pose preset** - Click one button to sit your character
3. **Full body control** - Hips, spine, legs, and forearms
4. **Real-time updates** - See changes immediately
5. **Reset functionality** - Return to T-pose anytime

## 📋 Bone Mapping for Sitting Pose:

```javascript
const SITTING_POSE = {
    'hips': { x: 0° },           // Neutral hip position
    'spine': { x: 10° },         // Slight forward lean
    'upper_leg.L': { x: -90° },  // Left thigh down (90° bend)
    'upper_leg.R': { x: -90° },  // Right thigh down (90° bend)  
    'lower_leg.L': { x: 90° },   // Left shin forward
    'lower_leg.R': { x: 90° }    // Right shin forward
};
```

## 🎮 Using the Pose System:

1. **Load the enhanced page**: `/pose-system.html`
2. **Click "Sitting Pose"** - Instant sitting position
3. **Adjust forearms** - Use the sliders for X, Y, Z rotation (-50° to +50°)
4. **Fine-tune** - Adjust any body part as needed
5. **Reset** - Return to T-pose anytime

This solves the export problem by applying the sitting pose programmatically in the web application, giving you full control over the character's posture!