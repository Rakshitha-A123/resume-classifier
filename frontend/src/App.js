import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const upload = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("/predict", formData);
      setResult(res.data);
    } catch (err) {
      alert("Error uploading file");
      console.error(err);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Resume Classifier</h1>

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          style={styles.input}
        />

        <button onClick={upload} style={styles.button}>
          Upload Resume
        </button>

        {result && (
          <div style={styles.resultBox}>
            <h2>Top Predictions</h2>

            {result.predictions.map((p, i) => (
              <div
                key={i}
                style={{
                  ...styles.resultItem,
                  backgroundColor: i === 0 ? "#d1f7c4" : "#f1f1f1"
                }}
              >
                <strong>{p.role}</strong>
                <span>{p.confidence}%</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(to right, #667eea, #764ba2)",
    fontFamily: "Arial"
  },
  card: {
    background: "#fff",
    padding: "40px",
    borderRadius: "15px",
    boxShadow: "0px 10px 30px rgba(0,0,0,0.2)",
    textAlign: "center",
    width: "350px"
  },
  title: {
    marginBottom: "20px"
  },
  input: {
    marginBottom: "20px"
  },
  button: {
    padding: "10px 20px",
    border: "none",
    backgroundColor: "#667eea",
    color: "#fff",
    borderRadius: "8px",
    cursor: "pointer",
    fontWeight: "bold"
  },
  resultBox: {
    marginTop: "20px",
    textAlign: "left"
  },
  resultItem: {
    display: "flex",
    justifyContent: "space-between",
    padding: "10px",
    borderRadius: "8px",
    marginTop: "10px"
  }
};

export default App;