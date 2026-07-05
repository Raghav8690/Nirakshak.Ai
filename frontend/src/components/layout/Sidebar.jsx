import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Bell, FileText, BarChart3, ShieldCheck } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { name: 'Dashboard', path: '/', icon: <LayoutDashboard size={20} /> },
    { name: 'Engagement Feed', path: '/engagement', icon: <Bell size={20} /> },
    { name: 'Explainability', path: '/explainability', icon: <FileText size={20} /> },
    { name: 'Analytics', path: '/analytics', icon: <BarChart3 size={20} /> },
  ];

  return (
    <div className="w-64 h-screen glass-panel border-r border-white/5 flex flex-col fixed left-0 top-0 text-gray-300">
      <div className="p-6 flex items-center gap-3 border-b border-white/5">
        <div className="w-8 h-8 rounded-lg sbi-gradient flex items-center justify-center text-white">
          <ShieldCheck size={20} />
        </div>
        <div>
          <h1 className="text-xl font-bold text-white tracking-wide">Nirikshak<span className="text-blue-400">.AI</span></h1>
          <p className="text-[10px] text-gray-400 uppercase tracking-wider">Life-Stage Banking</p>
        </div>
      </div>

      <nav className="flex-1 py-6 px-4 flex flex-col gap-2">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                isActive 
                  ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' 
                  : 'hover:bg-white/5 hover:text-white'
              }`
            }
          >
            {item.icon}
            <span className="font-medium">{item.name}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-6 border-t border-white/5">
        <div className="bg-[#0b1121] rounded-xl p-4 border border-white/5">
          <p className="text-xs text-gray-400 mb-2">Hackathon Status</p>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="text-sm text-emerald-400 font-medium">System Active</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
