import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [craters, setCraters] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/craters/")
      .then(response => setCraters(response.data))
      .catch(error => console.error("Error fetching craters:", error));
  }, []);

  return (
    <div>
      <h1>Impaktní krátery v Evropě</h1>
      <ul>
        {craters.map((crater) => (
          <li key={crater.id}>
            {crater.name} - Průměr: {crater.diameter} km
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;


