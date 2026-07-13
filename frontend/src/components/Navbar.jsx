import { Shield, Wifi } from "lucide-react";
import { useEffect, useState } from "react";

function Navbar(){

    const [time,setTime]=useState("");

    useEffect(()=>{

        const timer=setInterval(()=>{

            setTime(new Date().toLocaleTimeString());

        },1000);

        return ()=>clearInterval(timer);

    },[]);

    return(

        <nav className="navbar">

            <div className="logo">

                <Shield size={34}/>

                <div>

                    <h2>AI Security Agent</h2>

                    <p>Real-Time Threat Monitoring</p>

                </div>

            </div>

            <div className="navbar-right">

                <div className="live">

                    <Wifi size={18}/>

                    LIVE

                </div>

                <div className="clock">

                    {time}

                </div>

            </div>

        </nav>

    );

}

export default Navbar;