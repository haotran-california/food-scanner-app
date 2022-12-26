import {useState} from 'react'
import bananaImg from './images/banana.jpg'
import orangeImg from './images/orange.jpg'
import cabbageImg from './images/cabbage.jpg'
import onionImg from './images/onion.jpg'
import './App.css'

function App() {

  const [prediction, setPrediction] = useState("")
  const [foodOpt, setFoodOpt] = useState("banana")
  const [imagePath, setImagePath] = useState(bananaImg)

  const handleChange = (e) => {
    var result = e.target.value
    setFoodOpt(result)
    if(result === "banana"){
      setImagePath(bananaImg)
    }else if(result === "orange"){
      setImagePath(orangeImg)
    }else if(result === "cabbage"){
      setImagePath(cabbageImg)
    }else{
      setImagePath(onionImg)
    }
  }

  const sendRequest = async () => {
    var url = "http://localhost:5000/predict"
    var formData = new FormData()
    var imageFile = await createFile()
    
    formData.append('file', imageFile)
  
    fetch(url, {
      method: "POST", 
      body: formData
    })
     .then(res => res.json())
     .then(data => setPrediction(data))

  }

  const createFile = async () => {
    let url = "http://localhost:3000"
    let response = await fetch(url + imagePath)
    let data = await response.blob()
    let metadata =  {type:"image/jpeg"}
    let file = new File([data], "current.jpg", metadata)
    return file
  }

  return (
    <div className="App">
      <h2>Food Scanner App (Test Project)</h2>
      <select onChange={handleChange} value={foodOpt}>
          <option value="banana">banana</option>
          <option value="orange">orange</option>
          <option value="cabbage">cabbage</option>
          <option value="onion">onion</option>
      </select>
      <div className="imageContainer">
        <img className="imageStyle" src={imagePath}/>
      </div>
      <p>Currently selected is: {foodOpt}</p>
      <p>The ML predicts this is: {prediction}</p>
      <button onClick={sendRequest}>Submit</button>
    </div>
  );
}

export default App;
