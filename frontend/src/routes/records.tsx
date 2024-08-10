import { Info } from "lucide-react";
import { Outlet, Link } from "react-router-dom";
import { useParams, useLoaderData } from "react-router-dom";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
export type Records = {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  created_by: string;
};

const formatDatetime = (datetime: string) => {
  return new Date(datetime).toISOString().split("T")[0] + " " ;
};

export default function Records() {
  const params = useParams<Record<string, string>>();
  const records = useLoaderData() as Records[];
  return (
    <div>
      <h1 className="text-3xl font-semibold  mb-4 text-violet-900">Records</h1>
      {records === null || records.length === 0 ? <>No records yet!</> : <RecordList records={records} />}
      <div>
        <p>{params.id}</p>
        <Outlet />
      </div>
    </div>
  );
}

function RecordList({ records }: { records: Records[] }) {
  return (
    <ul className="space-y-4">
      {records.map((record) => (
        <li key={record.id} className="border w-full rounded-md p-2 hover:shadow">
          <div className="flex justify-between">
            <h2 className="font-semibold flex hover:underline decoration-dotted decoration-violet-500 hover:text-violet-500">
              <Link to={`${record.id}`}>{record.name}</Link>
              <span className="self-center ml-2 hover:text-violet-500 transition-colors duration-300">
                {record.description && (
                  <DescriptionTooltip content={record.description}>
                    <Info className="h-4 w-4" />
                  </DescriptionTooltip>
                )}
              </span>
            </h2>
          </div>
          <div className="flex justify-between">
            <p className="text-sm text-slate-500">{record.created_by}</p>
            <p className="text-sm text-slate-500">{formatDatetime(record.created_at)}</p>
          </div>
        </li>
      ))}
    </ul>
  );
}

function DescriptionTooltip({ content, children }: { content: string; children: React.ReactNode }) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger>{children}</TooltipTrigger>
        <TooltipContent className="font-normal">
          <p>{content}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
