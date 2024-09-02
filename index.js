const express = require('express');
const cors = require('cors');
const multer = require('multer');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();

app.use(cors({
    origin: 'http://localhost:5173', // React app's URL
}));

app.use(express.json());  // Middleware to parse JSON

const upload = multer({ dest: 'uploads/' });

app.post('/upload', upload.single('image'), (req, res) => {
    const imagePath = path.join(__dirname, req.file.path);

    const pythonProcess = spawn('python3', ['python_script.py', imagePath]);

    let extractedData = '';

    pythonProcess.stdout.on('data', (data) => {
        extractedData += data.toString(); // Accumulate the data
    });

    pythonProcess.stdout.on('end', () => {
        try {
        const parsedData = JSON.parse(extractedData);
        fs.unlinkSync(imagePath); // Clean up the uploaded file
        res.json(parsedData);
        } catch (error) {
        console.error(`JSON parse error: ${error.message}`);
        res.status(500).send('Error processing image');
        }
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        res.status(500).send('Error processing image');
    });
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
