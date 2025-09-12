import React, { useState, useMemo } from 'react';
import type { Prospect } from '@/types';
import { Card } from '@/components/UI/Card/Card';
import { formatDate } from '@/utils/utils';
import { Button } from '@/components/UI/Button/Button';

type SortConfig = {
  key: keyof Prospect;
  direction: 'ascending' | 'descending';
};

const useSortableData = (items: Prospect[], config: SortConfig | null = null) => {
  const [sortConfig, setSortConfig] = useState(config);

  const sortedItems = useMemo(() => {
    let sortableItems = [...items];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        const valA = a[sortConfig.key];
        const valB = b[sortConfig.key];
        if (valA < valB) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (valA > valB) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [items, sortConfig]);

  const requestSort = (key: keyof Prospect) => {
    let direction: 'ascending' | 'descending' = 'ascending';
    if (sortConfig && sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  return { items: sortedItems, requestSort, sortConfig };
};

export const ProspectTable: React.FC<{ prospects: Prospect[] }> = ({ prospects }) => {
  const { items, requestSort, sortConfig } = useSortableData(prospects);

  const getSortIndicator = (key: keyof Prospect) => {
    if (!sortConfig || sortConfig.key !== key) return null;
    return sortConfig.direction === 'ascending' ? ' ▲' : ' ▼';
  };

  const headers: { key: keyof Prospect; label: string }[] = [
    { key: 'name', label: 'Name' },
    { key: 'company', label: 'Company' },
    { key: 'status', label: 'Status' },
    { key: 'leadScore', label: 'Lead Score' },
    { key: 'lastActivity', label: 'Last Activity' },
  ];

  return (
    <Card padding="none">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              {headers.map(({ key, label }) => (
                <th key={key} scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  <Button variant="ghost" size="sm" onClick={() => requestSort(key)}>
                    {label} {getSortIndicator(key)}
                  </Button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            {items.map((prospect) => (
              <tr key={prospect.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{prospect.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{prospect.company}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800`}>
                    {prospect.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{prospect.leadScore}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{formatDate(prospect.lastActivity)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
};