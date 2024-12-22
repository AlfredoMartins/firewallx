import { Globe, Home, ShieldAlert } from "lucide-react";
import logo from "@/assets/firewall-icon.png"
import { Link } from "react-router";

const items = [
    {
        title: "Home",
        url: "home",
        icon: Home,
    },
    {
        title: "Alerts",
        url: "log-alert",
        icon: ShieldAlert,
    },
    {
        title: "GeoMap",
        url: "geo-map",
        icon: Globe,
    },
];

export const TopNavMenu = () => {
    return (
        <div className="flex w-screen bg-gray-800 text-white h-[60px] items-center p-4 shadow-lg">
            <div className="flex w-1/4 justify-center items-center space-x-2">
                <img
                    src={logo}
                    alt="Logo"
                    className="h-[50px]"
                />
                <span className="text-xl font-extrabold text-gradient bg-gradient-to-r bg-clip-text">
                    FIREWALL X
                </span>
            </div>
            <div className="flex-grow">
                <div className="flex justify-center gap-8">
                    {items.map((item) => (
                        <Link
                            key={item.title}
                            to={item.url}
                            className="flex items-center gap-2 p-2 hover:bg-gray-700 active:bg-gray-600 rounded-md transition text-white "
                        >
                            <item.icon className="w-5 h-5 text-white" />
                            <span className="text-gray-400">{item.title}</span>
                        </Link>
                    ))}
                </div>
            </div>
            <div className="flex w-1/4 justify-center text-sm">
                Notifications
            </div>
        </div>
    );
};