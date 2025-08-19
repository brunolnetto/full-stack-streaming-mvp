import React from "react";
import type { Request } from "../../types/requests";

interface RequestListProps {
  requests: Request[];
}

const RequestList: React.FC<RequestListProps> = ({ requests }) => (
  <ul className="divide-y divide-gray-200">
    {requests.map((req, idx) => (
      <li key={idx} className="p-2">
        <span className="font-mono text-xs">{JSON.stringify(req)}</span>
      </li>
    ))}
  </ul>
);

export default RequestList; 