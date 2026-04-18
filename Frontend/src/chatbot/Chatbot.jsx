import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Minimize2, Bot, Send, Globe } from 'lucide-react';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [language, setLanguage] = useState('english');
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);

  const translations = {
    english: {
      title: 'Credify AI',
      online: 'Online',
      placeholder: 'Type your message...',
      quickRepliesLabel: 'Quick replies:',
      greeting: "Hello! I'm Credify AI Assistant. How can I help you today?",
      quickReplies: [
        'How to check credit score?',
        'What documents needed?',
        'How does it work?',
        'Help with registration'
      ],
      responses: {
        score: "To check your credit score, simply login and follow these steps:\n1) Give consent\n2) Select bank\n3) Verify with Aadhar & PAN\n4) Complete OTP verification.\nYour score will be ready in minutes!",
        document: "You'll need:\n• Valid Aadhar Card (12 digits)\n• PAN Card\n• Active bank account\n• Mobile number linked to email for OTP verification.",
        work: "Credify is an AI-powered credit scoring platform. You securely share your bank data and we instantly generate your credit score.",
        register: "To register:\n1) Click 'Login'\n2) Select 'User'\n3) Click 'Register'\n4) Fill name, email, 10-digit phone\n5) Create a strong password with letters and @_ symbols.",
        hello: "Hello! Welcome to Credify. I can help you with credit score queries, registration process, and general support. How may I assist you?",
        default: "I'm here to help! You can ask me about:\n• Credit score checking process\n• Required documents\n• Registration help\n• General queries\n\nFeel free to ask!"
      }
    },
    hindi: {
      title: 'क्रेडिफाई एआई',
      online: 'ऑनलाइन',
      placeholder: 'अपना संदेश लिखें...',
      quickRepliesLabel: 'त्वरित उत्तर:',
      greeting: "नमस्ते! मैं क्रेडिफाई एआई सहायक हूं। मैं आपकी कैसे मदद कर सकता हूं?",
      quickReplies: [
        'क्रेडिट स्कोर कैसे चेक करें?',
        'कौन से दस्तावेज़ चाहिए?',
        'यह कैसे काम करता है?',
        'पंजीकरण में मदद'
      ],
      responses: {
        score: "अपना क्रेडिट स्कोर चेक करने के लिए:\n1) लॉगिन करें\n2) सहमति दें\n3) बैंक चुनें\n4) आधार और पैन से सत्यापित करें\n5) ओटीपी सत्यापन पूरा करें।\nआपका स्कोर कुछ ही मिनटों में तैयार हो जाएगा!",
        document: "आपको चाहिए:\n• वैध आधार कार्ड (12 अंक)\n• पैन कार्ड\n• सक्रिय बैंक खाता\n• ओटीपी सत्यापन के लिए मोबाइल नंबर।",
        work: "क्रेडिफाई एक AI-संचालित क्रेडिट स्कोरिंग प्लेटफॉर्म है। आप अपना बैंक डेटा सुरक्षित रूप से शेयर करते हैं और हम तुरंत आपका क्रेडिट स्कोर जनरेट करते हैं।",
        register: "पंजीकरण के लिए:\n1) 'लॉगिन' पर क्लिक करें\n2) 'यूज़र' चुनें\n3) 'रजिस्टर' पर क्लिक करें\n4) नाम, ईमेल, 10-अंकों का फोन भरें\n5) अक्षरों और @_ प्रतीकों के साथ मजबूत पासवर्ड बनाएं।",
        hello: "नमस्ते! क्रेडिफाई में आपका स्वागत है। मैं क्रेडिट स्कोर प्रश्न, पंजीकरण प्रक्रिया और सामान्य सहायता में मदद कर सकता हूं। मैं आपकी कैसे सहायता कर सकता हूं?",
        default: "मैं यहां मदद के लिए हूं! आप मुझसे पूछ सकते हैं:\n• क्रेडिट स्कोर चेकिंग प्रक्रिया\n• आवश्यक दस्तावेज़\n• पंजीकरण सहायता\n• सामान्य प्रश्न\n\nबेझिझक पूछें!"
      }
    }
  };

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setMessages([{
        id: 1,
        text: translations[language].greeting,
        sender: 'bot',
        timestamp: new Date()
      }]);
    }
  }, [isOpen, language]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const getBotResponse = (userMessage) => {
    const msg = userMessage.toLowerCase();
    const responses = translations[language].responses;

    if (msg.includes('credit score') || msg.includes('score') || msg.includes('स्कोर')) {
      return responses.score;
    } else if (msg.includes('document') || msg.includes('need') || msg.includes('दस्तावेज़')) {
      return responses.document;
    } else if (msg.includes('work') || msg.includes('काम')) {
      return responses.work;
    } else if (msg.includes('register') || msg.includes('signup') || msg.includes('पंजीकरण')) {
      return responses.register;
    } else if (msg.includes('hello') || msg.includes('hi') || msg.includes('नमस्ते')) {
      return responses.hello;
    } else {
      return responses.default;
    }
  };

  const handleSend = () => {
    if (!inputText.trim()) return;
    const userMessage = { id: Date.now(), text: inputText, sender: 'user', timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInputText('');

    setTimeout(() => {
      const botMessage = {
        id: Date.now() + 1,
        text: getBotResponse(inputText),
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
    }, 1000);
  };

  const handleQuickReply = (reply) => {
    const userMessage = { id: Date.now(), text: reply, sender: 'user', timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);

    setTimeout(() => {
      const botMessage = {
        id: Date.now() + 1,
        text: getBotResponse(reply),
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
    }, 1000);
  };

  const toggleLanguage = () => {
    const newLanguage = language === 'english' ? 'hindi' : 'english';
    setLanguage(newLanguage);
    
    // Reset conversation with new language greeting
    setMessages([{
      id: Date.now(),
      text: translations[newLanguage].greeting,
      sender: 'bot',
      timestamp: new Date()
    }]);
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 w-20 h-20 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-full shadow-2xl hover:shadow-3xl transition-all transform hover:scale-110 flex items-center justify-center z-50 group"
        style={{ 
          boxShadow: '0 10px 40px rgba(59, 130, 246, 0.6), 0 0 20px rgba(99, 102, 241, 0.4)'
        }}
      >
        <div className="absolute inset-0 rounded-full bg-blue-400 animate-ping opacity-20"></div>
        <MessageCircle className="w-10 h-10 text-white relative z-10 group-hover:rotate-12 transition-transform" />
        <span className="absolute -top-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-white">
          <span className="absolute inset-0 bg-green-400 rounded-full animate-ping"></span>
        </span>
      </button>
    );
  }

  return (
    <div className={`fixed bottom-4 right-4 w-96 bg-white rounded-3xl shadow-2xl z-50 flex flex-col transition-all border-2 border-blue-300 ${isMinimized ? 'h-16' : 'h-[600px]'}`}
         style={{ boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3), 0 0 30px rgba(59, 130, 246, 0.2)' }}>
      
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-800 p-4 rounded-t-3xl flex items-center justify-between relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-32 h-32 bg-white rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-0 right-0 w-40 h-40 bg-white rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        </div>

        <div className="flex items-center space-x-3 relative z-10">
          <div className="w-12 h-12 bg-gradient-to-br from-white to-blue-100 rounded-full flex items-center justify-center relative shadow-lg">
            <Bot className="w-7 h-7 text-blue-600 animate-pulse" />
            <span className="absolute -bottom-0.5 -right-0.5 w-4 h-4 bg-green-500 rounded-full border-2 border-white">
              <span className="absolute inset-0 bg-green-400 rounded-full animate-ping"></span>
            </span>
          </div>
          <div>
            <h3 className="font-bold text-white text-lg">{translations[language].title}</h3>
            <p className="text-xs text-green-200 flex items-center font-semibold">
              <span className="w-2 h-2 bg-green-400 rounded-full mr-1.5 animate-pulse shadow-lg shadow-green-400/50"></span>
              {translations[language].online}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 relative z-10">
          <button 
            onClick={toggleLanguage}
            className="text-white hover:bg-white/20 p-2 rounded-xl transition-all backdrop-blur-sm bg-white/10 group relative"
            title={language === 'english' ? 'हिंदी में बदलें' : 'Switch to English'}
          >
            <Globe className="w-5 h-5 group-hover:rotate-180 transition-transform duration-500" />
            <div className="absolute -bottom-8 right-0 bg-slate-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
              {language === 'english' ? 'हिंदी' : 'English'}
            </div>
          </button>
          <button 
            onClick={() => setIsMinimized(!isMinimized)} 
            className="text-white hover:bg-white/20 p-2 rounded-xl transition-all backdrop-blur-sm bg-white/10"
          >
            <Minimize2 className="w-4 h-4" />
          </button>
          <button 
            onClick={() => setIsOpen(false)} 
            className="text-white hover:bg-white/20 p-2 rounded-xl transition-all backdrop-blur-sm bg-white/10 hover:rotate-90"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {!isMinimized && (
        <>
          {/* Messages Area with Background Image */}
          <div 
            className="flex-1 overflow-y-auto p-4 space-y-4 relative"
            style={{
              backgroundImage: 'url(https://i.pinimg.com/736x/d1/75/a2/d175a2ca475c97f99f8c03178ab7e3af.jpg)',
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              backgroundRepeat: 'no-repeat'
            }}
          >
            {/* Blur overlay */}
            <div className="absolute inset-0 backdrop-blur-md bg-white/40"></div>
            
            {/* Messages */}
            <div className="relative z-10 space-y-4">
              {messages.map((msg) => (
                <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
                  <div className={`max-w-[80%] ${
                    msg.sender === 'user' 
                      ? 'bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-700 text-white shadow-xl' 
                      : 'bg-white/95 text-gray-900 shadow-xl border-2 border-blue-200'
                  } rounded-2xl p-4 backdrop-blur-sm`}>
                    <p className="text-sm font-bold whitespace-pre-line leading-relaxed">{msg.text}</p>
                    <p className={`text-xs mt-2 font-semibold ${msg.sender === 'user' ? 'text-blue-200' : 'text-gray-600'}`}>
                      {msg.timestamp.toLocaleTimeString(language === 'hindi' ? 'hi-IN' : 'en-US', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </p>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Quick Replies */}
          {messages.length === 1 && (
            <div className="px-4 pb-3 bg-gradient-to-r from-blue-50 to-indigo-50 relative z-10">
              <p className="text-xs font-bold text-gray-700 mb-2">{translations[language].quickRepliesLabel}</p>
              <div className="flex flex-wrap gap-2">
                {translations[language].quickReplies.map((reply, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleQuickReply(reply)}
                    className="text-xs font-bold bg-gradient-to-br from-blue-100 via-blue-200 to-indigo-200 hover:from-blue-200 hover:via-blue-300 hover:to-indigo-300 text-blue-900 border-2 border-blue-300 hover:border-blue-400 px-3 py-2 rounded-xl transition-all transform hover:scale-105 hover:-translate-y-1 shadow-md hover:shadow-xl"
                  >
                    {reply}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input Area */}
          <div className="p-4 border-t-2 border-blue-100 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-b-3xl">
            <div className="flex space-x-2">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder={translations[language].placeholder}
                className="flex-1 px-4 py-3 border-2 border-blue-200 rounded-xl focus:border-blue-500 focus:outline-none text-sm font-semibold bg-white focus:shadow-lg transition-all placeholder:text-gray-400"
              />
              <button 
                onClick={handleSend} 
                disabled={!inputText.trim()}
                className="bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-700 hover:from-blue-700 hover:via-blue-800 hover:to-indigo-800 disabled:from-gray-300 disabled:to-gray-400 text-white p-3 rounded-xl transition-all transform hover:scale-110 active:scale-95 disabled:transform-none disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
                style={{ boxShadow: '0 4px 15px rgba(59, 130, 246, 0.4)' }}
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            
            <div className="text-center mt-2">
              <p className="text-xs font-bold text-gray-600">
                {language === 'english' ? 'Powered by Credify AI' : 'क्रेडिफाई एआई द्वारा संचालित'}
              </p>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Chatbot;