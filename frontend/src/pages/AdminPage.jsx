import React, { useState, useEffect } from 'react';
import { getAnalytics } from '../services/api';
import { Users, BellRing, CheckCircle, Target, TrendingUp } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const AdminPage = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAnalytics().then(res => {
      setData(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="text-white p-8 animate-pulse">Loading Analytics...</div>;
  if (!data) return null;

  const stats = [
    { label: 'Total Customers', value: data.total_customers, icon: <Users size={20} />, color: 'text-blue-400', bg: 'bg-blue-400/10' },
    { label: 'Nudges Generated', value: data.total_triggers, icon: <BellRing size={20} />, color: 'text-purple-400', bg: 'bg-purple-400/10' },
    { label: 'Accepted Offers', value: data.total_accepted, icon: <CheckCircle size={20} />, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
    { label: 'Conversion Rate', value: `${data.acceptance_rate}%`, icon: <Target size={20} />, color: 'text-orange-400', bg: 'bg-orange-400/10' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">Admin Dashboard</h1>
        <p className="text-gray-400 text-sm">Aggregate performance of the proactive intelligence engine</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-4 gap-6">
        {stats.map((stat, idx) => (
          <div key={idx} className="glass-card p-6 flex items-center gap-4">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${stat.bg} ${stat.color}`}>
              {stat.icon}
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">{stat.label}</p>
              <h3 className="text-2xl font-bold text-white">{stat.value}</h3>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-12 gap-6">
        {/* Trend Chart */}
        <div className="col-span-8 glass-card p-6 h-96 flex flex-col">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <TrendingUp size={18} className="text-blue-400"/> Conversion Trend (Last 7 Days)
            </h3>
          </div>
          <div className="flex-1 w-full h-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.conversion_trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorAccepted" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorNudges" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff1a" vertical={false} />
                <XAxis dataKey="day" stroke="#6b7280" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#6b7280" fontSize={12} tickLine={false} axisLine={false} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#151e32', borderColor: '#ffffff1a', borderRadius: '8px' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Area type="monotone" dataKey="nudges" name="Nudges Sent" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#colorNudges)" />
                <Area type="monotone" dataKey="accepted" name="Accepted" stroke="#10b981" strokeWidth={2} fillOpacity={1} fill="url(#colorAccepted)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Trigger Type Breakdown */}
        <div className="col-span-4 glass-card p-6 h-96 flex flex-col">
          <h3 className="text-lg font-semibold text-white mb-6">Top Trigger Types</h3>
          <div className="flex-1 w-full h-full overflow-hidden">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.trigger_type_breakdown.slice(0, 5)} layout="vertical" margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff1a" horizontal={false} />
                <XAxis type="number" stroke="#6b7280" fontSize={10} hide />
                <YAxis dataKey="trigger_type" type="category" stroke="#e5e7eb" fontSize={11} tickLine={false} axisLine={false} width={120} tickFormatter={(val) => val.replace(/_/g, ' ')} />
                <RechartsTooltip 
                  cursor={{fill: '#ffffff0a'}}
                  contentStyle={{ backgroundColor: '#151e32', borderColor: '#ffffff1a', borderRadius: '8px' }}
                />
                <Bar dataKey="total" name="Total Nudges" fill="#3b82f6" radius={[0, 4, 4, 0]} barSize={16} />
                <Bar dataKey="accepted" name="Accepted" fill="#10b981" radius={[0, 4, 4, 0]} barSize={16} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPage;
