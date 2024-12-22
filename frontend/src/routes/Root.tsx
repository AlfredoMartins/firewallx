import { LogPage } from "@/pages/log/log-page";
import AppRoutes from "./AppRoutes";
import { TopNavMenu } from "./components/TopNavMenu";

export const Root = () => {
    return (
        <div className="flex flex-col w-screen h-screen items-center">
            <TopNavMenu />
            <main className="flex w-full h-full">
                <div className="flex-none w-1/5 bg-slate-300">
                    <LogPage />
                </div>
                <div className="flex-1">
                    <AppRoutes />
                </div>
            </main>
        </div>
    );
};