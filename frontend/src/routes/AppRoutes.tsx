import { Route, Routes } from "react-router";
import { NotFoundPage } from "../pages/not-found";
import { HomePage } from "../pages/home/home";
import { AlertPage } from "@/pages/alert/alert-page";
import { GeoMapPage } from "@/pages/geo-map/geo-map";

const AppRoutes: React.FC = () => (
  <Routes>
    <Route>
      <Route index path="/home" element={<HomePage />} />
      <Route path="/log-alert" element={<AlertPage />} />
      <Route path="/geo-map" element={<GeoMapPage />} />
      <Route path="/" element={<HomePage />} />
    </Route>
    <Route path="*" element={<NotFoundPage />} />
  </Routes>
);

export default AppRoutes;
