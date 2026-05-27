export interface ApiError {
  detail: string | Array<{ loc: string[]; msg: string; type: string }>;
}

export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}
