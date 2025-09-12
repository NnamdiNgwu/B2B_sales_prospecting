import { useState } from 'react';

// export const useErrorHandler = () => {
//   const [error, setError] = useState<string | null>(null);
//   const handleError = (msg: string) => setError(msg);
//   const clearError = () => setError(null);
//   return { error, handleError, clearError };
// };


export const getErrorMessage = (error: unknown): string => {
  if (error instanceof Error) {
    return error.message;
  }
  if (typeof error === 'string') {
    return error;
  }
  return 'An unknown error occurred.';
};