const { desktopCapturer } = require('electron');
const Tesseract = require('tesseract.js');

// Capture screenshot
desktopCapturer.getSources({ types: ['screen'] }).then(async sources => {
    for (const source of sources) {
        if (source.name === 'Entire Screen') {
            const screenshot = await captureScreen(source);
            // Extract text from screenshot
            Tesseract.recognize(
                screenshot,
                'eng',
                {
                    logger: m => console.log(m)
                }
            ).then(({ data: { text } }) => {
                console.log(text);
                // Translate or define text here
            });
        }
    }
});

async function captureScreen(source) {
    const stream = await navigator.mediaDevices.getUserMedia({
        audio: false,
        video: {
            mandatory: {
                chromeMediaSource: 'desktop',
                chromeMediaSourceId: source.id,
                minWidth: 1280,
                maxWidth: 1280,
                minHeight: 720,
                maxHeight: 720
            }
        }
    });
    const video = document.createElement('video');
    video.srcObject = stream;
    video.play();
    return new Promise((resolve) => {
        video.onloadedmetadata = () => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            stream.getTracks()[0].stop();
            resolve(canvas.toDataURL());
        };
    });
}
