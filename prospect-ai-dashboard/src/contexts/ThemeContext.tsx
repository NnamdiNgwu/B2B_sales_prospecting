// import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
// import type { Theme, ThemeContextType } from "@/types";

// const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// export const useTheme = (): ThemeContextType => {
//   const context = useContext(ThemeContext);
//   if (!context) {
//     throw new Error('useTheme must be used within a ThemeProvider');
//   }
//   return context;
// };

// interface ThemeProviderProps {
//   children: ReactNode;
// }

// export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
//   // State should be the theme string itself, not just a boolean
//   const [theme, setTheme] = useState<Theme>(() => {
//     const savedTheme = localStorage.getItem('prospectai-theme') as Theme | null;
//     if (savedTheme) {
//       return savedTheme;
//     }
//     return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
//   });

//   useEffect(() => {
//     // Logic to apply the theme to the document
//     const root = window.document.documentElement;
//     root.classList.remove('light', 'dark');
//     root.classList.add(theme);
//     localStorage.setItem('prospectai-theme', theme);
//   }, [theme]);

//   const toggleTheme = () => {
//     setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'));
//   };

//   // The provided value MUST match the ThemeContextType shape
//   const value: ThemeContextType = {
//     theme: theme,
//     isDark: theme === 'dark', // isDark is now derived from the theme state
//     toggleTheme,
//   };

//   return (
//     <ThemeContext.Provider value={value}>
//       {children}
//     </ThemeContext.Provider>
//   );
// };

// filepath: /Users/Nnamdi2/data_science_projects/B2B_sales_prospecting/prospect-ai-dashboard/src/contexts/ThemeContext.tsx
import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'

type Theme = 'light' | 'dark'
type Ctx = { theme: Theme; toggle: () => void }

const ThemeContext = createContext<Ctx | undefined>(undefined)

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>(() => {
    const saved = localStorage.getItem('theme')
    if (saved === 'light' || saved === 'dark') return saved
    const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches
    return prefersDark ? 'dark' : 'light'
  })

  useEffect(() => {
    const root = document.documentElement
    if (theme === 'dark') root.classList.add('dark')
    else root.classList.remove('dark')
    localStorage.setItem('theme', theme)
  }, [theme])

  const value = useMemo<Ctx>(() => ({ theme, toggle: () => setTheme(t => (t === 'dark' ? 'light' : 'dark')) }), [theme])

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

export const useTheme = () => {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider')
  return ctx
}