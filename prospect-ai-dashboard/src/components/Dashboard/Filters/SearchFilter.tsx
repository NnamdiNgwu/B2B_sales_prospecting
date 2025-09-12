import React from 'react';

interface SearchFilterProps {
  value: string;
  onChange: (value: string) => void;
}

export const SearchFilter: React.FC<SearchFilterProps> = ({ value, onChange }) => {
  return (
    <div>
      <label htmlFor="search" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
        Search
      </label>
      <input
        type="text"
        id="search"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search by name, company..."
        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600"
      />
    </div>
  );
};