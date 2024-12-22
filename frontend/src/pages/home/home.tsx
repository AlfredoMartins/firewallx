import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import instance, { socket } from "@/services/api";

export const HomePage = () => {
    const [blockedIPs, setBlockedIPs] = useState<string[]>(["0.0.0.0"]);

    const socket_event = () => {
        socket.on('connect', () => {
            console.log('Connected to backend');
        });

        socket.on('new-blocked', (data) => {
            const ip = data.msg;
            console.log("data from pipe: ", data);
            addBlockedIP(ip);
        });
    };

    useEffect(() => {
        socket_event();
    }, []);
    
    const addBlockedIP = (IP: string) => {
        setBlockedIPs((prev) => [...prev, IP]);
    };

    function handleRemoveBlockedIP(ip: string) {
        instance.delete('blocked_ips/' + ip).then((res) => {
            if (res.status === 201) {
                setBlockedIPs((prev) => prev.filter(x => x !== ip));
            }
        });
    }

    return (
        <div>
            <h1>Home page</h1>
            <div className="grid grid-cols-2">
                <div className="col-span-1"></div>
                <div className="col-span-1">
                    <h1>Blocked IPs:</h1>
                    {blockedIPs.map((item, index) => (
                        <div key={index}>
                            <span>{item}</span>
                            <Button onClick={() => handleRemoveBlockedIP(item)}>Remove</Button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};
