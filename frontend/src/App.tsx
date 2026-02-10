import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

// definr the message
interface Message {
  id: number;
  text: string;
  sender: 'user' | 'ai';
  category?: string; // "Chameleon" color changing
}

export default function App() {
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { 
      id: 1, 
      text: "Hello! I am Chameleon. Ask me about Sports, Finance, or Tech, and I will adapt my brain to answer you.", 
      sender: 'ai' 
    }
  ]);
  
  // auto scroll to the buttom 
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(scrollToBottom, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    // 1. add user message
    const userMessage: Message = { id: Date.now(), text: input, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // 2. simulate AI response (connect Python later)
    setTimeout(() => {
      const aiResponse: Message = { 
        id: Date.now() + 1, 
        text: "I see you said: " + input + ". (I am currently a dummy UI, connect my brain next!)", 
        sender: 'ai' 
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    }, 1000);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleSend();
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white font-sans">
      
      {/* HEADER */}
      <header className="flex items-center justify-between p-6 bg-gray-800 border-b border-gray-700 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-tr from-purple-500 to-blue-500 rounded-lg">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl font-bold tracking-wide">Chameleon AI</h1>
        </div>
        <div className="text-sm text-gray-400">
          <span className="inline-block w-2 h-2 mr-2 bg-green-500 rounded-full animate-pulse"></span>
          Online
        </div>
      </header>

      {/* CHAT AREA */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg) => (
          <motion.div 
            key={msg.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex items-start max-w-[80%] gap-3 ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}>
              
              {/* Avatar */}
              <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 
                ${msg.sender === 'user' ? 'bg-blue-600' : 'bg-gray-700'}`}>
                {msg.sender === 'user' ? <User size={20} /> : <Bot size={20} />}
              </div>

              {/* Bubble */}
              <div className={`p-4 rounded-2xl shadow-md text-sm leading-relaxed
                ${msg.sender === 'user' 
                  ? 'bg-blue-600 text-white rounded-tr-none' 
                  : 'bg-gray-800 border border-gray-700 text-gray-200 rounded-tl-none'}`}>
                {msg.text}
              </div>

            </div>
          </motion.div>
        ))}
        
        {/* Loading Indicator */}
        {isLoading && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
            <div className="flex items-center gap-2 text-gray-500 text-sm ml-14">
              <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></span>
              <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:-.3s]"></span>
              <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:-.5s]"></span>
            </div>
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* INPUT AREA */}
      <div className="p-4 bg-gray-800 border-t border-gray-700">
        <div className="flex gap-4 max-w-4xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Ask about Sports, Finance, or Tech..."
            className="flex-1 bg-gray-900 text-white rounded-xl px-5 py-3 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          />
          <button
            onClick={handleSend}
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 rounded-xl flex items-center gap-2 transition-all shadow-lg active:scale-95"
          >
            <Send size={18} />
            <span className="hidden sm:inline">Send</span>
          </button>
        </div>
      </div>

    </div>
  );
}