import { useState } from 'react'
import axios from "axios";
import ArrowRight from "./assets/arrow-right.svg";
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [outputFile, setOutputFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showSubmit, setShowSubmit] = useState(false)
  const handleFileChange = (e) => {
    const imageFile = e.target.files[0]
    const imageObject = URL.createObjectURL(e.target.files[0])
    setFile({imageFile, imageObject})
    setShowSubmit(true)
  }

  const handleOnSubmit = async () => {
    let formData = new FormData();
    formData.append('file', file.imageFile)
    setShowSubmit(false)
    setLoading(true)
    try {
      const res = await axios.post(
        "/api/predict",
        formData,
        {
            headers: {
                "Content-type": "multipart/form-data",
                "Access-Control-Allow-Origin": "*"
            },
            responseType: 'blob'                  
        },
      )
      setOutputFile(res.data)
      setLoading(false)
    } catch (error) {
      console.log({error})
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <h1 className="heading">Image Enhancement</h1>
      <div className="inputWrapper">

        <label className="inputFileLabel">
          <input type="file" className="inputFile" onChange={handleFileChange} />
          Select Image File
        </label>
      </div>
      <div className="imagesDiv">
        <div className="inputImage">
          <img src={file ? file.imageObject : ""} alt="" />
        </div>
        {loading ? (
          <div className="loader-container">
            <div className="spinner"></div>
          </div>
        ) : outputFile ? (
          <div className="arrowIcon">
            <img src={ArrowRight} alt="" width={100} />
          </div>
        ) : (<></>)}
        {outputFile && (
          <div className="outputImage">
            <img src={URL.createObjectURL(outputFile)} alt="" />
          </div>
        )}
      </div>
      {showSubmit && (
        <div className="submitButtonWrapper">
          <input type="submit" className="submitButton" onClick={handleOnSubmit} value="Submit"/>
        </div>
      )}
    </div>
  )
}

export default App
