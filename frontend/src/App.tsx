import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { AnalyzePage } from './pages/AnalyzePage';
import { InvestigationPage } from './pages/InvestigationPage';
import { AlertsPage } from './pages/AlertsPage';
import { CasesPage } from './pages/CasesPage';
import { AboutPage } from './pages/AboutPage';
import { DatasetGeneratorPage } from './pages/DatasetGeneratorPage';
import { DatasetExplorerPage } from './pages/DatasetExplorerPage';
import { JudgeDemoPage } from './pages/JudgeDemoPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <Routes>
            {/* 1. Public Landing Page at Root URL */}
            <Route path="/" element={<LandingPage />} />

            {/* 2. Public Investigator Login Route */}
            <Route path="/login" element={<LoginPage />} />

            {/* 3. Protected Application Routes (Requires Authentication) */}
            <Route
              path="/*"
              element={
                <ProtectedRoute>
                  <div className="flex flex-col min-h-screen bg-[#090d16] text-slate-100">
                    <Header />
                    <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
                      <Routes>
                        <Route path="/dashboard" element={<DashboardPage />} />
                        <Route path="/analyze" element={<AnalyzePage />} />
                        <Route path="/investigate/:subjectId?" element={<InvestigationPage />} />
                        <Route path="/alerts" element={<AlertsPage />} />
                        <Route path="/cases" element={<CasesPage />} />
                        <Route path="/dataset" element={<DatasetGeneratorPage />} />
                        <Route path="/generator" element={<DatasetGeneratorPage />} />
                        <Route path="/explorer" element={<DatasetExplorerPage />} />
                        <Route path="/judge-demo" element={<JudgeDemoPage />} />
                        <Route path="/about" element={<AboutPage />} />
                        {/* Fallback for unknown protected paths */}
                        <Route path="*" element={<Navigate to="/dashboard" replace />} />
                      </Routes>
                    </main>
                    <Footer />
                  </div>
                </ProtectedRoute>
              }
            />
          </Routes>
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  );
};

export default App;
