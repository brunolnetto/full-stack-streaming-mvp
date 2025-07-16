export default function RequestList({ requests }) {
  return (
    <ul className="divide-y divide-gray-200">
      {requests.map((req, idx) => (
        <li key={idx} className="p-2">
          <span className="font-mono text-xs">{JSON.stringify(req)}</span>
        </li>
      ))}
    </ul>
  );
} 