
import './App.css';
import Navbar from './Navbar';
import React, { useCallback, useState, useEffect, useRef } from 'react';
import Webcam from "react-webcam";

//const WebcamComponent = () => <Webcam />;

function  App() {

/* const videoRef = useRef(null)

const photoRef = useRef(null)

const getUserCamera = () =>{
  navigator.mediaDevices.getUserMedia({
    videeo:true
  })
  .then((stream) => {
    let video = videoRef.current
    
    video.srcObject = stream

    video.play()
    
  })
  .catch((error)=>{
    console.log(error)
  })

}

useEffect(() =>{
  getUserCamera()
}, [videoRef]) */


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

  const handleDownload = useCallback(() => {
    if (recordedChunks.length) {
      const blob = new Blob(recordedChunks, {
        type: "video/webm",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      document.body.appendChild(a);
      a.style = "display: none";
      a.href = url;
      a.download = "react-webcam-stream-capture.webm";
      a.click();
      window.URL.revokeObjectURL(url);
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
      <Navbar/>
      <div className = "interview">
        <Webcam className = "webCam" ref={webcamRef} audio = {true} videoConstraints={videoConstraints} audioConstraints={audioConstraints}  mirrored = {true} muted={true}/>
                <div className="buttons">
                    {capturing ? (
                      <button className = "vidButtons" onClick={handleStopCaptureClick}>Stop Capture</button>
                    ) : (
                      <button className = "vidButtons" onClick={handleStartCaptureClick}>Start Capture</button>
                    )}
                    {recordedChunks.length > 0 && (
                      <button onClick={handleDownload}>Download</button>
                    )}
                  </div>

        <div className = "avatarBox">
          <h1>avatar box</h1>
        </div>
      </div>
    </div>
  );
}

export default App;
