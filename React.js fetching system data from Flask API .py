import { useState, useEffect } from 'react';

function SystemMonitor() {
    const [data, setData] = useState(null);

    useEffect(() => {
        fetch('/api/system_status')
            .then(response => response.json())
            .then(data => setData(data));
    }, []);

    return (
        <div>
            <h2>System Monitor Dashboard</h2>
            {data ? (
                <div>
                    <p>CPU Usage: {data.cpu_usage}%</p>
                    <p>Memory Usage: {data.memory_usage}%</p>
                    <p>Disk Usage: {data.disk_usage}%</p>
                </div>
            ) : (
                <p>Loading data...</p>
            )}
        </div>
    );
}

export default SystemMonitor;
