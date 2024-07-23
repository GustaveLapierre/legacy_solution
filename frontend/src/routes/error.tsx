import { Button } from "@/components/ui/button";
import { useRouteError, Link } from "react-router-dom";

export default function ErrorPage() {
  const error = useRouteError();
  console.error(error); //! DEBUG

  return (
    <div id="error-page">
      <h1>Oops!</h1>
      <p>An unexpected error has occurred.</p>
      {/* @ts-expect-error type of error is unknown */}
      <details>{error.statusText || error.message}</details>
      <Link to="/">Go back to the home page</Link>
    </div>
  );
}

export function Error404({ message }: { message?: string }) {
  return (
    <div className="h-full justify-center items-center flex">
      <div>
        <h1 className="font-bold text-3xl font-mono text-center">404</h1>
        <p className="text-lg text-center font-semibold">{message ? message : "Page not found"}</p>
        <div className="flex justify-center items-center">
        <Button  className="w-24" variant="link" size={"sm"} onClick={() => window.history.back()}>
          Back
        </Button>
        </div>
      </div>
    </div>
  );
}
