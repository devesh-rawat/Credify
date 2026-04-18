const responses = {
  greeting: [
    "Hello! Welcome to Credify. How can I assist you today?",
    "Hi there! I'm here to help you with your credit and loan queries.",
    "Welcome! What would you like to know about Credify?"
  ],
  
  whatIsCredify: "Credify is an AI-powered income verification and credit scoring platform. We help lenders instantly verify income and assess creditworthiness for people without traditional credit history. We use digital footprints like UPI transactions, utility payments, and behavioral data to create trust scores.",
  
  howItWorks: "Credify works in 4 simple steps:\n\n1️⃣ User Consent: Link your financial data securely\n2️⃣ Data Extraction: We analyze UPI, wallet, and bill payments\n3️⃣ AI Scoring: Our AI generates your Trust Score (0-100)\n4️⃣ Decision: Lenders get instant approval recommendations\n\nThe entire process takes just 2 minutes!",
  
  trustScore: "Your Trust Score is an AI-generated creditworthiness rating from 0-100. It's calculated using:\n\n• Income consistency from UPI/wallet data\n• Bill payment history\n• Digital behavior patterns\n• Transaction frequency and amounts\n\nScores above 75 are excellent, 60-75 are good, and below 60 need improvement.",
  
  applyLoan: "To apply for a loan:\n\n1. Click 'Register' to create an account\n2. Complete income verification by linking UPI/wallet\n3. Get your Trust Score instantly\n4. Submit loan application with desired amount\n5. Get approval decision in 2-3 minutes!\n\nWould you like me to guide you to the registration page?",
  
  eligibility: "You're eligible for a Credify loan if you:\n\n✅ Are 18 years or older\n✅ Have active UPI/digital wallet usage\n✅ Have regular income (formal or informal)\n✅ Pay utility bills regularly\n\nNo CIBIL score needed! We verify your income digitally.",
  
  security: "Your data security is our top priority:\n\n🔒 Bank-grade 256-bit encryption\n🔒 DPDP & GDPR compliant\n🔒 RBI guidelines adherent\n🔒 No data stored without consent\n🔒 Anonymized data processing\n\nWe never share your data with third parties without permission.",
  
  lenderBenefits: "For Lenders, Credify offers:\n\n📈 +25% approval rate improvement\n📉 -15% default rate reduction\n⚡ 2-minute decision time (vs 2 days)\n💰 40% lower verification costs\n🎯 87% accuracy in income verification\n📊 Real-time dashboard & API access",
  
  fees: "Credify pricing:\n\n👤 For Borrowers: FREE verification & scoring\n🏦 For Lenders: Pay-per-use API model\n   • ₹10 per verification\n   • ₹50 per full credit report\n   • Volume discounts available\n\nNo hidden charges or subscription fees!",
  
  contact: "You can reach us:\n\n📧 Email: support@credify.ai\n📞 Phone: +91-9876543210\n🌐 Website: https://credify.ai\n💬 Live chat: Right here!\n\nOur support team is available 24/7."
};

// Keywords mapping for intent detection
const intentKeywords = {
  greeting: ['hi', 'hello', 'hey', 'good morning', 'good evening', 'namaste', 'start'],
  whatIsCredify: ['what is credify', 'about credify', 'tell me about', 'what do you do', 'credify meaning'],
  howItWorks: ['how does it work', 'how credify works', 'process', 'steps', 'workflow', 'procedure'],
  trustScore: ['trust score', 'credit score', 'scoring', 'rating', 'how is score calculated', 'score meaning'],
  applyLoan: ['apply loan', 'get loan', 'loan application', 'apply for credit', 'need loan', 'want loan'],
  eligibility: ['eligible', 'eligibility', 'qualify', 'who can apply', 'requirements', 'criteria'],
  security: ['security', 'safe', 'secure', 'privacy', 'data protection', 'encryption'],
  lenderBenefits: ['lender benefits', 'for lenders', 'why lenders', 'lender advantage', 'nbfc'],
  fees: ['fee', 'cost', 'price', 'charges', 'how much', 'pricing', 'payment'],
  contact: ['contact', 'reach you', 'phone number', 'email', 'support', 'help desk']
};

// Detect intent from user message
const detectIntent = (message) => {
  const lowerMessage = message.toLowerCase();
  
  for (const [intent, keywords] of Object.entries(intentKeywords)) {
    if (keywords.some(keyword => lowerMessage.includes(keyword))) {
      return intent;
    }
  }
  
  return 'default';
};

// Get chatbot response
export const getChatbotResponse = async (userMessage) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  const intent = detectIntent(userMessage);
  
  if (intent === 'greeting') {
    return responses.greeting[Math.floor(Math.random() * responses.greeting.length)];
  }
  
  if (intent in responses) {
    return responses[intent];
  }
  
  // Default response for unrecognized queries
  return "I'm here to help! I can answer questions about:\n\n• What Credify is and how it works\n• Trust Score calculation\n• Loan applications and eligibility\n• Data security and privacy\n• Benefits for lenders\n• Pricing and fees\n• Contact information\n\nWhat would you like to know?";
};

// Get quick reply suggestions
export const getQuickReplies = () => {
  return [
    "What is Credify?",
    "How does it work?",
    "Apply for loan",
    "Check eligibility",
    "Is my data safe?"
  ];
};

// Advanced: If you want to integrate with a real AI API (Claude, OpenAI, etc.)
export const getAIChatbotResponse = async (userMessage, conversationHistory = []) => {
  try {
    // Example with Anthropic Claude API
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Note: In production, use environment variables for API keys
        // 'x-api-key': import.meta.env.VITE_ANTHROPIC_API_KEY,
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 500,
        system: `You are a helpful AI assistant for Credify, an AI-powered credit scoring platform. 
        
Key information about Credify:
- Helps credit-invisible users get loans through AI-powered income verification
- Uses UPI, wallet data, and digital behavior to create Trust Scores
- 87% accuracy, 2-minute decisions, RBI compliant
- For borrowers: Free. For lenders: Pay-per-use API
- Trust Score range: 0-100 (75+ excellent, 60-75 good, <60 needs improvement)

Be friendly, concise, and helpful. Guide users to register or contact support when needed.`,
        messages: [
          ...conversationHistory,
          { role: 'user', content: userMessage }
        ]
      })
    });

    const data = await response.json();
    return data.content[0].text;
  } catch (error) {
    console.error('AI API Error:', error);
    // Fallback to rule-based response
    return getChatbotResponse(userMessage);
  }
};