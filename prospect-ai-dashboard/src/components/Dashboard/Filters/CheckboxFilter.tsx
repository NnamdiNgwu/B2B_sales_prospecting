import React from 'react';

interface CheckboxFilterProps {
  label: string;
  options: string[];
  selectedValues: string[];
  onChange: (values: string[]) => void;
}

export const CheckboxFilter: React.FC<CheckboxFilterProps> = ({ label, options, selectedValues, onChange }) => {
  const handleCheckboxChange = (option: string) => {
    const newSelection = selectedValues.includes(option)
      ? selectedValues.filter((item) => item !== option)
      : [...selectedValues, option];
    onChange(newSelection);
  };

  return (
    <div>
      <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">{label}</h4>
      <div className="mt-2 space-y-2">
        {options.map((option) => (
          <div key={option} className="flex items-center">
            <input
              id={`${label}-${option}`}
              type="checkbox"
              checked={selectedValues.includes(option)}
              onChange={() => handleCheckboxChange(option)}
              className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
            />
            <label htmlFor={`${label}-${option}`} className="ml-3 text-sm text-gray-600 dark:text-gray-400">
              {option}
            </label>
          </div>
        ))}
      </div>
    </div>
  );
};