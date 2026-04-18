import React from 'react';
import { Bot, User } from 'lucide-react';

const ChatMessage = ({ message }) => {
  const isBot = message.sender === 'bot';
  
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className={`flex items-start gap-2 mb-4 ${!isBot ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div className={`chatbot-avatar-small ${isBot ? 'bg-blue-100' : 'bg-orange-100'}`}>
        {isBot ? (
          <Bot className="w-4 h-4 text-blue-600" />
        ) : (
          <User className="w-4 h-4 text-orange-600" />
        )}
      </div>

      {/* Message Bubble */}
      <div className={`flex flex-col ${!isBot ? 'items-end' : ''}`}>
        <div
          className={`chatbot-message ${
            isBot ? 'chatbot-message-bot' : 'chatbot-message-user'
          }`}
        >
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
        </div>
        <span className="text-xs text-slate-400 mt-1 px-1">
          {formatTime(message.timestamp)}
        </span>
      </div>
    </div>
  );
};

export default ChatMessage;