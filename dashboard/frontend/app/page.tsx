"use client";

import { useEffect, useState } from "react";
import axios from "axios";

interface Job {
  job_id: string;
  title: string;
  company: string;
  url: string;
  status?: string;
  date?: string;
}

export default function Dashboard() {
  const API = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";


  const [newJobs, setNewJobs] = useState<Job[]>([]);
  const [appliedJobs, setAppliedJobs] = useState<Job[]>([]);
  const [running, setRunning] = useState(false);

  // ----------------------------
  // FETCHERS
  // ----------------------------

  const fetchNewJobs = async () => {
    const res = await axios.get(`${API}/new-jobs`);
    setNewJobs(res.data);
  };

  const fetchAppliedJobs = async () => {
    const res = await axios.get(`${API}/applied`);
    setAppliedJobs(res.data);
  };

  // ----------------------------
  // RUN BOT (8.1 IMPLEMENTED)
  // ----------------------------

  const runBot = async () => {
    try {
      setRunning(true);

      // 1️⃣ Run backend bot
      await axios.post(`${API}/run-bot`);

      // 2️⃣ Refresh applied jobs immediately
      await fetchAppliedJobs();

      alert("Bot finished. Applied jobs updated.");
    } catch (err) {
      console.error(err);
      alert("Bot failed");
    } finally {
      setRunning(false);
    }
  };

  // ----------------------------
  // INITIAL LOAD
  // ----------------------------

  useEffect(() => {
    fetchNewJobs();
    fetchAppliedJobs();
  }, []);

  // ----------------------------
  // UI
  // ----------------------------

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-4xl font-bold mb-6">
        Job Auto Apply Dashboard
      </h1>

      {/* ACTION BUTTON */}
      <div className="mb-8">
        <button
          onClick={runBot}
          disabled={running}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg"
        >
          {running ? "Running..." : "Run Job Bot"}
        </button>
      </div>

      {/* NEW JOBS */}
      <h2 className="text-2xl font-semibold mb-4">
        New Jobs
      </h2>

      <div className="mb-10">
        {newJobs.length === 0 && <p>No new jobs found.</p>}

        {newJobs.map((job) => (
          <div
            key={job.job_id}
            className="border p-4 rounded-lg mb-3 bg-gray-900"
          >
            <h3 className="text-xl font-bold">{job.title}</h3>
            <p className="text-gray-300">{job.company}</p>
            <a
              href={job.url}
              target="_blank"
              className="text-blue-400 underline"
            >
              View Job
            </a>
          </div>
        ))}
      </div>

      {/* APPLIED JOBS */}
      <h2 className="text-2xl font-semibold mb-4">
        Applied Jobs
      </h2>

      <div>
        {appliedJobs.length === 0 && <p>No applied jobs yet.</p>}

        {appliedJobs.map((job) => (
          <div
            key={job.job_id}
            className="border p-4 rounded-lg mb-3 bg-gray-800"
          >
            <h3 className="text-xl font-bold">{job.title}</h3>
            <p className="text-gray-300">{job.company}</p>
            <p>Status: {job.status}</p>
            <p>Date: {job.date}</p>
            <a
              href={job.url}
              target="_blank"
              className="text-blue-400 underline"
            >
              View Job
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
