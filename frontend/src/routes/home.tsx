import { FileUpload } from "@/components/file-upload";
export default function Home() {
  return (
    <div>
      <h1 className="text-3xl font-semibold  mb-4 text-violet-900">Home</h1>
      {/* <img src="/images/logo-lg.png" className="w-1/2 md:w-1/3 lg:w-64 mb-4" /> */}
      <p className="text-lg mb-2 font-medium">Upload suitable Excel files to generate summaries</p>
      <FileUpload />
    </div>
  );
}
