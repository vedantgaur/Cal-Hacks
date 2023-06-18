import './App.css';
import Navbar from './Navbar';
import React, { useCallback, useState, useEffect, useRef } from 'react';
import Webcam from "react-webcam";
import AWS from 'aws-sdk';

// Configure AWS SDK
AWS.config.update({
  accessKeyId: 'YOUR_AWS_ACCESS_KEY_ID',
  secretAccessKey: 'YOUR_AWS_SECRET_ACCESS_KEY',
  region: 'YOUR_AWS_REGION',
});

const s3 = new AWS.S3();

function App() {
  const webcamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const [capturing, setCapturing] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);

  const handleDataAvailable = useCallback(
    ({ data }) => {
      if (data.size > 0) {
        setRecordedChunks((prev) => prev.concat(data));
      }
    },
    [setRecordedChunks]
  );

  const handleStartCaptureClick = useCallback(() => {
    setCapturing(true);
    mediaRecorderRef.current = new MediaRecorder(webcamRef.current.stream, {
      mimeType: "video/webm",
    });
    mediaRecorderRef.current.addEventListener(
      "dataavailable",
      handleDataAvailable
    );
    mediaRecorderRef.current.start();
  }, [webcamRef, setCapturing, mediaRecorderRef, handleDataAvailable]);

  const handleStopCaptureClick = useCallback(() => {
    mediaRecorderRef.current.stop();
    setCapturing(false);
  }, [mediaRecorderRef, setCapturing]);

  const handleUpload = useCallback(() => {
    if (recordedChunks.length) {
      const blob = new Blob(recordedChunks, {
        type: "video/webm",
      });

      // Generate a unique file name
      const fileName = `audio_${Date.now()}.webm`;

      // Specify the S3 bucket and key
      const params = {
        Bucket: 'YOUR_S3_BUCKET_NAME',
        Key: fileName,
        Body: blob,
        ACL: 'public-read', // Adjust the ACL as needed
      };

      // Upload the file to S3
      s3.upload(params, (err, data) => {
        if (err) {
          console.log(err);
        } else {
          console.log("File uploaded successfully:", data.Location);
          // Trigger your Lambda function here with the S3 file URL (data.Location)
        }
      });

      setRecordedChunks([]);
    }
  }, [recordedChunks]);

  const videoConstraints = {
    width: 420,
    height: 420,
    facingMode: "user",
  };

  const audioConstraints = {
    suppressLocalAudioPlayback: true,
    noiseSuppression: true,
    echoCancellation: true,
  };

  return (
    <div className="App">
      <Navbar />
      <div className="interview">
        <Webcam
          className="webCam"
          ref={webcamRef}
          audio={true}
          videoConstraints={videoConstraints}
          audioConstraints={audioConstraints}
          mirrored={true}
          muted={true}
        />
        <div className="buttons">
          {capturing ? (
            <button className="vidButtons" onClick={handleStopCaptureClick}>
              Stop Capture
            </button>
          ) : (
            <button className="vidButtons" onClick={handleStartCaptureClick}>
              Start Capture
            </button>
          )}
          {recordedChunks.length > 0 && (
            <button onClick={handleUpload}>Upload</button>
          )}
        </div>

        <div className="avatarBox">
          <h1>avatar box</h1>
        </div>
      </div>
    </div>
  );
}

export default App;
