import React from 'react';

interface RangeFilterProps {
  label: string;
  min: number;
  max: number;
  value: [number, number];
  onChange: (value: [number, number]) => void;
}

export const RangeFilter: React.FC<RangeFilterProps> = ({ label, min, max, value, onChange }) => {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">{label}</label>
      <div className="flex items-center space-x-2 mt-1">
        <input
          type="range"
          min={min}
          max={max}
          value={value[1]}
          onChange={(e) => onChange([value[0], parseInt(e.target.value, 10)])}
          className="w-full"
        />
        <span className="text-sm text-gray-500 dark:text-gray-400">{value[1]}</span>
      </div>
    </div>
  );
};