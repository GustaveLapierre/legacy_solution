import { useLoaderData, useNavigate, Link } from "react-router-dom";
import type { Records as SingleRecord } from "./records";
import { Button } from "@/components/ui/button";
import { Trash2, Download } from "lucide-react";
import { toast } from "sonner";

type Entries = {
  key: string;
  general_summary: string;
  value: { summary: string; quote: string; subtitle: string; title: string }[];
}[];

type SingleRecordProps = {
  record: SingleRecord;
  entries: Entries;
};

export default function SingleRecord() {
  const { record, entries } = useLoaderData() as SingleRecordProps;
  const navigate = useNavigate();

  const handleDelete = async () => {
    const res = await fetch(`/api/delete-record/${record.id}`, {
      method: "DELETE",
    });

    if (!res.ok) {
      toast.error("Failed to delete record");
    }

    toast.success("Record deleted");
    setTimeout(() => {
      navigate("/records");
    }, 1500);
  };

  // @ts-ignore
  const handleSave = async () => {
    const res = await fetch(`/api/generate-summary/${record.id}`);

    if (!res.ok) {
      toast.error("Failed to generate summary");
    }

    toast.success("Summary generated");
    return res;
  };

  return (
    <div>
      <h1 className="text-3xl font-semibold  mb-4 text-violet-900 truncate">{record.name}</h1>
      <p className="text-slate-700 text-balance mx-4 mb-4">{record.description}</p>
      <div className="flex space-x-4 float-right">
        <Button variant={"link"} size={"icon"}>
          <Link to={`/api/generate-summary/${record.id}`} target="_blank">
            <Download className="text-violet-500" />
          </Link>
        </Button>
        <Button variant={"outline"} size={"icon"} onClick={handleDelete}>
          <Trash2 className=" text-red-500" />
        </Button>
      </div>

      <section className="lg:w-[210mm] mx-auto tracking-tight [line-height:1.35] ">
        {entries.map((entry, index) => (
          <div key={index + 1}>
            <h1 className="text-xl font-semibold mb-4 text-violet-90 indent-8">
              {index + 1}.&ensp;{entry.key}
            </h1>
            <p className="text-justify mb-8">{entry.general_summary}</p>
            <ol
              type="a"
              className="pl-12 list-inside [&>li]:[list-style-type:lower-alpha] [&>li::marker]:font-semibold [&>li]:[display:list-item]"
            >
              {entry.value.map((value, index) => (
                <li key={index} className="mt-0 mb-8">
                  <span className="font-bold">{value.subtitle}</span>
                  <p className="my-2 text-justify">{value.summary}</p>
                  <p className="my-10 italic text-justify">{value.quote}</p>
                </li>
              ))}
            </ol>
          </div>
        ))}
      </section>
    </div>
  );
}
