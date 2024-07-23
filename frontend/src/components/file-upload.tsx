import { useCallback, useRef } from "react";
import { useDropzone } from "react-dropzone";
import { Info } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

export function FileUpload() {
  const [files, setFiles] = useState<File[]>([]);
  const [description, setDescription] = useState<string>("");
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [progress, setProgress] = useState<number>(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const onDrop = useCallback((acceptedFiles: File[]) => {
    // Do something with the files
    setFiles(acceptedFiles);
  }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const showProgress = () => {
    let current = 0;
    intervalRef.current = setInterval(() => {
      if (current >= 95) {
        clearInterval(intervalRef.current!);
        return;
      }
      current += 2.5;
      setProgress(current);
    }, 2000);
  };

  const uploadFile = async () => {
    showProgress();
    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", files[0]);
    formData.append("description", description.length > 0 ? description.slice(0, 255) : "No description");
    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const result = await response.json();
      toast.error(<p className="font-semibold">Error: {result.message}</p>);
      setIsUploading(false);
      clearInterval(intervalRef.current!);
      setProgress(0);
      return;
    }
    const result = await response.json();
    toast.success(<p className="font-semibold">Success: {result.message}</p>);
    setProgress(100);
    clearInterval(intervalRef.current!);
    setIsUploading(false);
  };

  const formatSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <section className="">
      <div
        {...getRootProps()}
        className="flex flex-col items-center justify-center h-44 border border-dashed rounded-lg"
      >
        <input {...getInputProps()} multiple={false} />
        {isDragActive ? (
          <p>Drop the files here ...</p>
        ) : (
          <>
            <p>Drag 'n' drop some files here, or click to select files</p>
            <p className="flex">
              <span className="mr-1 self-center">
                <Info className="w-4 h-4" />
              </span>
              <i className="text-sm text-slate-700">Only well formed CSV and XLSX files are allowed</i>
            </p>
          </>
        )}
      </div>

      <div className="my-4">
        <h2 className="text-lg font-semibold">Selected file</h2>
        {files.length === 0 ? (
          <p>No files selected yet</p>
        ) : (
          <div className="font-semibold text rounded-sm border w-full px-2 h-12 flex items-center justify-between">
            <p className="font-semibold truncate w-3/4">{files[0].name}</p>
            <p className="font-normal">{formatSize(files[0].size)}</p>
          </div>
        )}
        <h2 className="text-lg font-semibold my-2">Short description</h2>
        <textarea
          className="w-full border rounded-sm px-2 text-sm"
          placeholder="please provide a short description maximum of 256 characters"
          rows={5}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>
      <Progress
        value={progress}
        className={`my-4 h-2 [&>*]duration-1000 ${progress === 100 ? "[&>*]:bg-violet-500" : "[&>*]:bg-violet-500/70"}`}
      />
      <div className="my-4 flex items-center justify-center">
        <Button size={"sm"} className="w-32" onClick={uploadFile} disabled={isUploading || files.length === 0}>
          {isUploading ? "Processing..." : "Upload"}
        </Button>
      </div>
    </section>
  );
}
