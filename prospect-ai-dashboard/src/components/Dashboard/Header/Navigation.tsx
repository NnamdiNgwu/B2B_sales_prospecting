import React from 'react'
import { NavLink } from 'react-router-dom'
import { Button } from '@/components/UI/Button/Button'

type Props = { onOpenImport?: () => void; onOpenSettings?: () => void }

const items = [
  { name: 'Dashboard', to: '/dashboard' },
  { name: 'Campaigns', to: '/campaigns' },
  { name: 'Analytics', to: '/analytics' },
  { name: 'Settings', to: '/settings' },
]

export const Navigation: React.FC<Props> = ({ onOpenImport, onOpenSettings }) => {
  return (
    <div className="w-full flex items-center justify-between gap-4">
      <nav className="hidden md:flex md:space-x-8 md:ml-8">
        {items.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? 'text-gray-900 dark:text-white'
                  : 'text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400'
              }`
            }
          >
            {item.name}
          </NavLink>
        ))}
      </nav>
      <div className="flex items-center gap-2">
        {onOpenImport && <Button size="sm" onClick={onOpenImport}>Import</Button>}
        {onOpenSettings && <Button size="sm" variant="outline" onClick={onOpenSettings}>Settings</Button>}
      </div>
    </div>
  )
}


// import React from 'react'
// import { Button } from '@/components/UI/Button/Button'

// type Props = {
//   onOpenImport?: () => void
//   onOpenSettings?: () => void
// }

// const navigationItems = [
//   { name: 'Dashboard', href: '#', active: true },
//   { name: 'Campaigns', href: '#', active: true },
//   { name: 'Analytics', href: '#', active: true },
//   { name: 'Settings', href: '#', active: true },
// ]

// export const Navigation: React.FC<Props> = ({ onOpenImport, onOpenSettings }) => {
//   return (
//     <div className="w-full flex items-center justify-between gap-4">
//       <nav className="hidden md:flex md:space-x-8">
//         {navigationItems.map((item) => (
//           <a
//             key={item.name}
//             href={item.href}
//             className={`px-3 py-2 text-sm font-medium transition-colors ${
//               item.active
//                 ? 'text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400'
//                 : 'text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400'
//             }`}
//           >
//             {item.name}
//           </a>
//         ))}
//       </nav>
//       <div className="flex items-center gap-2">
//         {onOpenImport && <Button size="sm" onClick={onOpenImport}>Import</Button>}
//         {onOpenSettings && <Button size="sm" variant="outline" onClick={onOpenSettings}>Settings</Button>}
//       </div>
//     </div>
//   )
// }

// import React from 'react';

// const navigationItems = [
//   { name: 'Dashboard', href: '#', active: true },
//   { name: 'Campaigns', href: '#', active: false },
//   { name: 'Analytics', href: '#', active: false },
//   { name: 'Settings', href: '#', active: false }
// ];

// export const Navigation: React.FC = () => {
//   return (
//     <nav className="hidden md:ml-8 md:flex md:space-x-8">
//       {navigationItems.map((item) => (
//         <a
//           key={item.name}
//           href={item.href}
//           className={`px-3 py-2 text-sm font-medium transition-colors ${
//             item.active
//               ? 'text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400'
//               : 'text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400'
//           }`}
//         >
//           {item.name}
//         </a>
//       ))}
//     </nav>
//   );
// };
