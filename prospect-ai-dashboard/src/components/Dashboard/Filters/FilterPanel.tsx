import React from 'react';
import type { FilterOptions, Prospect } from '@/types';
import { Card } from '@/components/UI/Card/Card';
import { Button } from '@/components/UI/Button/Button';
import { SearchFilter } from './SearchFilter';
import { CheckboxFilter } from './CheckboxFilter';
import { RangeFilter } from './RangeFilter';
import { INDUSTRIES, COMPANY_SIZES } from '@/constants/dashboard';

interface FilterPanelProps {
  filters: FilterOptions;
  onFiltersChange: (filters: FilterOptions) => void;
  prospects: Prospect[];
}

export const FilterPanel: React.FC<FilterPanelProps> = ({ 
  filters, 
  onFiltersChange, 
  prospects 
}) => {
  const locations = [...new Set(prospects.map(p => p.location))].filter(Boolean);
  const statuses = ['new', 'contacted', 'responded', 'qualified', 'converted', 'rejected'];
  const allTags = [...new Set(prospects.flatMap(p => p.tags))].filter(Boolean);

  const updateFilter = (key: keyof FilterOptions, value: any) => {
    onFiltersChange({ ...filters, [key]: value });
  };

  const clearFilters = () => {
    onFiltersChange({
      search: '',
      industry: [],
      companySize: [],
      leadScore: [0, 100],
      status: [],
      location: [],
      tags: []
    });
  };

  return (
    <div className="px-6 py-4 bg-gray-50 dark:bg-gray-700 border-t border-gray-200 dark:border-gray-600">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <div className="col-span-1 md:col-span-2">
          <SearchFilter
            value={filters.search}
            onChange={(value) => updateFilter('search', value)}
          />
        </div>

        <CheckboxFilter
          label="Industry"
          options={INDUSTRIES}
          selectedValues={filters.industry}
          onChange={(values) => updateFilter('industry', values)}
        />

        <CheckboxFilter
          label="Company Size"
          options={COMPANY_SIZES}
          selectedValues={filters.companySize}
          onChange={(values) => updateFilter('companySize', values)}
        />

        <CheckboxFilter
          label="Status"
          options={statuses}
          selectedValues={filters.status}
          onChange={(values) => updateFilter('status', values)}
        />

        <RangeFilter
          label="Lead Score"
          min={0}
          max={100}
          value={filters.leadScore}
          onChange={(value) => updateFilter('leadScore', value)}
        />
      </div>

      <div className="mt-4 flex justify-end">
        <Button variant="outline" onClick={clearFilters}>
          Clear Filters
        </Button>
      </div>
    </div>
  );
};