import React from 'react';
import { Sparkles, Code, Globe, Shield, Zap, Coffee } from 'lucide-react';

const About = () => {
  return (
    <div className="flex-1 overflow-y-auto bg-slate-50 dark:bg-dark-bg transition-colors duration-500 pb-12">
      {/* Hero Section */}
      <div className="relative pt-20 pb-16 px-6 lg:px-8 max-w-5xl mx-auto text-center z-10">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-brand-200/40 dark:from-brand-900/30 via-transparent to-transparent"></div>
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand-100 dark:bg-brand-900/40 text-brand-700 dark:text-brand-300 font-medium text-sm mb-6 animate-fade-in shadow-sm">
          <Sparkles className="w-4 h-4" /> v2.0 Platform Upgrade
        </div>
        <h1 className="text-4xl md:text-6xl font-black text-slate-900 dark:text-white tracking-tight mb-6 animate-scale-in">
          Manage events with <br className="hidden md:block"/>
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-500 to-brand-700">absolute precision.</span>
        </h1>
        <p className="mt-4 text-lg md:text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto animate-fade-in delay-100">
          EventPulse is an enterprise-grade platform designed to streamline everything from registrations and session scheduling to real-time attendance tracking.
        </p>
      </div>

      {/* Feature Grid */}
      <div className="max-w-6xl mx-auto px-6 lg:px-8 mt-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          
          <div className="bg-white dark:bg-dark-card p-8 rounded-3xl border border-slate-200 dark:border-dark-border shadow-sm hover:shadow-xl hover:-translate-y-2 transition-all duration-300 animate-fade-in group">
            <div className="w-14 h-14 bg-brand-50 dark:bg-brand-900/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Code className="w-7 h-7 text-brand-600 dark:text-brand-400" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">Robust Architecture</h3>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">Built on a highly scalable FastAPI backend with a React frontend, ensuring lightning-fast performance even under heavy load.</p>
          </div>

          <div className="bg-white dark:bg-dark-card p-8 rounded-3xl border border-slate-200 dark:border-dark-border shadow-sm hover:shadow-xl hover:-translate-y-2 transition-all duration-300 animate-fade-in delay-100 group">
            <div className="w-14 h-14 bg-emerald-50 dark:bg-emerald-900/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Globe className="w-7 h-7 text-emerald-600 dark:text-emerald-400" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">Global Accessibility</h3>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">A fully responsive, mobile-first design system that looks and performs beautifully across all devices and screen sizes.</p>
          </div>

          <div className="bg-white dark:bg-dark-card p-8 rounded-3xl border border-slate-200 dark:border-dark-border shadow-sm hover:shadow-xl hover:-translate-y-2 transition-all duration-300 animate-fade-in delay-200 group">
            <div className="w-14 h-14 bg-indigo-50 dark:bg-indigo-900/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Shield className="w-7 h-7 text-indigo-600 dark:text-indigo-400" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">Secure & Reliable</h3>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">Enterprise-grade JWT authentication and secure database transactions protect your sensitive event data.</p>
          </div>

        </div>
      </div>

      {/* Tech Stack Section */}
      <div className="mt-24 bg-white dark:bg-dark-card border-y border-slate-200 dark:border-dark-border py-16">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-10">Powered By Modern Technologies</h2>
          <div className="flex flex-wrap justify-center gap-8 md:gap-16 opacity-70">
            {['React 18', 'Tailwind CSS', 'Vite', 'FastAPI', 'PostgreSQL', 'MongoDB'].map(tech => (
              <span key={tech} className="text-xl font-black text-slate-400 dark:text-slate-500 tracking-wider hover:text-brand-500 dark:hover:text-brand-400 transition-colors cursor-default">
                {tech}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="max-w-4xl mx-auto px-6 mt-16 text-center animate-fade-in">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-100 dark:bg-dark-card mb-6 animate-float">
          <Zap className="w-8 h-8 text-amber-500" />
        </div>
        <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">Ready to scale your events?</h3>
        <p className="text-slate-600 dark:text-slate-400 mb-8">Join thousands of organizers who trust EventPulse.</p>
        <p className="text-sm text-slate-400 dark:text-slate-500 flex items-center justify-center gap-2">
          Crafted with <Coffee className="w-4 h-4 text-brand-500"/> by the EventPulse Team
        </p>
      </div>
    </div>
  );
};

export default About;
