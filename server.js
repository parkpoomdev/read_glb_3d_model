const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));
app.use('/models', express.static(path.join(__dirname)));

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/pose-system', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'pose-system.html'));
});

app.get('/debug', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'debug.html'));
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
    console.log(`📁 Serving 3D models from: ${__dirname}`);
    console.log(`🎯 Primary model: human_model_sit_possition_002.glb (with keyframe poses)`);
    console.log(`🎬 Features: Animation keyframes + manual pose control`);
    console.log(`🎮 Open browser to start animating forearms!`);
});