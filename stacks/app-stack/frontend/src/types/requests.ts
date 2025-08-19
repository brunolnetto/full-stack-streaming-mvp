export interface Request {
  id?: string;
  timestamp?: string;
  method?: string;
  path?: string;
  status?: number;
  [key: string]: any; // Allow for additional dynamic fields
} 