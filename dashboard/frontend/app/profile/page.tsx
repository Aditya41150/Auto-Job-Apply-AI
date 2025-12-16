"use client";

import { useState } from "react";
import axios from "axios";

export default function ProfilePage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [resume, setResume] = useState<File | null>(null);

  const API = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

  const saveProfile = async () => {
    try {
      await axios.post(`${API}/profile/update`, {
        name,
        email,
        phone,
      });
      alert("Profile Saved");
    } catch (err) {
      alert("Failed to save");
      console.error(err);
    }
  };

  const uploadResume = async () => {
    if (!resume) return alert("Choose a file");

    try {
      const form = new FormData();
      form.append("file", resume);

      await axios.post(`${API}/profile/upload_resume`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      alert("Resume Uploaded");
    } catch (err) {
      alert("Failed to upload");
      console.error(err);
    }
  };

  return (
    <div style={{ padding: "30px", maxWidth: "600px", margin: "auto" }}>
      <h1 style={{ fontSize: "32px", marginBottom: "20px" }}>Profile</h1>

      {/* Name */}
      <div style={{ marginBottom: "20px" }}>
        <label>Name</label><br />
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "5px",
            borderRadius: "6px",
            border: "1px solid #444",
            background: "#111",
            color: "white"
          }}
        />
      </div>

      {/* Email */}
      <div style={{ marginBottom: "20px" }}>
        <label>Email</label><br />
        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "5px",
            borderRadius: "6px",
            border: "1px solid #444",
            background: "#111",
            color: "white"
          }}
        />
      </div>

      {/* Phone */}
      <div style={{ marginBottom: "20px" }}>
        <label>Phone</label><br />
        <input
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "5px",
            borderRadius: "6px",
            border: "1px solid #444",
            background: "#111",
            color: "white"
          }}
        />
      </div>

      <button
        onClick={saveProfile}
        style={{
          padding: "10px 20px",
          background: "#1a73e8",
          border: "none",
          borderRadius: "6px",
          color: "white",
          cursor: "pointer",
          marginBottom: "30px"
        }}
      >
        Save
      </button>

      <hr style={{ margin: "30px 0", borderColor: "#444" }} />

      {/* Resume Upload */}
      <div style={{ marginBottom: "20px" }}>
        <label>Upload Resume (PDF)</label><br />
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setResume(e.target.files?.[0] || null)}
          style={{ marginTop: "10px" }}
        />
      </div>

      <button
        onClick={uploadResume}
        style={{
          padding: "10px 20px",
          background: "#34a853",
          border: "none",
          borderRadius: "6px",
          color: "white",
          cursor: "pointer"
        }}
      >
        Upload Resume
      </button>
    </div>
  );
}
