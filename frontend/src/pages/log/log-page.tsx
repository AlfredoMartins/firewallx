import { useState } from "react";
import { ItemLog } from "./components/item";
import instance from "@/services/api";


export type Log = {
    id: number;
    title: string;
    message: string;
    time: number;
};

const dummyData: Log[] = [

];

export const LogPage = () => {
    const [data, setData] = useState<Log[]>([...dummyData]);

    const [filters, setFilters] = useState({
        title: "",
        message: "",
        time: "",
    });
    const [pageIndex, setPageIndex] = useState(0);
    const pageSize = 3;

    const filteredData = data.filter((log) => {
        const titleMatch = log.title.toLowerCase().includes(filters.title.toLowerCase());
        const messageMatch = log.message.toLowerCase().includes(filters.message.toLowerCase());
        const timeMatch = filters.time
            ? log.time.toString().includes(filters.time)
            : true;
        return titleMatch && messageMatch && timeMatch;
    });

    const totalPages = Math.ceil(filteredData.length / pageSize);
    const validPageIndex = Math.min(Math.max(pageIndex, 0), totalPages - 1);

    const paginatedData = filteredData.slice(
        validPageIndex * pageSize,
        (validPageIndex + 1) * pageSize
    );

    const handleFilterChange = (field: keyof typeof filters, value: string) => {
        setFilters((prev) => ({
            ...prev,
            [field]: value,
        }));
        setPageIndex(0); // Reset to the first page when filters change
    };

    const handleNextPage = () => {
        if (validPageIndex < totalPages - 1) {
            setPageIndex(validPageIndex + 1);
        }
    };

    const handlePrevPage = () => {
        if (validPageIndex > 0) {
            setPageIndex(validPageIndex - 1);
        }
    };

    const handleFirstPage = () => {
        setPageIndex(0);
    };

    const handleLastPage = () => {
        setPageIndex(totalPages - 1);
    };


    const handleLogs = () => {
        instance.get('logs').then((res) => {
            setData([...res.data])
        })
    };

    return (
        <div>
            <div style={{ marginBottom: "1rem" }}>
                <label>
                    Title:{" "}
                    <input
                        type="text"
                        value={filters.title}
                        onChange={(e) => handleFilterChange("title", e.target.value)}
                        placeholder="Filter by title"
                    />
                </label>
                <label>
                    Message:{" "}
                    <input
                        type="text"
                        value={filters.message}
                        onChange={(e) => handleFilterChange("message", e.target.value)}
                        placeholder="Filter by message"
                    />
                </label>
                <label>
                    Time:{" "}
                    <input
                        type="text"
                        value={filters.time}
                        onChange={(e) => handleFilterChange("time", e.target.value)}
                        placeholder="Filter by time"
                    />
                </label>
            </div>

            <button onClick={ () => {
                handleLogs();
            } }> Load </button>

            <table>
                <thead>
                    <tr>
                        <th>Log Center</th>
                    </tr>
                </thead>
                <tbody>
                    {paginatedData.map((log) => (
                        <tr key={log.id}>
                            <td>
                                <ItemLog item={log} />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <div style={{ marginTop: "1rem" }}>
                <button onClick={handleFirstPage} disabled={validPageIndex === 0}>
                    First
                </button>
                <button onClick={handlePrevPage} disabled={validPageIndex === 0}>
                    Prev
                </button>
                <span>
                    Page {validPageIndex + 1} of {totalPages}
                </span>
                <button onClick={handleNextPage} disabled={validPageIndex === totalPages - 1}>
                    Next
                </button>
                <button onClick={handleLastPage} disabled={validPageIndex === totalPages - 1}>
                    Last
                </button>
            </div>
        </div>
    );
};