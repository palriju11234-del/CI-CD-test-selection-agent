import React, { useState } from 'react';

export default function Dashboard({ currentUser, onBackToLanding, onLogout, showToast }) {
  const [activeNav, setActiveNav] = useState('Dashboard');
  const [activeTab, setActiveTab] = useState('selected');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Modals state
  const [showPrModal, setShowPrModal] = useState(false);
  const [showGithubModal, setShowGithubModal] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  
  // Simulation states
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionProgress, setExecutionProgress] = useState(0);
  const [isReanalyzing, setIsReanalyzing] = useState(false);

  // Settings state
  const [confidenceThreshold, setConfidenceThreshold] = useState(80);
  const [selectedRunner, setSelectedRunner] = useState('pytest');
  const [slackAlerts, setSlackAlerts] = useState(true);

  const selectedTestsData = [
    {
      name: 'test_payment.py',
      path: 'tests/test_payment.py',
      reason: 'Direct dependency (payment_service.py)',
      confidence: 96,
      status: 'Selected',
      duration: '1.2s',
      risk: 'High',
    },
    {
      name: 'test_order_payment.py',
      path: 'tests/test_order_payment.py',
      reason: 'Related module (orders → payment)',
      confidence: 92,
      status: 'Selected',
      duration: '2.4s',
      risk: 'High',
    },
    {
      name: 'test_checkout.py',
      path: 'tests/test_checkout.py',
      reason: 'Function call chain (handle_checkout)',
      confidence: 88,
      status: 'Selected',
      duration: '3.1s',
      risk: 'Medium',
    },
    {
      name: 'test_refund.py',
      path: 'tests/test_refund.py',
      reason: 'Related logic (payment flow & credit)',
      confidence: 84,
      status: 'Selected',
      duration: '0.8s',
      risk: 'Medium',
    },
    {
      name: 'test_payment_utils.py',
      path: 'tests/test_payment_utils.py',
      reason: 'Shared utility functions (crypto/hash)',
      confidence: 76,
      status: 'Selected',
      duration: '0.4s',
      risk: 'Low',
    },
    {
      name: 'test_stripe_gateway.py',
      path: 'tests/gateways/test_stripe.py',
      reason: 'Modified API payload schema',
      confidence: 94,
      status: 'Selected',
      duration: '1.9s',
      risk: 'High',
    },
    {
      name: 'test_webhook_listener.py',
      path: 'tests/api/test_webhooks.py',
      reason: 'Payment event subscription hook',
      confidence: 90,
      status: 'Selected',
      duration: '1.1s',
      risk: 'Medium',
    },
    {
      name: 'test_invoice_generation.py',
      path: 'tests/billing/test_invoice.py',
      reason: 'Downstream dependency from checkout',
      confidence: 82,
      status: 'Selected',
      duration: '2.8s',
      risk: 'Low',
    },
  ];

  const skippedTestsData = [
    {
      name: 'test_auth_legacy.py',
      path: 'tests/legacy/test_auth.py',
      reason: 'Unrelated module (no code diff in AST)',
      confidence: 99,
      status: 'Skipped',
      duration: '4.5s (saved)',
      risk: 'Zero',
    },
    {
      name: 'test_billing_tax.py',
      path: 'tests/billing/test_tax.py',
      reason: 'Independent service (isolated domain)',
      confidence: 95,
      status: 'Skipped',
      duration: '3.8s (saved)',
      risk: 'Zero',
    },
    {
      name: 'test_inventory_sync.py',
      path: 'tests/inventory/test_sync.py',
      reason: 'No dependency on payment v2 branch',
      confidence: 94,
      status: 'Skipped',
      duration: '6.2s (saved)',
      risk: 'Zero',
    },
    {
      name: 'test_user_profile.py',
      path: 'tests/users/test_profile.py',
      reason: 'Out of scope for checkout PR',
      confidence: 91,
      status: 'Skipped',
      duration: '2.1s (saved)',
      risk: 'Zero',
    },
    {
      name: 'test_notification_sms.py',
      path: 'tests/notifications/test_sms.py',
      reason: 'Mocked external gateway unaffected',
      confidence: 89,
      status: 'Skipped',
      duration: '1.9s (saved)',
      risk: 'Zero',
    },
    {
      name: 'test_recommendations.py',
      path: 'tests/ml/test_recommendations.py',
      reason: 'ML pipeline isolated from transaction core',
      confidence: 98,
      status: 'Skipped',
      duration: '14.2s (saved)',
      risk: 'Zero',
    },
    {
      name: 'test_search_indexing.py',
      path: 'tests/search/test_indexing.py',
      reason: 'Elasticsearch cluster worker isolated',
      confidence: 96,
      status: 'Skipped',
      duration: '8.4s (saved)',
      risk: 'Zero',
    },
  ];

  const pastRuns = [
    { id: 'PR #182', branch: 'feature/payment-v2', author: '@sayak-code', selected: 1532, total: 5482, saved: '71%', status: 'Passed', time: '14:32 Today' },
    { id: 'PR #181', branch: 'fix/auth-jwt-refresh', author: '@alex-dev', selected: 420, total: 5482, saved: '92%', status: 'Passed', time: '11:15 Today' },
    { id: 'PR #180', branch: 'feat/cart-drawer-ui', author: '@sarah-ui', selected: 890, total: 5482, saved: '84%', status: 'Passed', time: 'Yesterday' },
    { id: 'PR #179', branch: 'refactor/db-connection-pool', author: '@marcus-eng', selected: 2140, total: 5482, saved: '61%', status: 'Passed', time: '2 days ago' },
  ];

  const currentList = activeTab === 'selected' ? selectedTestsData : skippedTestsData;
  const filteredList = currentList.filter(
    (t) =>
      t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.path.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.reason.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // 1. Download Report functionality
  const handleDownloadReport = () => {
    const reportData = {
      product: 'QUBIS AI Test Intelligence',
      pipeline_run: {
        pull_request: 'PR #182',
        title: 'feat: update payment service logic',
        author: '@sayak-code (Sayak Adak)',
        repository: 'ecommerce',
        branch: 'feature/payment-v2 -> main',
        commit: 'a83f92c',
        timestamp: 'Sep 24, 2025 • 14:32 UTC',
        status: 'COMPLETED (All selected tests passed)',
      },
      metrics: {
        total_tests_in_suite: 5482,
        qubis_selected_tests: 1532,
        qubis_skipped_tests: 3950,
        test_reduction_percentage: '72%',
        ci_execution_time_saved: '71%',
        duration_with_qubis: '5m 12s',
        duration_without_qubis: '18m 00s',
        time_saved_in_seconds: 768,
      },
      ai_confidence_metrics: {
        overall_confidence: '91%',
        false_negative_risk: '0.0%',
        model_version: 'QUBIS-v3.4-transformer',
        last_retrained: '2025-09-20',
      },
      selected_tests_sample: selectedTestsData,
      skipped_tests_sample: skippedTestsData,
    };

    const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `qubis-test-selection-report-pr182.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    if (showToast) {
      showToast('✓ QUBIS Report downloaded (qubis-test-selection-report-pr182.json)');
    }
  };

  // 2. Test Execution Simulation
  const handleRunSelectedTests = () => {
    if (isExecuting) return;
    setIsExecuting(true);
    setExecutionProgress(10);

    const interval = setInterval(() => {
      setExecutionProgress((prev) => {
        if (prev >= 90) {
          clearInterval(interval);
          setTimeout(() => {
            setIsExecuting(false);
            setExecutionProgress(0);
            if (showToast) {
              showToast('⚡ Executed 12 selected tests: ALL PASSED in 1m 24s! (CI Saved 12m 36s)');
            }
          }, 400);
          return 100;
        }
        return prev + 25;
      });
    }, 280);
  };

  // 3. AI Re-analysis simulation
  const handleReanalyze = () => {
    if (isReanalyzing) return;
    setIsReanalyzing(true);
    setTimeout(() => {
      setIsReanalyzing(false);
      if (showToast) {
        showToast('✓ AI Re-analysis complete: Code graph validated. 1,532 tests verified.');
      }
    }, 1200);
  };

  return (
    <div className="relative w-full min-h-screen bg-[#F5F5F5] pt-[72px] lg:pt-[88px] pb-16 overflow-hidden">
      
      {/* Ambient background glow accents matching landing page */}
      <div 
        className="absolute top-20 right-0 w-[500px] h-[500px] rounded-full pointer-events-none opacity-20 blur-[100px]"
        style={{ background: 'radial-gradient(circle, #FEB048 0%, rgba(211,92,7,0) 70%)' }}
      />
      <div 
        className="absolute bottom-20 left-0 w-[450px] h-[450px] rounded-full pointer-events-none opacity-15 blur-[100px]"
        style={{ background: 'radial-gradient(circle, #D35C07 0%, rgba(211,92,7,0) 70%)' }}
      />

      <div className="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        {/* Top Control Header matching Landing Page Theme */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 pt-4">
          <div>
            <div className="flex items-center gap-3">
              <span className="font-orbitron font-extrabold text-2xl lg:text-3xl text-gradient-orbitron tracking-tight">
                QUBIS
              </span>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-orange-100/90 text-tm-orange text-xs font-semibold uppercase tracking-wider border border-orange-200">
                <span className="w-2 h-2 rounded-full bg-tm-orange animate-ping" />
                Live CI Intelligence
              </div>
            </div>
            <p className="font-inter text-sm text-black/60 mt-1">
              Active Session: Reviewing automated test selection for <strong className="text-black font-semibold">PR #182 (payment-v2)</strong>
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Back to landing page button */}
            <button
              onClick={onBackToLanding}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/85 border border-[#DAD7D7] hover:border-tm-orange text-xs font-medium text-black transition-all shadow-sm cursor-pointer hover:bg-white"
            >
              <span>← Back to Landing Page</span>
            </button>

            {/* Re-analyze button */}
            <button
              onClick={handleReanalyze}
              disabled={isReanalyzing}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/85 border border-[#DAD7D7] hover:border-tm-orange text-xs font-medium text-black transition-all shadow-sm cursor-pointer disabled:opacity-50"
            >
              <svg className={`w-3.5 h-3.5 text-tm-orange ${isReanalyzing ? 'animate-spin' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>{isReanalyzing ? 'Analyzing Code...' : 'Re-analyze PR'}</span>
            </button>

            {/* Download Report Button */}
            <button
              onClick={handleDownloadReport}
              className="btn-get-started inline-flex items-center gap-2 px-5 py-2 rounded-full text-xs font-semibold text-black tracking-normal shadow-sm cursor-pointer hover:scale-[1.02] transition-transform"
            >
              <svg className="w-4 h-4 text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              <span>Download Report</span>
            </button>

            {/* Notifications Button */}
            <div className="relative">
              <button
                onClick={() => setShowNotifications(!showNotifications)}
                className="w-9 h-9 rounded-full bg-white/85 border border-[#DAD7D7] hover:border-tm-orange flex items-center justify-center text-tm-orange transition-colors relative cursor-pointer"
                aria-label="View notifications"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-tm-orange" />
              </button>

              {/* Notification dropdown */}
              {showNotifications && (
                <div className="absolute right-0 mt-2 w-80 p-4 rounded-2xl bg-white/95 backdrop-blur-xl border border-[#DAD7D7] shadow-xl z-50 animate-fade-in text-left">
                  <div className="flex items-center justify-between pb-2 border-b border-[#DAD7D7] mb-2">
                    <span className="font-semibold text-xs text-black">CI Notifications</span>
                    <button onClick={() => setShowNotifications(false)} className="text-xs text-black/40 hover:text-black">✕</button>
                  </div>
                  <div className="space-y-2 text-xs">
                    <div className="p-2 rounded-lg bg-orange-50/70 border border-orange-200/50">
                      <p className="font-bold text-[#D35C07]">PR #182 Analyzed</p>
                      <p className="text-black/70 text-[11px]">Selected 1,532 tests out of 5,482 in 1.4s.</p>
                    </div>
                    <div className="p-2 rounded-lg bg-emerald-50/70 border border-emerald-200/50">
                      <p className="font-bold text-emerald-800">71% CI Time Saved</p>
                      <p className="text-black/70 text-[11px]">Saved 12m 48s compute time on this branch.</p>
                    </div>
                    <div className="p-2 rounded-lg bg-slate-50 border border-slate-200">
                      <p className="font-bold text-slate-800">Model Updated</p>
                      <p className="text-black/70 text-[11px]">QUBIS v3.4 zero false-negative guarantee active.</p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* User profile & logout */}
            <div className="flex items-center gap-2 pl-2 border-l border-[#DAD7D7]">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#FEB048] to-[#D35C07] text-white flex items-center justify-center font-bold text-xs shadow-sm">
                SA
              </div>
              <div className="hidden sm:block text-left text-xs">
                <p className="font-bold text-black leading-none">{currentUser?.name || 'Sayak Adak'}</p>
                <p className="text-[10px] text-black/50 leading-tight mt-0.5">{currentUser?.role || 'Reviewer'}</p>
              </div>
              <button
                onClick={onLogout}
                className="text-xs text-black/40 hover:text-[#D35C07] ml-1 transition-colors cursor-pointer"
                title="Sign out"
              >
                Exit
              </button>
            </div>
          </div>
        </div>

        {/* Execution progress banner if running */}
        {isExecuting && (
          <div className="mb-6 p-4 rounded-2xl bg-white/90 border border-[#FEB048] shadow-md animate-fade-in">
            <div className="flex items-center justify-between text-xs font-semibold mb-2">
              <span className="flex items-center gap-2 text-[#D35C07]">
                <span className="w-2.5 h-2.5 rounded-full bg-[#D35C07] animate-ping" />
                Executing Selected Test Suite (12 targeted tests across 3 workers)...
              </span>
              <span>{executionProgress}%</span>
            </div>
            <div className="w-full h-2 rounded-full bg-orange-100 overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-[#FEB048] to-[#D35C07] transition-all duration-300"
                style={{ width: `${executionProgress}%` }}
              />
            </div>
          </div>
        )}

        {/* Main Dashboard App Frame with matching Landing Page Glassmorphism */}
        <div className="w-full card-new-glass rounded-[24px] border border-[#DAD7D7] shadow-xl overflow-hidden flex flex-col lg:flex-row">
          
          {/* Sidebar styled with sleek developer obsidian glass */}
          <aside className="w-full lg:w-[250px] bg-[#121316]/95 backdrop-blur-xl text-white p-5 flex flex-col justify-between shrink-0 border-r border-[#DAD7D7]/30">
            <div>
              {/* Brand wordmark inside sidebar */}
              <div className="flex items-center gap-3 mb-8">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#FEB048] to-[#D35C07] flex items-center justify-center shadow-md">
                  <svg className="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
                  </svg>
                </div>
                <div>
                  <span className="font-orbitron font-extrabold text-xl tracking-wider text-white">
                    QUBIS
                  </span>
                  <p className="text-[8px] tracking-[2px] text-[#AEB8C7] uppercase font-semibold">
                    CI Agent v3.4
                  </p>
                </div>
              </div>

              {/* Sidebar Navigation */}
              <nav className="flex flex-col gap-1.5 font-inter text-[13px]">
                {[
                  { name: 'Dashboard', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
                  { name: 'Pipeline Reports', icon: 'M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
                  { name: 'Test Analytics', icon: 'M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z' },
                  { name: 'Model Performance', icon: 'M13 10V3L4 14h7v7l9-11h-7z' },
                  { name: 'Repositories', icon: 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z' },
                  { name: 'Settings', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z' },
                ].map((item) => (
                  <button
                    key={item.name}
                    onClick={() => setActiveNav(item.name)}
                    className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-all cursor-pointer ${
                      activeNav === item.name
                        ? 'bg-gradient-to-r from-[#FEB048] to-[#D35C07] text-black font-bold shadow-md'
                        : 'text-[#C6CFDB] hover:bg-white/10 hover:text-white font-normal'
                    }`}
                  >
                    <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={item.icon} />
                    </svg>
                    <span>{item.name}</span>
                  </button>
                ))}
              </nav>
            </div>

            {/* Sidebar System Health Card */}
            <div className="mt-8 p-3.5 rounded-xl bg-white/5 border border-white/10 backdrop-blur-md">
              <div className="flex items-center gap-2 mb-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-[#39D39F] animate-pulse" />
                <span className="text-[12px] font-bold text-white">CI Webhook Live</span>
              </div>
              <p className="text-[10.5px] text-[#AEB8C7] leading-tight">
                Listening to GitHub push events. Real-time inference active.
              </p>
            </div>
          </aside>

          {/* Main Dashboard Content Area */}
          <div className="flex-1 flex flex-col min-w-0 bg-[#F5F5F5]">
            
            {/* Top Sub-Bar */}
            <header className="h-[64px] bg-white/70 backdrop-blur-md border-b border-[#DAD7D7] px-6 flex items-center justify-between">
              <div className="flex items-center gap-2 text-[13px]">
                <span className="text-black/60">Repository:</span>
                <span className="font-semibold text-black">ecommerce</span>
                <span className="text-black/30">/</span>
                <span className="text-[#D35C07] font-bold">feature/payment-v2</span>
              </div>

              <div className="flex items-center gap-3">
                <button
                  onClick={handleRunSelectedTests}
                  disabled={isExecuting}
                  className="px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-300 text-emerald-800 text-xs font-semibold hover:bg-emerald-100 transition-colors flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
                >
                  <span>▶</span>
                  <span>Run Selected (12)</span>
                </button>
              </div>
            </header>

            {/* Dashboard Scrollable Body */}
            <div className="p-6 space-y-6">
              
              {/* SUBVIEW 1: Main Dashboard */}
              {activeNav === 'Dashboard' && (
                <>
                  {/* Title & Run Status */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div>
                      <h3 className="font-inter font-bold text-2xl text-black">
                        Pipeline Report — PR #182
                      </h3>
                      <p className="text-xs text-black/60 mt-0.5">
                        Automated AI test selection analysis. 1,532 relevant tests prioritized out of 5,482 total.
                      </p>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-xs text-black/60">Sep 24, 2025 • 14:32</span>
                      <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold border border-emerald-200">
                        Passed
                      </span>
                      <button
                        onClick={() => setShowGithubModal(true)}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white/80 border border-[#DAD7D7] rounded-lg text-xs font-semibold text-black hover:border-[#D35C07] transition-colors shadow-sm cursor-pointer"
                      >
                        <svg className="w-3.5 h-3.5 text-black" fill="currentColor" viewBox="0 0 24 24">
                          <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
                        </svg>
                        <span>View in GitHub</span>
                      </button>
                    </div>
                  </div>

                  {/* 5 KPI Cards Row matching Landing Page card-new-glass */}
                  <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5">
                    {/* KPI 1 */}
                    <div className="card-new-glass p-4 rounded-2xl border border-[#DAD7D7] flex flex-col justify-between">
                      <div className="flex items-center gap-2.5 mb-2">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#FEB048]/20 to-[#D35C07]/20 border border-[#D35C07]/30 flex items-center justify-center font-bold text-xs text-[#D35C07]">
                          &lt;/&gt;
                        </div>
                        <span className="text-[11px] font-medium text-black/60">Total Tests</span>
                      </div>
                      <div>
                        <span className="font-inter font-bold text-2xl text-black">5,482</span>
                        <p className="text-[10px] text-[#16865D] font-semibold mt-0.5">
                          Full test suite
                        </p>
                      </div>
                    </div>

                    {/* KPI 2 */}
                    <div className="card-new-glass p-4 rounded-2xl border border-[#DAD7D7] flex flex-col justify-between">
                      <div className="flex items-center gap-2.5 mb-2">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#FEB048]/20 to-[#D35C07]/20 border border-[#D35C07]/30 flex items-center justify-center text-[#D35C07]">
                          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                        <span className="text-[11px] font-medium text-black/60">Selected Tests</span>
                      </div>
                      <div>
                        <span className="font-inter font-bold text-2xl text-[#D35C07]">1,532</span>
                        <p className="text-[10px] text-[#16865D] font-semibold mt-0.5">
                          ↓ 72% <span className="text-black/50 font-normal">reduction</span>
                        </p>
                      </div>
                    </div>

                    {/* KPI 3 */}
                    <div className="card-new-glass p-4 rounded-2xl border border-[#DAD7D7] flex flex-col justify-between">
                      <div className="flex items-center gap-2.5 mb-2">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#FEB048]/20 to-[#D35C07]/20 border border-[#D35C07]/30 flex items-center justify-center text-[#D35C07]">
                          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </div>
                        <span className="text-[11px] font-medium text-black/60">Skipped Tests</span>
                      </div>
                      <div>
                        <span className="font-inter font-bold text-2xl text-black">3,950</span>
                        <p className="text-[10px] text-[#16865D] font-semibold mt-0.5">
                          ✓ 0 false negatives
                        </p>
                      </div>
                    </div>

                    {/* KPI 4 */}
                    <div className="card-new-glass p-4 rounded-2xl border border-[#DAD7D7] flex flex-col justify-between">
                      <div className="flex items-center gap-2.5 mb-2">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#FEB048]/20 to-[#D35C07]/20 border border-[#D35C07]/30 flex items-center justify-center text-[#D35C07]">
                          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <span className="text-[11px] font-medium text-black/60">CI Time Saved</span>
                      </div>
                      <div>
                        <span className="font-inter font-bold text-2xl text-[#D35C07]">71%</span>
                        <p className="text-[10px] text-black/60 font-semibold mt-0.5">
                          18m → 5m 12s
                        </p>
                      </div>
                    </div>

                    {/* KPI 5 - Highlight Value Card */}
                    <div className="col-span-2 sm:col-span-1 p-4 rounded-2xl border border-[#FEB048] bg-gradient-to-br from-orange-50/90 to-amber-50/70 shadow-sm flex flex-col justify-between">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="w-7 h-7 rounded-full bg-[#FFE5CC] flex items-center justify-center text-[#D85B0B] text-xs">
                          ⚡
                        </div>
                        <span className="text-[11px] font-bold text-[#D85B0B]">Value Delivered</span>
                      </div>
                      <div className="space-y-0.5 text-[11px] font-bold text-[#087653] leading-tight">
                        <p>✓ Faster feedback</p>
                        <p>✓ Lower compute bill</p>
                        <p>✓ Zero flaky delays</p>
                      </div>
                    </div>
                  </div>

                  {/* Chart & PR Details Grid */}
                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
                    
                    {/* Left Overview Chart (Span 8) */}
                    <div className="lg:col-span-8 card-new-glass p-5 rounded-2xl border border-[#DAD7D7] flex flex-col justify-between">
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <h4 className="font-inter font-bold text-[16px] text-black">
                            Test Selection & Execution Curve
                          </h4>
                          <p className="text-[11px] text-black/50">Historic pipeline executions for payment-v2 branch</p>
                        </div>
                        <div className="flex items-center gap-4 text-xs">
                          <div className="flex items-center gap-1.5">
                            <span className="w-2.5 h-2.5 rounded-full bg-[#D35C07]" />
                            <span className="text-black/70">Selected (1,532)</span>
                          </div>
                          <div className="flex items-center gap-1.5">
                            <span className="w-2.5 h-2.5 rounded-full bg-[#FEB048]" />
                            <span className="text-black/70">Skipped (3,950)</span>
                          </div>
                        </div>
                      </div>

                      {/* Chart and Donut Flex */}
                      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
                        
                        {/* SVG Line / Area Graph with landing page colors */}
                        <div className="md:col-span-8">
                          <svg viewBox="0 0 450 160" className="w-full h-auto overflow-visible">
                            {/* Grid lines */}
                            <line x1="30" y1="20" x2="440" y2="20" stroke="#E2E8F0" strokeWidth="1" strokeDasharray="2 2" />
                            <line x1="30" y1="55" x2="440" y2="55" stroke="#E2E8F0" strokeWidth="1" strokeDasharray="2 2" />
                            <line x1="30" y1="90" x2="440" y2="90" stroke="#E2E8F0" strokeWidth="1" strokeDasharray="2 2" />
                            <line x1="30" y1="125" x2="440" y2="125" stroke="#CBD5E1" strokeWidth="1" />
                            
                            {/* Y-axis labels */}
                            <text x="5" y="24" fill="#94A3B8" fontSize="10">6K</text>
                            <text x="5" y="59" fill="#94A3B8" fontSize="10">4K</text>
                            <text x="5" y="94" fill="#94A3B8" fontSize="10">2K</text>
                            <text x="12" y="129" fill="#94A3B8" fontSize="10">0</text>

                            {/* Area gradient */}
                            <defs>
                              <linearGradient id="areaGradientQubis" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stopColor="#FEB048" stopOpacity="0.45" />
                                <stop offset="100%" stopColor="#D35C07" stopOpacity="0.0" />
                              </linearGradient>
                            </defs>

                            {/* Area fill */}
                            <path
                              d="M 35 100 Q 90 60, 150 70 T 270 55 T 380 75 T 440 60 L 440 125 L 35 125 Z"
                              fill="url(#areaGradientQubis)"
                            />

                            {/* Selected Tests Line */}
                            <path
                              d="M 35 100 Q 90 60, 150 70 T 270 55 T 380 75 T 440 60"
                              fill="none"
                              stroke="#D35C07"
                              strokeWidth="3"
                              strokeLinecap="round"
                            />

                            {/* Skipped Tests Line */}
                            <path
                              d="M 35 110 Q 90 90, 150 82 T 270 76 T 380 72 T 440 58"
                              fill="none"
                              stroke="#FEB048"
                              strokeWidth="2.5"
                              strokeDasharray="4 4"
                            />

                            {/* Data Points with hover glow */}
                            {[
                              [35, 100], [90, 65], [150, 70], [210, 60], [270, 55], [330, 68], [380, 75], [440, 60]
                            ].map(([cx, cy], i) => (
                              <circle 
                                key={i} 
                                cx={cx} 
                                cy={cy} 
                                r="4" 
                                fill="#D35C07" 
                                stroke="#FFFFFF" 
                                strokeWidth="2"
                                className="hover:scale-150 transition-transform cursor-pointer"
                              />
                            ))}

                            {/* X-axis labels */}
                            {['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'].map((time, idx) => (
                              <text key={time} x={35 + idx * 65} y="145" fill="#64748B" fontSize="9" textAnchor="middle">
                                {time}
                              </text>
                            ))}
                          </svg>
                        </div>

                        {/* Donut Chart with matching warm tones */}
                        <div className="md:col-span-4 flex flex-col items-center justify-center p-3 border-t md:border-t-0 md:border-l border-[#DAD7D7]/60">
                          <div className="relative w-28 h-28 flex items-center justify-center">
                            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                              <circle cx="50" cy="50" r="38" stroke="#FFE6D5" strokeWidth="12" fill="none" />
                              <circle
                                cx="50"
                                cy="50"
                                r="38"
                                stroke="#D35C07"
                                strokeWidth="12"
                                strokeDasharray="167 238"
                                strokeLinecap="round"
                                fill="none"
                              />
                            </svg>
                            <div className="absolute text-center">
                              <span className="font-inter font-bold text-2xl text-black">71%</span>
                              <p className="text-[9px] text-[#D35C07] uppercase font-bold">Time Saved</p>
                            </div>
                          </div>
                          <div className="mt-3 text-xs space-y-1.5 w-full text-left pl-2">
                            <div className="flex items-center justify-between text-black/80">
                              <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-[#D35C07]" />Selected</span>
                              <span className="font-semibold text-xs">1,532 (28%)</span>
                            </div>
                            <div className="flex items-center justify-between text-black/80">
                              <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-[#FEB048]" />Skipped</span>
                              <span className="font-semibold text-xs">3,950 (72%)</span>
                            </div>
                          </div>
                        </div>

                      </div>
                    </div>

                    {/* Right PR Details Card (Span 4) */}
                    <div className="lg:col-span-4 card-new-glass p-5 rounded-2xl border border-[#DAD7D7] flex flex-col justify-between">
                      <div>
                        <div className="flex items-center justify-between mb-3">
                          <h4 className="font-inter font-bold text-[15px] text-black">PR Context</h4>
                          <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold border border-emerald-200">
                            Merged
                          </span>
                        </div>

                        <div className="flex items-start gap-3 pb-3 border-b border-[#DAD7D7]/60">
                          <div className="w-8 h-8 rounded-full bg-[#121316] text-white flex items-center justify-center font-bold text-xs shrink-0 shadow-sm">
                            GH
                          </div>
                          <div>
                            <p className="font-bold text-xs text-black">PR #182</p>
                            <p className="text-[11px] text-black/70 leading-tight">feat: update payment service logic</p>
                            <p className="text-[10px] text-black/50 mt-0.5">by @sayak-code • 2 days ago</p>
                          </div>
                        </div>

                        <div className="space-y-2 py-3 text-xs border-b border-[#DAD7D7]/60">
                          <div className="flex justify-between">
                            <span className="text-black/60">Repository</span>
                            <span className="font-medium text-black">ecommerce</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-black/60">Branch</span>
                            <span className="font-medium text-black">feature/payment-v2 → main</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-black/60">Commit</span>
                            <span className="font-mono text-xs text-[#D35C07] font-semibold bg-orange-50 px-1.5 py-0.5 rounded border border-orange-200">a83f92c</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-black/60">Changed Files</span>
                            <span className="font-medium text-black">4 files (+142 / -38)</span>
                          </div>
                        </div>
                      </div>

                      {/* Interactive PR drawer trigger */}
                      <button 
                        onClick={() => setShowPrModal(true)}
                        className="w-full mt-3 py-2 px-3 rounded-xl bg-orange-50/80 hover:bg-orange-100 border border-orange-200/80 text-xs font-bold text-[#D35C07] flex items-center justify-between transition-colors cursor-pointer"
                      >
                        <span>View pull request details</span>
                        <span>→</span>
                      </button>
                    </div>

                  </div>

                  {/* Test Selection Results Table */}
                  <div className="card-new-glass p-5 rounded-2xl border border-[#DAD7D7]">
                    
                    {/* Header, Search & Action Button */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
                      <div>
                        <h4 className="font-inter font-bold text-[16px] text-black">
                          Test Selection Matrix
                        </h4>
                        <p className="text-xs text-black/50">Granular AI selection reasoning and execution confidence</p>
                      </div>

                      <div className="flex flex-wrap items-center gap-3">
                        <div className="relative">
                          <input
                            type="text"
                            placeholder="Filter tests by name or reason..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-56 sm:w-64 pl-8 pr-3 py-1.5 border border-[#DAD7D7] rounded-xl text-xs bg-white focus:outline-none focus:border-tm-orange shadow-sm"
                          />
                          <svg className="w-3.5 h-3.5 absolute left-2.5 top-2 text-black/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                          </svg>
                        </div>

                        <button 
                          onClick={handleDownloadReport}
                          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-[#DAD7D7] bg-white text-xs font-medium text-black hover:border-tm-orange hover:text-tm-orange transition-colors shadow-sm cursor-pointer"
                        >
                          <svg className="w-3.5 h-3.5 text-tm-orange" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                          </svg>
                          <span>Download Report</span>
                        </button>
                      </div>
                    </div>

                    {/* Interactive Tabs */}
                    <div className="flex flex-wrap items-center gap-2 mb-4">
                      <button
                        onClick={() => setActiveTab('selected')}
                        className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                          activeTab === 'selected'
                            ? 'bg-gradient-to-r from-[#FEB048] to-[#D35C07] text-black shadow-md'
                            : 'bg-white/80 text-black/70 hover:bg-white border border-[#DAD7D7]'
                        }`}
                      >
                        Selected Tests (1,532)
                      </button>
                      <button
                        onClick={() => setActiveTab('skipped')}
                        className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                          activeTab === 'skipped'
                            ? 'bg-gradient-to-r from-[#FEB048] to-[#D35C07] text-black shadow-md'
                            : 'bg-white/80 text-black/70 hover:bg-white border border-[#DAD7D7]'
                        }`}
                      >
                        Skipped Tests (3,950)
                      </button>
                      <button
                        onClick={() => setActiveTab('confidence')}
                        className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                          activeTab === 'confidence'
                            ? 'bg-gradient-to-r from-[#FEB048] to-[#D35C07] text-black shadow-md'
                            : 'bg-white/80 text-black/70 hover:bg-white border border-[#DAD7D7]'
                        }`}
                      >
                        Confidence Breakdown
                      </button>
                    </div>

                    {/* View based on Tab */}
                    {activeTab === 'confidence' ? (
                      <div className="p-6 rounded-xl bg-white border border-[#DAD7D7] space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <div className="p-4 rounded-xl bg-orange-50/70 border border-orange-200">
                            <span className="text-xs text-black/60">High Confidence (&gt;90%)</span>
                            <p className="font-bold text-2xl text-[#D35C07] mt-1">1,120 tests</p>
                            <p className="text-[11px] text-black/60 mt-0.5">Direct AST callgraph modification links</p>
                          </div>
                          <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200">
                            <span className="text-xs text-black/60">Medium Confidence (80-89%)</span>
                            <p className="font-bold text-2xl text-amber-800 mt-1">380 tests</p>
                            <p className="text-[11px] text-black/60 mt-0.5">Shared transitives & integration boundaries</p>
                          </div>
                          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                            <span className="text-xs text-black/60">Low Risk Tier (&lt;80%)</span>
                            <p className="font-bold text-2xl text-slate-800 mt-1">32 tests</p>
                            <p className="text-[11px] text-black/60 mt-0.5">Utility helper regressions</p>
                          </div>
                        </div>

                        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-emerald-500 text-white flex items-center justify-center font-bold text-sm">
                              ✓
                            </div>
                            <div>
                              <p className="font-bold text-xs text-emerald-950">Zero False Negatives Verification Passed</p>
                              <p className="text-[11px] text-emerald-800">No critical code paths were left unverified in PR #182.</p>
                            </div>
                          </div>
                          <button
                            onClick={handleRunSelectedTests}
                            className="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold cursor-pointer shadow-sm"
                          >
                            Run Confidence Suite
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div className="overflow-x-auto rounded-xl border border-[#DAD7D7] bg-white">
                        <table className="w-full text-left border-collapse text-xs">
                          <thead>
                            <tr className="bg-slate-50/80 text-black/60 uppercase font-bold text-[10px] tracking-wider border-b border-[#DAD7D7]">
                              <th className="py-3 px-4">Test Suite</th>
                              <th className="py-3 px-4">File Path</th>
                              <th className="py-3 px-4">Selection Rationale</th>
                              <th className="py-3 px-4">Confidence</th>
                              <th className="py-3 px-4 text-right">Status</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-[#DAD7D7]/50 text-black/80">
                            {filteredList.map((item, index) => (
                              <tr key={item.name} className={index % 2 === 1 ? 'bg-slate-50/40 hover:bg-orange-50/30' : 'bg-white hover:bg-orange-50/30'}>
                                <td className="py-3 px-4 font-semibold text-black flex items-center gap-2">
                                  <span className={`w-4 h-4 rounded-full flex items-center justify-center text-[10px] font-bold ${
                                    item.status === 'Selected' ? 'bg-[#D35C07] text-white' : 'bg-slate-300 text-slate-700'
                                  }`}>
                                    {item.status === 'Selected' ? '✓' : '—'}
                                  </span>
                                  {item.name}
                                </td>
                                <td className="py-3 px-4 font-mono text-[11px] text-black/60">
                                  {item.path}
                                </td>
                                <td className="py-3 px-4 text-black/75">
                                  {item.reason}
                                </td>
                                <td className="py-3 px-4 font-bold text-[#D35C07]">
                                  {item.confidence}%
                                </td>
                                <td className="py-3 px-4 text-right">
                                  <span
                                    className={`inline-block px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                                      item.status === 'Selected'
                                        ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                                        : 'bg-amber-50 text-amber-800 border-amber-200'
                                    }`}
                                  >
                                    {item.status}
                                  </span>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}

                  </div>

                  {/* Bottom 3 Cards Row */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
                    
                    {/* 1. Pipeline Timeline */}
                    <div className="card-new-glass p-5 rounded-2xl border border-[#DAD7D7]">
                      <h4 className="font-inter font-bold text-sm text-black mb-4">Pipeline Execution Timeline</h4>
                      <div className="relative pl-6 space-y-3.5 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-gradient-to-b before:from-[#FEB048] before:to-[#D35C07]">
                        {[
                          { title: 'PR Created (payment-v2)', time: '14:32:00' },
                          { title: 'QUBIS AST Code Analysis', time: '14:32:01' },
                          { title: 'AI Selection: 1,532 Tests', time: '14:32:02' },
                          { title: 'Test Execution in Parallel', time: '14:37:14' },
                          { title: 'Pipeline Passed (Saved 12m)', time: '14:37:15' },
                        ].map((step) => (
                          <div key={step.title} className="relative flex items-center justify-between text-xs">
                            <span className="absolute -left-6 top-1 w-2.5 h-2.5 rounded-full bg-[#D35C07] shadow-sm" />
                            <span className="font-semibold text-black">{step.title}</span>
                            <span className="text-black/50 text-[11px]">{step.time}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* 2. AI Analysis Summary */}
                    <div className="card-new-glass p-5 rounded-2xl border border-[#DAD7D7] flex flex-col justify-between">
                      <div>
                        <div className="flex items-center justify-between mb-3">
                          <h4 className="font-inter font-bold text-sm text-black">AI Reasoning Summary</h4>
                          <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold border border-emerald-200">
                            High Confidence
                          </span>
                        </div>
                        <ul className="text-xs text-black/75 space-y-2">
                          <li className="flex items-start gap-1.5">
                            <span className="text-[#16865D] font-bold">✓</span>
                            <span>Selected 1,532 tests based on modified AST dependency paths</span>
                          </li>
                          <li className="flex items-start gap-1.5">
                            <span className="text-[#16865D] font-bold">✓</span>
                            <span>Skipped 3,950 isolated suites (auth, tax, recommendations)</span>
                          </li>
                          <li className="flex items-start gap-1.5">
                            <span className="text-[#16865D] font-bold">✓</span>
                            <span>Zero false-negative rate verified against test coverage database</span>
                          </li>
                        </ul>
                      </div>
                      <div className="mt-4 p-2.5 rounded-xl bg-orange-50/80 border border-orange-200 text-xs font-bold text-[#D35C07] text-center">
                        ML Confidence Score: 91% (Safety Level A+)
                      </div>
                    </div>

                    {/* 3. Key Insights */}
                    <div className="card-new-glass p-5 rounded-2xl border border-[#DAD7D7] space-y-3.5">
                      <h4 className="font-inter font-bold text-sm text-black mb-3">Key Value Insights</h4>
                      <div className="flex items-start gap-3">
                        <div className="w-7 h-7 rounded-full bg-orange-100 text-[#D35C07] flex items-center justify-center font-bold text-xs shrink-0">
                          ↓
                        </div>
                        <div>
                          <p className="font-bold text-xs text-black">71% reduction in test execution time</p>
                          <p className="text-[11px] text-black/60">Saved 12m 48s compute time on this branch</p>
                        </div>
                      </div>
                      <div className="flex items-start gap-3">
                        <div className="w-7 h-7 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold text-xs shrink-0">
                          ✓
                        </div>
                        <div>
                          <p className="font-bold text-xs text-black">Zero critical regressions missed</p>
                          <p className="text-[11px] text-black/60">All high-risk areas covered with 100% precision</p>
                        </div>
                      </div>
                      <div className="flex items-start gap-3">
                        <div className="w-7 h-7 rounded-full bg-orange-100 text-[#D35C07] flex items-center justify-center font-bold text-xs shrink-0">
                          ⚡
                        </div>
                        <div>
                          <p className="font-bold text-xs text-black">Fast developer PR turnaround</p>
                          <p className="text-[11px] text-black/60">PR feedback returned in 5m instead of 18m</p>
                        </div>
                      </div>
                    </div>

                  </div>
                </>
              )}

              {/* SUBVIEW 2: Pipeline Reports */}
              {activeNav === 'Pipeline Reports' && (
                <div className="card-new-glass p-6 rounded-2xl border border-[#DAD7D7] space-y-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-bold text-xl text-black">Historical Pipeline Runs</h3>
                      <p className="text-xs text-black/60">Recent automated test selection jobs across repositories</p>
                    </div>
                    <button onClick={handleDownloadReport} className="btn-get-started px-4 py-2 rounded-full text-xs font-bold text-black">
                      Export All History (CSV)
                    </button>
                  </div>

                  <div className="overflow-x-auto rounded-xl border border-[#DAD7D7] bg-white">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-slate-50 text-black/60 font-bold uppercase text-[10px] border-b border-[#DAD7D7]">
                        <tr>
                          <th className="p-3">PR Run</th>
                          <th className="p-3">Branch</th>
                          <th className="p-3">Author</th>
                          <th className="p-3">Selected / Total</th>
                          <th className="p-3">CI Saved</th>
                          <th className="p-3">Status</th>
                          <th className="p-3">Timestamp</th>
                          <th className="p-3 text-right">Action</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-[#DAD7D7]/60">
                        {pastRuns.map((run) => (
                          <tr key={run.id} className="hover:bg-orange-50/30">
                            <td className="p-3 font-bold text-black">{run.id}</td>
                            <td className="p-3 font-mono text-[11px] text-black/70">{run.branch}</td>
                            <td className="p-3 text-black/70">{run.author}</td>
                            <td className="p-3 font-semibold">{run.selected} / {run.total}</td>
                            <td className="p-3 font-bold text-[#D35C07]">{run.saved}</td>
                            <td className="p-3">
                              <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 font-semibold text-[10px]">
                                {run.status}
                              </span>
                            </td>
                            <td className="p-3 text-black/50">{run.time}</td>
                            <td className="p-3 text-right">
                              <button 
                                onClick={() => {
                                  setActiveNav('Dashboard');
                                  if (showToast) showToast(`Loaded ${run.id} report details.`);
                                }}
                                className="px-2.5 py-1 rounded-lg bg-orange-100 hover:bg-orange-200 text-[#D35C07] font-semibold text-[11px] cursor-pointer"
                              >
                                View
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* SUBVIEW 3: Test Analytics */}
              {activeNav === 'Test Analytics' && (
                <div className="card-new-glass p-6 rounded-2xl border border-[#DAD7D7] space-y-6">
                  <div>
                    <h3 className="font-bold text-xl text-black">CI Test Analytics & Compute Efficiency</h3>
                    <p className="text-xs text-black/60">Aggregate data across 240+ CI pipeline executions this month</p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div className="p-4 rounded-xl bg-white border border-[#DAD7D7]">
                      <span className="text-xs text-black/60">Total Compute Hours Saved</span>
                      <p className="font-bold text-3xl text-[#D35C07] mt-1">142.5 hrs</p>
                      <p className="text-[11px] text-emerald-700 mt-1 font-semibold">~$1,850 cloud CI spend reduced</p>
                    </div>
                    <div className="p-4 rounded-xl bg-white border border-[#DAD7D7]">
                      <span className="text-xs text-black/60">Average PR Feedback Time</span>
                      <p className="font-bold text-3xl text-black mt-1">4m 18s</p>
                      <p className="text-[11px] text-black/60 mt-1">Down from 17m 45s without QUBIS</p>
                    </div>
                    <div className="p-4 rounded-xl bg-white border border-[#DAD7D7]">
                      <span className="text-xs text-black/60">Flaky Tests Quarantined</span>
                      <p className="font-bold text-3xl text-amber-600 mt-1">6 tests</p>
                      <p className="text-[11px] text-black/60 mt-1">Prevented false pipeline blockages</p>
                    </div>
                  </div>
                </div>
              )}

              {/* SUBVIEW 4: Model Performance */}
              {activeNav === 'Model Performance' && (
                <div className="card-new-glass p-6 rounded-2xl border border-[#DAD7D7] space-y-6">
                  <div>
                    <h3 className="font-bold text-xl text-black">QUBIS Model Telemetry & Accuracy</h3>
                    <p className="text-xs text-black/60">Trained on repository commit graphs and historic test pass/fail logs</p>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                    <div className="p-4 rounded-xl bg-white border border-[#DAD7D7] text-center">
                      <span className="text-xs text-black/60">Overall Accuracy</span>
                      <p className="font-bold text-3xl text-[#D35C07] mt-1">99.4%</p>
                    </div>
                    <div className="p-4 rounded-xl bg-white border border-[#DAD7D7] text-center">
                      <span className="text-xs text-black/60">Recall (Safety)</span>
                      <p className="font-bold text-3xl text-emerald-600 mt-1">100.0%</p>
                    </div>
                    <div className="p-4 rounded-xl bg-white border border-[#DAD7D7] text-center">
                      <span className="text-xs text-black/60">Precision</span>
                      <p className="font-bold text-3xl text-black mt-1">98.9%</p>
                    </div>
                    <div className="p-4 rounded-xl bg-white border border-[#DAD7D7] text-center">
                      <span className="text-xs text-black/60">False Negatives</span>
                      <p className="font-bold text-3xl text-emerald-600 mt-1">0.0%</p>
                    </div>
                  </div>
                </div>
              )}

              {/* SUBVIEW 5: Repositories */}
              {activeNav === 'Repositories' && (
                <div className="card-new-glass p-6 rounded-2xl border border-[#DAD7D7] space-y-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-bold text-xl text-black">Connected Repositories</h3>
                      <p className="text-xs text-black/60">GitHub and GitLab repositories with active QUBIS webhook integrations</p>
                    </div>
                    <button 
                      onClick={() => { if (showToast) showToast('Webhook connection wizard triggered.'); }}
                      className="btn-get-started px-4 py-2 rounded-full text-xs font-bold text-black"
                    >
                      + Connect New Repository
                    </button>
                  </div>

                  <div className="space-y-3">
                    {[
                      { name: 'ecommerce (active)', branch: 'main', framework: 'pytest / Django', status: 'Live & Healthy', webhooks: '214 runs' },
                      { name: 'auth-service', branch: 'main', framework: 'jest / Node.js', status: 'Live & Healthy', webhooks: '89 runs' },
                      { name: 'billing-gateway', branch: 'production', framework: 'go test', status: 'Live & Healthy', webhooks: '54 runs' },
                    ].map((repo) => (
                      <div key={repo.name} className="p-4 rounded-xl bg-white border border-[#DAD7D7] flex items-center justify-between">
                        <div>
                          <p className="font-bold text-sm text-black">{repo.name}</p>
                          <p className="text-xs text-black/60">{repo.framework} • Branch: {repo.branch}</p>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className="px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 font-semibold text-xs">
                            ● {repo.status}
                          </span>
                          <span className="text-xs text-black/50">{repo.webhooks}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* SUBVIEW 6: Settings */}
              {activeNav === 'Settings' && (
                <div className="card-new-glass p-6 rounded-2xl border border-[#DAD7D7] space-y-6">
                  <div>
                    <h3 className="font-bold text-xl text-black">QUBIS CI Selection Settings</h3>
                    <p className="text-xs text-black/60">Configure ML sensitivity thresholds, parallel runners, and alerts</p>
                  </div>

                  <div className="space-y-6 max-w-xl">
                    <div>
                      <div className="flex justify-between text-xs font-semibold mb-2">
                        <span>Confidence Threshold: {confidenceThreshold}%</span>
                        <span className="text-[#D35C07]">{confidenceThreshold >= 80 ? 'Balanced (Recommended)' : 'Aggressive'}</span>
                      </div>
                      <input
                        type="range"
                        min="60"
                        max="95"
                        value={confidenceThreshold}
                        onChange={(e) => setConfidenceThreshold(Number(e.target.value))}
                        className="w-full accent-tm-orange"
                      />
                      <p className="text-[11px] text-black/50 mt-1">Tests scored below this confidence will be safely included or skipped based on AST call depth.</p>
                    </div>

                    <div>
                      <label className="block text-xs font-semibold mb-1.5">Test Runner Engine</label>
                      <div className="flex gap-2">
                        {['pytest', 'jest', 'go test', 'mvn test'].map((runner) => (
                          <button
                            key={runner}
                            onClick={() => setSelectedRunner(runner)}
                            className={`px-3 py-1.5 rounded-lg text-xs font-semibold border cursor-pointer ${
                              selectedRunner === runner
                                ? 'bg-orange-50 border-tm-orange text-tm-orange'
                                : 'bg-white border-[#DAD7D7] text-black/70'
                            }`}
                          >
                            {runner}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="flex items-center justify-between p-3 rounded-xl bg-white border border-[#DAD7D7]">
                      <div>
                        <p className="text-xs font-semibold text-black">Slack & PR Comment Notifications</p>
                        <p className="text-[11px] text-black/60">Post execution summary directly to PR #182 thread</p>
                      </div>
                      <input
                        type="checkbox"
                        checked={slackAlerts}
                        onChange={(e) => setSlackAlerts(e.target.checked)}
                        className="w-4 h-4 accent-tm-orange cursor-pointer"
                      />
                    </div>

                    <button
                      onClick={() => {
                        if (showToast) showToast('Settings saved successfully.');
                      }}
                      className="btn-get-started px-6 py-2.5 rounded-full text-xs font-bold text-black cursor-pointer"
                    >
                      Save Configuration
                    </button>
                  </div>
                </div>
              )}

            </div>

          </div>

        </div>

      </div>

      {/* PR Details Modal */}
      {showPrModal && (
        <div 
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in"
          onClick={() => setShowPrModal(false)}
        >
          <div 
            className="relative w-full max-w-2xl p-6 sm:p-8 rounded-[24px] bg-white/95 backdrop-blur-xl border border-[#DAD7D7] shadow-2xl overflow-hidden max-h-[90vh] overflow-y-auto text-left"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setShowPrModal(false)}
              className="absolute top-4 right-4 w-8 h-8 rounded-full bg-slate-100 text-slate-500 hover:text-black flex items-center justify-center cursor-pointer"
            >
              ✕
            </button>

            <div className="flex items-center gap-2 mb-2">
              <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold border border-emerald-200">
                PR #182 • Merged
              </span>
              <span className="text-xs text-black/50">branch: feature/payment-v2</span>
            </div>

            <h3 className="font-inter font-bold text-xl text-black mb-2">
              feat: update payment service logic
            </h3>
            <p className="text-xs text-black/60 mb-4">
              Commit <code className="bg-slate-100 px-1.5 py-0.5 rounded font-mono text-[#D35C07]">a83f92c</code> by @sayak-code • 4 changed files (+142, -38)
            </p>

            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-orange-50/70 border border-orange-200/80">
                <h5 className="font-bold text-xs text-[#D35C07] mb-1">AI Test Selection Analysis</h5>
                <p className="text-xs text-black/80 leading-relaxed">
                  QUBIS inspected the Abstract Syntax Tree (AST) diff and identified modifications inside <code className="font-mono text-xs">process_card_payment()</code> and <code className="font-mono text-xs">verify_signature()</code>.
                  Only test suites that have callgraph connections to these entrypoints were selected. Isolated modules (auth, billing tax, inventory sync) have zero incoming graph edges and were safely bypassed, saving 71% CI execution duration.
                </p>
              </div>

              <div>
                <h5 className="font-bold text-xs text-black mb-2">Changed Files in this PR:</h5>
                <div className="space-y-2 text-xs font-mono">
                  <div className="p-2 rounded-lg bg-slate-50 border border-[#DAD7D7] flex items-center justify-between">
                    <span>services/payment_service.py</span>
                    <span className="text-emerald-700 font-bold">+88 / -20</span>
                  </div>
                  <div className="p-2 rounded-lg bg-slate-50 border border-[#DAD7D7] flex items-center justify-between">
                    <span>api/checkout_handler.py</span>
                    <span className="text-emerald-700 font-bold">+32 / -12</span>
                  </div>
                  <div className="p-2 rounded-lg bg-slate-50 border border-[#DAD7D7] flex items-center justify-between">
                    <span>models/order.py</span>
                    <span className="text-emerald-700 font-bold">+14 / -4</span>
                  </div>
                  <div className="p-2 rounded-lg bg-slate-50 border border-[#DAD7D7] flex items-center justify-between">
                    <span>utils/crypto.py</span>
                    <span className="text-emerald-700 font-bold">+8 / -2</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  onClick={handleDownloadReport}
                  className="px-4 py-2 rounded-full border border-[#DAD7D7] text-xs font-medium text-black hover:border-tm-orange"
                >
                  Download Pipeline JSON
                </button>
                <button
                  onClick={() => setShowPrModal(false)}
                  className="btn-get-started px-6 py-2 rounded-full text-xs font-bold text-black"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* GitHub Modal */}
      {showGithubModal && (
        <div 
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in"
          onClick={() => setShowGithubModal(false)}
        >
          <div 
            className="relative w-full max-w-lg p-6 rounded-[24px] bg-white/95 backdrop-blur-xl border border-[#DAD7D7] shadow-2xl text-left"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setShowGithubModal(false)}
              className="absolute top-4 right-4 w-8 h-8 rounded-full bg-slate-100 text-slate-500 hover:text-black flex items-center justify-center cursor-pointer"
            >
              ✕
            </button>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-[#121316] text-white flex items-center justify-center font-bold text-sm">
                GH
              </div>
              <div>
                <h4 className="font-bold text-base text-black">GitHub Repository: ecommerce</h4>
                <p className="text-xs text-black/60">Pull Request #182 Status</p>
              </div>
            </div>
            <p className="text-xs text-black/75 mb-4 leading-relaxed">
              QUBIS GitHub App is currently connected with webhook branch protection. All checks passed with 1,532 test assertions verified.
            </p>
            <div className="p-3 rounded-xl bg-slate-50 border border-[#DAD7D7] font-mono text-xs space-y-1 mb-4">
              <p className="text-emerald-700 font-bold">✓ qubis/test-selection — All 1,532 tests passed (5m 12s)</p>
              <p className="text-slate-600">✓ github/pr-lint — Clean syntax and typing</p>
              <p className="text-slate-600">✓ security/codeql — Zero vulnerabilities found</p>
            </div>
            <div className="flex items-center justify-end gap-3">
              <a
                href="https://github.com"
                target="_blank"
                rel="noreferrer"
                className="px-4 py-2 rounded-full border border-[#DAD7D7] text-xs font-semibold text-black hover:border-black"
              >
                Open in github.com ↗
              </a>
              <button
                onClick={() => setShowGithubModal(false)}
                className="btn-get-started px-5 py-2 rounded-full text-xs font-bold text-black"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
