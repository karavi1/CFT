import React, { useState, useEffect } from "react";
import axios from "axios";

const BASE_URL = "http://18.191.202.36:8000";

function Home() {
  const [message, setMessage] = useState("");
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    axios
      .get(`${BASE_URL}/`)
      .then((res) => {
        setMessage(res.data?.message || "No message returned");
      })
      .catch((err) => {
        setError("Error fetching message: " + err.message);
      });
  }, []);

  return (
    <div className="container text-center mt-5">
      <h1 className="mb-4">🏋️‍♂️ {message}</h1>
      {error && <div className="alert alert-danger">{error}</div>}

      <p className="text-muted">Track your workouts, visualize your progress, and stay consistent.</p>

      <div className="mt-4">
        <a href="/users" className="btn btn-success me-2">
          Manage Users
        </a>
        <a href="/exercises" className="btn btn-secondary me-2">
          Manage Exercises
        </a>
        <a href="/workouts" className="btn btn-primary">
          Manage Workouts
        </a>
      </div>
    </div>
  );
}

export default Home;