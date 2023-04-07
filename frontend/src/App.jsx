import React, { useState, useRef } from "react";
import axios from "axios";
import ArrowRight from "./assets/arrow-right.svg";
import FileUpload from "./assets/file-upload.svg";
import ResetIcon from "./assets/reset-icon.svg";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [outputFile, setOutputFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showSubmit, setShowSubmit] = useState(false);
  const [OCRText, setOCRText] = useState("");
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const handleDrag = function (e) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = function (e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setOutputFile(null);
      setOCRText("");
      const imageFile = e.dataTransfer.files[0];
      const imageObject = URL.createObjectURL(e.dataTransfer.files[0]);
      setFile({ imageFile, imageObject });
      setShowSubmit(true);
    }
  };

  const handleChange = function (e) {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      setOutputFile(null);
      setOCRText("");
      const imageFile = e.target.files[0];
      const imageObject = URL.createObjectURL(e.target.files[0]);
      setFile({ imageFile, imageObject });
      setShowSubmit(true);
    }
  };

  const onButtonClick = () => {
    inputRef.current.click();
  };

  const handleOnSubmit = async () => {
    let formData = new FormData();
    formData.append("file", file.imageFile);
    setLoading(true);
    try {
      const res = await axios.post("/api/predict", formData, {
        headers: {
          "Content-type": "multipart/form-data",
          "Access-Control-Allow-Origin": "*",
        },
        responseType: "blob",
      });
      setOutputFile(res.data);
      setShowSubmit(false);
      await fetchOCR();
      setLoading(false);
    } catch (error) {
      console.log({ error });
      setLoading(false);
    }
  };

  const fetchOCR = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`/api/predict?fileName=${file.imageFile.name.split(".")[0]}`);
      setOCRText(await res.data.text);
    } catch (error) {
      console.log({ error });
      setLoading(false);
    }
  };

  const reset = () => {
    setFile(null);
    setOutputFile(null);
    setOCRText("");
    setShowSubmit(false)
    setLoading(false)
    setDragActive(false)
  };

  return (
    <div className="App">
      {loading && (
        <div className="loader-container">
          <div className="spinner"></div>
        </div>
      )}
      <h1 className="heading" onClick={reset}>
        Image Enhancement
        {outputFile && (
          <img className="resetIcon" src={ResetIcon} alt="" width={30} height={30} />
        )}
      </h1>
      {!outputFile && (
        <form className="form-file-upload" onDragEnter={handleDrag} onSubmit={(e) => e.preventDefault()}>
          <input ref={inputRef} type="file" className="input-file-upload" multiple={false} onChange={handleChange} />
          <label htmlFor="input-file-upload" className="label-file-upload">
            <div className="drag-area-wrapper">
              <p className="heading-file-upload">Upload your images</p>
              <p className="sub-heading-file-upload">PNG and JPG files are allowed</p>
              <button className="upload-button sub-heading-file-upload" onClick={onButtonClick}>
                <div>
                  <img src={FileUpload} alt="" width={90} height={75} />
                </div>
                <p>Drag and drop or browse to choose a file</p>
              </button>
            </div>
          </label>
          {dragActive && (
            <div
              className="drag-file-element"
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            ></div>
          )}
        </form>
      )}
      {showSubmit && (
        <div className="submitButtonWrapper">
          <input type="submit" className="submitButton" onClick={handleOnSubmit} value="Submit" />
          <p className="previewText">Image Preview:</p>
        </div>
      )}
      <div className="imagesWrapper">
        <div className="imagesDiv">
          {file && (
            <div className="inputImage">
              <img src={file.imageObject} alt="" width={504} height={400} />
            </div>
          )}
          {outputFile ? (
            <div className="arrowIcon">
              <img src={ArrowRight} alt="" width={100} />
            </div>
          ) : (
            <></>
          )}
          {outputFile && (
            <div className="outputImage">
              <img src={URL.createObjectURL(outputFile)} alt="" width={504} height={400} />
            </div>
          )}
        </div>
      </div>
      {OCRText && (
        <div className="OCRDiv">
          <p className="OCRText">Text Detected: {OCRText}</p>
        </div>
      )}
    </div>
  );
}

export default App;

