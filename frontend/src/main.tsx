import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import ErrorPage, { Error404 } from "./routes/error.tsx";
import Root from "./routes/root.tsx";
import Records from "./routes/records.tsx";
import SingleRecord from "./routes/single-record.tsx";
import Home from "./routes/home.tsx";
import { ProfileLoader, RecordsLoader, SingleRecordLoader } from "./routes/loaders.ts";
import Settings from "./routes/settings.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: "records",
        element: <Records />,
        loader: RecordsLoader,
      },
      {
        path: "/records/:id",
        element: <SingleRecord />,
        loader: SingleRecordLoader,
        errorElement: <Error404 message="Record not found"/>,
      },
      {
        path: "settings",
        element: <Settings />,
        loader: ProfileLoader,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);

// https://stackoverflow.com/questions/66265608/react-router-v6-get-path-pattern-for-current-route
