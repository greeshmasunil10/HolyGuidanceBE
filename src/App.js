// import React, { useState } from "react";
// import "./App.css";

// function App() {
//   const [question, setQuestion] = useState("");
//   const [response, setResponse] = useState("");
//   const [error, setError] = useState(null);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setError(null);
//     // Fetch the response from the API endpoint
//     try {
//       const res = await fetch(`http://localhost:5000/?question=${question}`);

//       if (!res.ok) {
//         throw new Error(`Error: ${res.status}`);
//       }
//       const data = await res.json();
//       setResponse(data.response);
//     } catch (err) {
//       setError(err.message);
//     }
//   };

//   return (
//     <div className="content">
//       <h1>HOLY GUIDANCE</h1>
//       <form onSubmit={handleSubmit}>
//         <label>
//           Enter your question:
//           <input
//             type="text"
//             value={question}
//             onChange={(e) => setQuestion(e.target.value)}
//           />
//         </label>
//         <button type="submit">Submit</button>
//       </form>
//       {error && <p style={{ color: "red" }}>{error}</p>}
//       <div className="response">{response && <p>{response}</p>}</div>
//     </div>
//   );
// }

// export default App;

// import React, { useState } from "react";
// import "./App.css";

// function App() {
//   const [question, setQuestion] = useState("");
//   const [response, setResponse] = useState("");
//   const [error, setError] = useState(null);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setError(null);
//     // Fetch the response from the API endpoint
//     try {
//       const res = await fetch(`http://localhost:5000/?question=${question}`);

//       if (!res.ok) {
//         throw new Error(`Error: ${res.status}`);
//       }
//       const data = await res.json();
//       setResponse(data.response);
//     } catch (err) {
//       setError(err.message);
//     }
//   };

//   return (
//     <div className="container">
//       <form className="form" onSubmit={handleSubmit}>
//         <label>
//           Enter your question:
//           <input
//             type="text"
//             value={question}
//             onChange={(e) => setQuestion(e.target.value)}
//           />
//         </label>
//         <button type="submit">Submit</button>
//       </form>
//       {error && <p className="error">{error}</p>}
//       {response && <p>{response}</p>}
//             </div>
//           );
//         }
     
        
//         export default App;

import React, { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await fetch(`http://localhost:5000/?question=${question}`);
      if (!res.ok) {
        throw new Error(`Error: ${res.status}`);
      }
      const data = await res.json();
      setResponse(data.response);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="sample">
      <form className="form" onSubmit={handleSubmit}>
        <label className="label">
          Enter your question:
          <input
            className="input"
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
        </label>
        <button className="button" type="submit">Submit</button>
      </form>
      {error && <p className="error">{error}</p>}

        {response && (
        <div className="message-box">
          <p className="message-text">{response}</p>
        </div>
      )}

    </div>
  );
}

export default App;
