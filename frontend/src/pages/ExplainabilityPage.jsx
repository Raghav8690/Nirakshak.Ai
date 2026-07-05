import React, { useState, useEffect } from 'react';
import { getTriggers } from '../services/api';
import { BrainCircuit, Search, ArrowRight, Activity, Database, Sparkles, AlertCircle } from 'lucide-react';

const ExplainabilityPage = () => {
  const [triggers, setTriggers] = useState([]);
  const [selectedTrigger, setSelectedTrigger] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getTriggers().then(res => {
      setTriggers(res.data);
      if (res.data.length > 0) {
        setSelectedTrigger(res.data[0]);
      }
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="text-white p-8 animate-pulse">Loading Reasoning Traces...</div>;

  return (
    <div className="grid grid-cols-12 gap-6 h-[calc(100vh-8rem)]">
      {/* Sidebar List */}
      <div className="col-span-4 glass-card overflow-hidden flex flex-col">
        <div className="p-4 border-b border-white/5 bg-white/5">
          <h2 className="text-white font-semibold flex items-center gap-2">
            <BrainCircuit size={18} className="text-blue-400" /> Recent Triggers
          </h2>
        </div>
        <div className="flex-1 overflow-y-auto p-2">
          {triggers.map(trigger => (
            <button
              key={trigger.id}
              onClick={() => setSelectedTrigger(trigger)}
              className={`w-full text-left p-4 rounded-xl mb-2 transition-all ${
                selectedTrigger?.id === trigger.id
                  ? 'bg-blue-500/10 border border-blue-500/20 shadow-lg shadow-blue-500/5'
                  : 'hover:bg-white/5 border border-transparent'
              }`}
            >
              <div className="flex justify-between items-start mb-1">
                <span className="text-sm font-medium text-white line-clamp-1">{trigger.product_recommended}</span>
                <span className={`text-[10px] px-2 py-0.5 rounded capitalize ${
                  trigger.status === 'accepted' ? 'bg-emerald-500/20 text-emerald-400' :
                  trigger.status === 'dismissed' ? 'bg-red-500/20 text-red-400' :
                  'bg-white/10 text-gray-400'
                }`}>
                  {trigger.status}
                </span>
              </div>
              <p className="text-xs text-gray-400 font-mono mt-2">ID: {trigger.id} | {trigger.trigger_type}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Main Explainability View */}
      <div className="col-span-8 glass-card flex flex-col overflow-hidden">
        {selectedTrigger ? (
          <div className="h-full flex flex-col">
            <div className="p-6 border-b border-white/5">
              <div className="flex items-center gap-3 mb-2">
                <span className="px-3 py-1 bg-blue-500/20 text-blue-400 text-xs rounded-full border border-blue-500/20 uppercase tracking-wider font-semibold">
                  {selectedTrigger.trigger_type.replace(/_/g, ' ')}
                </span>
                <span className="text-sm text-gray-400">Confidence Score: <span className="text-white font-mono">{Math.round(selectedTrigger.confidence * 100)}%</span></span>
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">{selectedTrigger.product_recommended}</h2>
              <p className="text-sm text-gray-400 italic">" {selectedTrigger.explanation} "</p>
            </div>

            <div className="flex-1 overflow-y-auto p-8 bg-[#0b1121]/50">
              <h3 className="text-lg font-semibold text-white mb-6">Reasoning Trace</h3>
              
              <div className="relative pl-8 space-y-8 before:absolute before:inset-0 before:ml-10 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-white/10 before:to-transparent">
                
                {/* Step 1: Signal Detection */}
                <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-[#0b1121] bg-[#151e32] text-blue-400 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 relative">
                    <Activity size={16} />
                  </div>
                  <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] glass-panel p-5">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-blue-400 text-xs font-bold uppercase tracking-wider">Step 1</span>
                      <h4 className="text-white font-medium">Signal Detected</h4>
                    </div>
                    <p className="text-sm text-gray-400">{selectedTrigger.signal_detected}</p>
                  </div>
                </div>

                {/* Step 2: Context Retrieval */}
                <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-[#0b1121] bg-[#151e32] text-emerald-400 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 relative">
                    <Database size={16} />
                  </div>
                  <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] glass-panel p-5">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-emerald-400 text-xs font-bold uppercase tracking-wider">Step 2</span>
                      <h4 className="text-white font-medium">Context Retrieved</h4>
                    </div>
                    <ul className="text-xs text-gray-400 space-y-1 font-mono">
                      <li>• Fetched customer 360 profile</li>
                      <li>• Fetched 6-month transaction history</li>
                      <li>• Vector search for '{selectedTrigger.product_category}' products</li>
                    </ul>
                  </div>
                </div>

                {/* Step 3: LLM Reasoning */}
                <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-[#0b1121] bg-blue-600 text-white shadow shadow-blue-500/50 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 relative">
                    <Sparkles size={16} />
                  </div>
                  <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] glass-panel p-5 border-blue-500/30 shadow-[0_0_15px_rgba(0,85,255,0.1)]">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-white text-xs font-bold uppercase tracking-wider bg-blue-500 px-2 py-0.5 rounded">Step 3</span>
                      <h4 className="text-white font-medium">LLM Evaluation</h4>
                    </div>
                    <div className="space-y-2 text-sm text-gray-300">
                      {selectedTrigger.reasoning_trace?.steps?.map((step, idx) => (
                        <div key={idx} className="flex gap-2 items-start">
                          <Check size={14} className="text-emerald-400 mt-0.5 shrink-0" />
                          <span>{step}</span>
                        </div>
                      )) || <span className="text-gray-500 italic">No detailed steps available</span>}
                    </div>
                    
                    <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs text-gray-500 font-mono">
                      <span>Model: {selectedTrigger.reasoning_trace?.model || 'Unknown'}</span>
                      <span className="flex items-center gap-1"><AlertCircle size={12}/> RBI Compliant Trace</span>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-gray-500">
            Select a trigger to view its reasoning trace
          </div>
        )}
      </div>
    </div>
  );
};

export default ExplainabilityPage;
