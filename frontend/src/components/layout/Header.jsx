import React from 'react';
import { Search, User, Settings, BellRing } from 'lucide-react';

const Header = () => {
  return (
    <header className="h-20 px-8 flex items-center justify-between glass-panel border-b border-white/5 sticky top-0 z-10">
      <div className="flex items-center bg-[#0b1121] border border-white/10 rounded-xl px-4 py-2 w-96">
        <Search size={18} className="text-gray-400" />
        <input 
          type="text" 
          placeholder="Search customers, transactions..." 
          className="bg-transparent border-none outline-none text-sm text-gray-200 ml-3 w-full placeholder-gray-500"
        />
      </div>

      <div className="flex items-center gap-4">
        <button className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center hover:bg-white/10 transition-colors relative">
          <BellRing size={18} className="text-gray-300" />
          <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
        <button className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center hover:bg-white/10 transition-colors">
          <Settings size={18} className="text-gray-300" />
        </button>
        <div className="flex items-center gap-3 ml-4 pl-4 border-l border-white/10">
          <div className="w-10 h-10 rounded-xl sbi-gradient flex items-center justify-center border border-white/20">
            <User size={20} className="text-white" />
          </div>
          <div>
            <p className="text-sm font-medium text-white">Rahul S.R.</p>
            <p className="text-xs text-gray-400">Admin / Analyst</p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
