import React, { useState, useEffect } from 'react';
import { getCustomers, getCustomer360, scanTriggers } from '../services/api';
import { User, CreditCard, ShieldCheck, TrendingUp, Activity, Search } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const COLORS = ['#0033A0', '#0055ff', '#3377ff', '#6699ff', '#99bbff', '#ccddee'];

const DashboardPage = () => {
  const [customers, setCustomers] = useState([]);
  const [selectedCustomerId, setSelectedCustomerId] = useState(null);
  const [customerData, setCustomerData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);

  useEffect(() => {
    getCustomers().then(res => {
      setCustomers(res.data);
      if (res.data.length > 0) {
        setSelectedCustomerId(res.data[0].id);
      }
      setLoading(false);
    });
  }, []);

  useEffect(() => {
    if (selectedCustomerId) {
      getCustomer360(selectedCustomerId).then(res => setCustomerData(res.data));
    }
  }, [selectedCustomerId]);

  const handleScan = async () => {
    setScanning(true);
    try {
      await scanTriggers(selectedCustomerId);
      const res = await getCustomer360(selectedCustomerId);
      setCustomerData(res.data);
    } catch (e) {
      console.error(e);
    }
    setScanning(false);
  };

  if (loading) return <div className="text-white p-8 animate-pulse">Loading Customer Data...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white">Customer 360</h1>
          <p className="text-gray-400 text-sm">Comprehensive view of customer profile and financial health</p>
        </div>
        <div className="flex gap-4">
          <select 
            className="bg-[#151e32] border border-white/10 rounded-xl px-4 py-2 text-white outline-none focus:border-blue-500"
            value={selectedCustomerId || ''}
            onChange={(e) => setSelectedCustomerId(e.target.value)}
          >
            {customers.map(c => (
              <option key={c.id} value={c.id}>{c.name} ({c.account_number})</option>
            ))}
          </select>
          <button 
            onClick={handleScan}
            disabled={scanning}
            className="sbi-gradient text-white px-6 py-2 rounded-xl font-medium shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40 transition-all flex items-center gap-2 disabled:opacity-50"
          >
            <Activity size={18} className={scanning ? "animate-spin" : ""} />
            {scanning ? "Scanning..." : "Scan for Patterns"}
          </button>
        </div>
      </div>

      {customerData && (
        <div className="grid grid-cols-12 gap-6">
          {/* Profile Card */}
          <div className="col-span-4 glass-card p-6">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-16 h-16 rounded-full sbi-gradient flex items-center justify-center text-white text-2xl font-bold">
                {customerData.name.charAt(0)}
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">{customerData.name}</h2>
                <p className="text-sm text-gray-400">{customerData.occupation} • {customerData.age} yrs</p>
              </div>
            </div>
            
            <div className="space-y-4">
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-gray-400 text-sm">Monthly Income</span>
                <span className="text-white font-medium font-mono">₹{customerData.monthly_income.toLocaleString()}</span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-gray-400 text-sm">Account Type</span>
                <span className="text-white font-medium">{customerData.account_type}</span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-gray-400 text-sm">Risk Profile</span>
                <span className="text-white font-medium capitalize">{customerData.risk_profile}</span>
              </div>
              <div className="flex justify-between pb-2">
                <span className="text-gray-400 text-sm">KYC Status</span>
                <span className="text-emerald-400 font-medium flex items-center gap-1">
                  <ShieldCheck size={14} /> {customerData.kyc_status}
                </span>
              </div>
            </div>
          </div>

          {/* Financial Health Score */}
          <div className="col-span-4 glass-card p-6 flex flex-col items-center justify-center relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-2xl -mr-10 -mt-10"></div>
            <h3 className="text-gray-400 text-sm mb-4">Financial Health Score</h3>
            <div className="relative w-32 h-32">
              <svg viewBox="0 0 36 36" className="w-32 h-32 transform -rotate-90">
                <path className="text-gray-800" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3" />
                <path className="text-blue-500" strokeDasharray={`${customerData.financial_health_score}, 100`} d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3" />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center flex-col">
                <span className="text-3xl font-bold text-white">{customerData.financial_health_score}</span>
                <span className="text-[10px] text-gray-400">/ 100</span>
              </div>
            </div>
            <p className="text-xs text-center text-gray-400 mt-4 px-4">
              Score based on savings ratio, credit usage, and transaction consistency.
            </p>
          </div>

          {/* Key Metrics */}
          <div className="col-span-4 flex flex-col gap-6">
            <div className="glass-card p-6 flex-1 flex flex-col justify-center">
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 bg-emerald-500/20 rounded-lg text-emerald-400">
                  <TrendingUp size={20} />
                </div>
                <span className="text-gray-400 text-sm">Total Inflow (6mo)</span>
              </div>
              <h4 className="text-2xl font-bold text-white font-mono">₹{customerData.total_credits.toLocaleString()}</h4>
            </div>
            
            <div className="glass-card p-6 flex-1 flex flex-col justify-center">
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 bg-orange-500/20 rounded-lg text-orange-400">
                  <CreditCard size={20} />
                </div>
                <span className="text-gray-400 text-sm">Total Outflow (6mo)</span>
              </div>
              <h4 className="text-2xl font-bold text-white font-mono">₹{customerData.total_debits.toLocaleString()}</h4>
            </div>
          </div>

          {/* Spend Categories */}
          <div className="col-span-6 glass-card p-6 h-80 flex flex-col">
            <h3 className="text-white font-medium mb-4">Spend Categories</h3>
            <div className="flex-1">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={customerData.top_spend_categories}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="amount"
                  >
                    {customerData.top_spend_categories.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#151e32', borderColor: '#ffffff1a', borderRadius: '8px' }}
                    itemStyle={{ color: '#fff' }}
                    formatter={(value) => `₹${value.toLocaleString()}`}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Product Holdings */}
          <div className="col-span-6 glass-card p-6">
            <h3 className="text-white font-medium mb-4">Current Product Holdings</h3>
            <div className="flex flex-wrap gap-3">
              {customerData.product_holdings.map((product, idx) => (
                <div key={idx} className="bg-white/5 border border-white/10 px-4 py-3 rounded-xl flex items-center gap-3">
                  <ShieldCheck size={18} className="text-blue-400" />
                  <span className="text-gray-200 text-sm">{product}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
