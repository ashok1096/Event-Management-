import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, X, Send, User } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: "Hi there! 👋 How can we help you with EventPulse today?", sender: 'bot', time: new Date() }
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const { user } = useAuth();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMsg = { id: Date.now(), text: input, sender: 'user', time: new Date() };
    setMessages([...messages, newMsg]);
    setInput('');

    // Simulate bot response
    setTimeout(() => {
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: "Thanks for reaching out! Our support team will get back to you shortly. For immediate assistance with APIs or dashboard configuration, please check the documentation.",
        sender: 'bot',
        time: new Date()
      }]);
    }, 1000);
  };

  return (
    <>
      {/* Chat Button */}
      <button
        onClick={() => setIsOpen(true)}
        className={`fixed bottom-6 right-6 p-4 rounded-full bg-brand-600 text-white shadow-xl shadow-brand-500/30 hover:bg-brand-500 hover:scale-105 transition-all duration-300 z-40 ${isOpen ? 'scale-0 opacity-0' : 'scale-100 opacity-100 animate-fade-in'}`}
      >
        <MessageCircle className="w-6 h-6" />
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-[350px] h-[500px] bg-white dark:bg-dark-card rounded-2xl shadow-2xl border border-slate-200 dark:border-dark-border flex flex-col z-50 animate-slide-up overflow-hidden">
          {/* Header */}
          <div className="p-4 bg-brand-600 text-white flex justify-between items-center shadow-md z-10">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center backdrop-blur-sm">
                <MessageCircle className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="font-bold text-sm">EventPulse Support</h3>
                <p className="text-xs text-brand-100 flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-green-400"></span> Online
                </p>
              </div>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-white/80 hover:text-white transition-colors p-1 rounded-lg hover:bg-white/10">
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto bg-slate-50 dark:bg-dark-bg space-y-4">
            {messages.map(msg => (
              <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                {msg.sender === 'bot' && (
                  <div className="w-8 h-8 rounded-full bg-brand-100 dark:bg-brand-900/50 flex items-center justify-center mr-2 flex-shrink-0">
                    <ZapIcon className="w-4 h-4 text-brand-600 dark:text-brand-400" />
                  </div>
                )}
                <div className={`max-w-[75%] rounded-2xl p-3 text-sm ${
                  msg.sender === 'user' 
                    ? 'bg-brand-600 text-white rounded-tr-sm shadow-md' 
                    : 'bg-white dark:bg-dark-card text-slate-800 dark:text-dark-text rounded-tl-sm shadow-sm border border-slate-100 dark:border-dark-border'
                }`}>
                  <p className="leading-relaxed">{msg.text}</p>
                  <p className={`text-[10px] mt-1 text-right ${msg.sender === 'user' ? 'text-brand-200' : 'text-slate-400 dark:text-slate-500'}`}>
                    {msg.time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 bg-white dark:bg-dark-card border-t border-slate-200 dark:border-dark-border">
            <form onSubmit={handleSend} className="relative flex items-center">
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder="Type your message..."
                className="w-full pl-4 pr-12 py-3 bg-slate-100 dark:bg-dark-bg border-none rounded-xl text-sm focus:ring-2 focus:ring-brand-500 outline-none text-slate-800 dark:text-dark-text placeholder:text-slate-500 dark:placeholder:text-slate-400 transition-all"
              />
              <button 
                type="submit"
                disabled={!input.trim()}
                className="absolute right-2 p-2 bg-brand-600 text-white rounded-lg hover:bg-brand-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
};

// Mini Zap Icon for bot
const ZapIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
  </svg>
);

export default ChatWidget;
