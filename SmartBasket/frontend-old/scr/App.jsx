
import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [status, setStatus] = useState("Connecting...");
  const [error, setError] = useState("");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/health")
      .then((response) => {
        setStatus(response.data.status);
      })
      .catch(() => {
        setError("Could not connect to SmartBasket backend.");
      });
  }, []);

  return (
    <div className="app">
      <h1>SmartBasket</h1>
      <p>Eat better. Spend less. Waste nothing.</p>

      <div className="status">
        <h2>Backend connection</h2>
        <p>{error || status}</p>
      </div>
    </div>
  );
}

export default App;
