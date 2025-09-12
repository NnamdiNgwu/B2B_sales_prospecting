
import React from 'react';

const navigationItems = [
  { name: 'Dashboard', href: '#', active: true },
  { name: 'Campaigns', href: '#', active: false },
  { name: 'Analytics', href: '#', active: false },
  { name: 'Settings', href: '#', active: false }
];

export const Navigation: React.FC = () => {
  return (
    <nav className="hidden md:ml-8 md:flex md:space-x-8">
      {navigationItems.map((item) => (
        <a
          key={item.name}
          href={item.href}
          className={`px-3 py-2 text-sm font-medium transition-colors ${
            item.active
              ? 'text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400'
              : 'text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400'
          }`}
        >
          {item.name}
        </a>
      ))}
    </nav>
  );
};