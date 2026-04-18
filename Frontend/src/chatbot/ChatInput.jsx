import React, { useState, useRef } from 'react';
import { Send, Trash2, Paperclip } from 'lucide-react';

const ChatInput = ({ onSend, onClear }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSend(input);
      setInput('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInput = (e) => {
    setInput(e.target.value);
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px';
    }
  };

  return (
    <div className="chatbot-input-container">
      <div className="chatbot-input-wrapper">
        <button
          type="button"
          className="chatbot-action-btn"
          title="Clear chat"
          onClick={onClear}
        >
          <Trash2 className="w-4 h-4" />
        </button>
        
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleInput}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          className="chatbot-textarea"
          rows="1"
        />
        
        <button
          type="button"
          onClick={handleSubmit}
          disabled={!input.trim()}
          className="chatbot-send-btn"
          title="Send message"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
      
      <div className="chatbot-footer-text">
        <p>Powered by Credify AI • Your data is secure</p>
      </div>
    </div>
  );
};

export default ChatInput;