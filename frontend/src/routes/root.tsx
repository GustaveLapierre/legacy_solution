import { Outlet } from "react-router-dom";
import { AuthContextProvider } from "@/components/AuthContext";
import MainLayout from "@/components/main-layout";
import { Toaster } from "@/components/ui/sonner";

export default function Root() {
  return (
    <>
      <AuthContextProvider>
        <MainLayout />
        <section className="mt-12 md:mt-0 mx-6 md:mx-0 border-0 h-screen md:ml-72 md:p-4">
          <Outlet />
        </section>
      </AuthContextProvider>
      <Toaster richColors theme="light" />
    </>
  );
}
