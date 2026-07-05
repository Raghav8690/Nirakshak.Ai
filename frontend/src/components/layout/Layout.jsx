import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

const Layout = () => {
  return (
    <div className="flex min-h-screen bg-[#0b1121]">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col relative">
        <div className="absolute top-0 left-0 w-full h-96 bg-blue-900/10 rounded-full blur-3xl pointer-events-none -z-10" />
        <Header />
        <main className="p-8 flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
