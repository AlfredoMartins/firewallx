import { Log } from "../log-page";

interface ItemProps {
    item: Log;
}

export const ItemLog = ({ item }: ItemProps) => {
    const { id, title, message, time } = item;

    return (
        <div className="p-6 rounded-lg hover:shadow-cyan-500/50 transition-shadow duration-300 neon-glow">
            <div className="mb-4">
                <h1 className="text-xl text-white font-extrabold">Log ID: {id}</h1>
                <p className="text-sm text-slate-100">
                    {new Date(time * 1000).toLocaleString()}
                </p>
            </div>
            <div className="mb-4">
                <h2 className="text-1xl font-semibold text-">{title}</h2>
                <p className="text-gray-400">{message}</p>
            </div>
            <button className=" text-black px-4 py-2 rounded-md focus:outline-none focus:ring-2">
                View Details
            </button>
        </div>
    );
};