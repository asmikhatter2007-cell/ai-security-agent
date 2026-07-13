import { useState } from "react";
import "./styles/dashboard.css";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import LiveFeed from "./components/LiveFeed";
import AlertPanel from "./components/AlertPanel";
import StatCards from "./components/StatCards";
import BootScreen from "./components/Bootscreen";

function App() {
  const [alerts, setAlerts] = useState([]);
  const[bootComplete,setBootComplete]=useState(false);
  const [stats, setStats] = useState({ total: 0, threats: 0, benign: 0 });
  const[threatGlow,setThreatGlow]=useState(false);

  if(!bootComplete){
    return(
      <BootScreen
      onComplete={()=>setBootComplete(true)}
      />
    )
  }
  function handleNewThreat(flow) {
    setAlerts(prev => [flow, ...prev].slice(0, 20));
    if(flow.severity==="HIGH"){
      setThreatGlow(true);
      setTimeout(()=>
      setThreatGlow(false),3000);
  }
  }
  
  function handleStatsUpdate(flow) {
    setStats(prev => ({
      total: prev.total + 1,
      threats: prev.threats + (flow.isBenign ? 0 : 1),
      benign: prev.benign + (flow.isBenign ? 1 : 0),
    }));
  }

  return (
    <div className="dashboard"
      style={{position:"relative"}}>
        <div style={{
  position: "fixed",
  inset: 0,
  pointerEvents: "none",
  zIndex: 9998,
  boxShadow: threatGlow
    ? "inset 0 0 80px rgba(239,68,68,0.45)"
    : "inset 0 0 18px rgba(239,68,68,0.25)",
  transition: "box-shadow 0.5s ease",
  borderRadius: 0,
}} />
      <Navbar />
      <div className="main-layout">
        <Sidebar />
        <LiveFeed
          onNewThreat={handleNewThreat}
          onStatsUpdate={handleStatsUpdate}
        />
        <AlertPanel alerts={alerts} />
      </div>
      <StatCards data={stats} />
    </div>
  );
}

export default App;