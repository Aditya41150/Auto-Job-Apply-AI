import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useEffect, useState } from "react"
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from "recharts"

export default function Home() {
  const [appliedJobs, setAppliedJobs] = useState([])
  const [stats, setStats] = useState([])

  useEffect(() => {
    fetch("http://localhost:8000/applied")
      .then(res => res.json())
      .then(data => setAppliedJobs(data))

    fetch("http://localhost:8000/stats")
      .then(res => res.json())
      .then(data => setStats(data))
  }, [])

  return (
    <main className="p-10 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Job Auto Apply Dashboard</h1>

      <div className="grid grid-cols-3 gap-6">

        {/* Applied Jobs Count */}
        <Card className="rounded-2xl shadow-lg">
          <CardContent className="p-6">
            <h2 className="text-lg mb-2">Total Applications</h2>
            <p className="text-4xl font-bold">{appliedJobs.length}</p>
          </CardContent>
        </Card>

        {/* Bot Status */}
        <Card className="rounded-2xl shadow-lg">
          <CardContent className="p-6">
            <h2 className="text-lg mb-2">Bot Status</h2>
            <Button className="mr-3"
              onClick={() => fetch("http://localhost:8000/control/start")}>
              Start Bot
            </Button>

            <Button variant="destructive"
              onClick={() => fetch("http://localhost:8000/control/stop")}>
              Stop Bot
            </Button>
          </CardContent>
        </Card>

        {/* Logs Button */}
        <Card className="rounded-2xl shadow-lg">
          <CardContent className="p-6">
            <h2 className="text-lg mb-2">View Logs</h2>
            <Button onClick={() => window.open("https://docs.google.com/spreadsheets/u/0/", "_blank")}>
              Open Sheet
            </Button>
          </CardContent>
        </Card>

      </div>

      {/* Chart */}
      <div className="mt-10 p-6 bg-white rounded-xl shadow-md">
        <h2 className="text-xl mb-4 font-semibold">Applications Per Day</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={stats}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="count" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>

    </main>
  )
}
