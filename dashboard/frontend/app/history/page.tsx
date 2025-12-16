"use client";

import { useEffect, useState } from "react";
import axios from "axios";

export default function HistoryPage() {
  const [history, setHistory] = useState<any[]>([]);
  const API = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

  useEffect(() => {
    const load = async () => {
      const res = await axios.get(`${API}/jobs/history`);
      setHistory(res.data);
    };
    load();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Job History</h1>

      <table border={1} cellPadding={8}>
        <thead>
          <tr>
            <th>Title</th>
            <th>Company</th>
            <th>Platform</th>
            <th>Status</th>
            <th>Time</th>
          </tr>
        </thead>

        <tbody>
          {history.map((job, i) => (
            <tr key={i}>
              <td>{job.title}</td>
              <td>{job.company}</td>
              <td>{job.platform}</td>
              <td>{job.status}</td>
              <td>{job.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
