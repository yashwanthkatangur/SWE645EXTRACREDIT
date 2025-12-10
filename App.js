import React, { useState } from "react";
import axios from "axios";
import "./app.css";

function App() {
  const [city, setCity] = useState("");
  const [budget, setBudget] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      city: city,
      budget: parseFloat(budget)
    };

    try {
      const response = await axios.post("http://localhost:8000/plan-trip", payload);
      setResult(response.data);
    } catch (error) {
      console.error("Error:", error);
      alert("Backend error. Check console.");
    }
  };

  return (
    <div className="container">
      <h1>Weather Based Trip Planner</h1>

      <form onSubmit={handleSubmit}>
        <label>City</label>
        <input 
          value={city} 
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter city name"
          required 
        />

        <label>Budget</label>
        <input 
          type="number"
          value={budget}
          onChange={(e) => setBudget(e.target.value)} 
          placeholder="Enter your max budget"
          required 
        />

        <button type="submit">Plan My Trip</button>
      </form>

      {result && (
        <div className="result-box">
          <h2>Weather Summary</h2>
          <p>{result.weather_summary}</p>

          <h2>Activities</h2>
          <ul>
            {result.activities.map((act, idx) => (
              <li key={idx}>
                <strong>{act.name}</strong> — ${act.cost}
              </li>
            ))}
          </ul>

          <div className="total-cost">
            Total Cost: ${result.total_cost}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
