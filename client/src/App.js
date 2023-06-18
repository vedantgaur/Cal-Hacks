import './App.css';
import Navbar from './Navbar';
import React, { useCallback, useState, useEffect, useRef } from 'react';
import Webcam from "react-webcam";
import { motion } from "framer-motion"




// import AWS from 'aws-sdk';

// // Configure AWS SDK
// AWS.config.update({
//   accessKeyId: 'YOUR_AWS_ACCESS_KEY_ID',
//   secretAccessKey: 'YOUR_AWS_SECRET_ACCESS_KEY',
//   region: 'YOUR_AWS_REGION',
// });

// const s3 = new AWS.S3();

function App() {
  const webcamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const [capturing, setCapturing] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const [scale, setScale] = useState(1);
  const [translateXLeft, setTranslateXLeft] = useState(0);
  const [translateYLeft, setTranslateYLeft] = useState(0);
  const [translateXRight, setTranslateXRight] = useState(0);
  const [translateYRight, setTranslateYRight] = useState(0);
  const [text, setText] = useState('');
  const [textOpacity, setTextOpacity] = useState(0);


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

    setScale(0.7)
    setTranslateXLeft(-150)
    setTranslateYLeft(-70 )
    setTranslateXRight(-873)
    setTranslateYRight(240)
    setTextOpacity(1)
  }, [webcamRef, setCapturing, mediaRecorderRef, handleDataAvailable]);

  const handleStopCaptureClick = useCallback(() => {
    mediaRecorderRef.current.stop();
    setCapturing(false);

    setScale(1)
    setTranslateYRight(0)
    setTranslateYLeft(0)
    setTranslateXRight(0)
    setTranslateXLeft(0)
    setTextOpacity(0)
  }, [mediaRecorderRef, setCapturing]);

  // const handleUpload = useCallback(() => {
  //   if (recordedChunks.length) {
  //     const blob = new Blob(recordedChunks, {
  //       type: "video/webm",
  //     });

  //     // Generate a unique file name
  //     const fileName = `audio_${Date.now()}.webm`;

  //     // Specify the S3 bucket and key
  //     const params = {
  //       Bucket: 'YOUR_S3_BUCKET_NAME',
  //       Key: fileName,
  //       Body: blob,
  //       ACL: 'public-read', // Adjust the ACL as needed
  //     };

  //     // Upload the file to S3
  //     s3.upload(params, (err, data) => {
  //       if (err) {
  //         console.log(err);
  //       } else {
  //         console.log("File uploaded successfully:", data.Location);
  //         // Trigger your Lambda function here with the S3 file URL (data.Location)
  //       }
  //     });

  //     setRecordedChunks([]);
  //   }
  // }, [recordedChunks]);

  const handleInputChange = (event) => {
    setText(event.target.value);
  };

  const videoConstraints = {
    width: 500,
    height: 420,
    facingMode: "user",
  };

  const audioConstraints = {
    suppressLocalAudioPlayback: true,
    noiseSuppression: true,
    echoCancellation: true,
  };




  return (
    <div className='App'>
      <div className='navbar bg-gradient-to-r from-cyan-400 to-blue-400 text-primary-content'>
        <a className="btn btn-ghost normal-case text-xl bg-black">Prosody</a>
      </div>
      <br />
      <div className='flex justify-around'>
        <div>
          <motion.div
            initial={{ scale : 1}}
            animate={{ scale : scale,  translateX: translateXLeft, translateY: translateYLeft}}
            transition={{ duration: 1}}
          >
          <Webcam
            className="webCam"
            ref={webcamRef}
            audio={true}
            videoConstraints={videoConstraints}
            audioConstraints={audioConstraints}
            mirrored={true}
            muted={true}
          />
          </motion.div>
        </div>

        <div>
          <motion.div
              initial={{ scale : 1}}
              animate={{ scale : scale,  translateX: translateXRight, translateY: translateYRight}}
              transition={{ duration: 1}}
            >
          <div className="avatarBox">
              <h1>avatar box</h1>
          </div>
          </motion.div>
        </div>
      </div>
        <div className="buttons">
          {capturing ? (
            <button className="vidButtons btn w-40 hover:bg-gradient-to-r from-pink-400 to-red-400" onClick={handleStopCaptureClick}>
              End Interview
            </button>
          ) : (
            <button className="vidButtons btn w-40 hover:bg-gradient-to-r from-cyan-400 to-blue-400" onClick={handleStartCaptureClick}>
              Begin Interview
            </button>
          )}
          {/* {recordedChunks.length > 0 && (
            <button onClick={handleUpload}>Upload</button>
          )} */}
        </div>


        <motion.div 
        initial = {{ opacity: 0, x: 840, y: -375}}
        animate = {{ opacity: textOpacity }}
        transition={{ duration: 1}}>
          <input type="text" className="input input-bordered input-md w-2/5 h-96" value={text} onChange={handleInputChange} />
        </motion.div>

      </div>
      
  );
}

export default App;
