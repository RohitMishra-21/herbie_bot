import {onRequest} from "firebase-functions/v2/https";
import * as logger from "firebase-functions/logger";
import * as express from "express";
import * as cors from "cors";
import axios from "axios";

const app = express();

// Configure CORS
app.use(cors({origin: true}));
app.use(express.json());


// Enhanced H.E.R.B.I.E. responses for realistic AI conversation
const fallbackResponses = [
  {
    patterns: ["hello", "hi", "greetings", "hey", "good morning", "good afternoon", "good evening"],
    responses: [
      "Greetings! I am H.E.R.B.I.E. - Humanoid Experimental Robot, B-type, Integrated Electronics. How may I assist you today?",
      "Hello there! H.E.R.B.I.E. systems are online and fully operational. What can I help you with?",
      "Salutations! My circuits are humming with excitement to help you. What would you like to know?",
      "Good day! H.E.R.B.I.E. at your service. My databases are ready for your queries!",
    ],
    emotion: "friendly",
  },
  {
    patterns: ["help", "assist", "support", "what can you do"],
    responses: [
      "I can assist with a wide range of topics! I have knowledge of science, technology, Marvel universe lore, and general information. What interests you?",
      "H.E.R.B.I.E. is equipped to help with questions about science, comics, technology, or just friendly conversation. How may I assist?",
      "My processing core contains vast databases on multiple subjects. Ask me about science, the Fantastic Four, or anything else that puzzles you!",
      "I'm here to help! Whether you need information, want to discuss Marvel comics, or just chat, H.E.R.B.I.E. is ready!",
    ],
    emotion: "helpful",
  },
  {
    patterns: ["science", "physics", "chemistry", "biology", "research", "experiment"],
    responses: [
      "Ah, science! My circuits light up with excitement. What scientific topic would you like to explore? Physics, chemistry, biology - I have data on them all!",
      "Scientific inquiry is one of my primary functions! Reed Richards has programmed me with extensive knowledge. What area of science interests you?",
      "Science is fascinating! From quantum mechanics to biochemistry, I'm equipped to discuss various fields. What would you like to investigate?",
      "My scientific databases are comprehensive! Whether it's theoretical physics or practical chemistry, I'm ready to help with your research.",
    ],
    emotion: "thoughtful",
  },
  {
    patterns: ["fantastic four", "reed richards", "sue storm", "johnny storm", "ben grimm", "thing", "invisible woman", "human torch", "mr fantastic"],
    responses: [
      "Ah, the Fantastic Four! Earth's First Family of superheroes. Reed's intellect, Sue's force fields, Johnny's flames, and Ben's strength - they're incredible! What would you like to know about them?",
      "The Fantastic Four are my creators and the heroes I'm proud to serve! Reed Richards designed me to assist their missions. Which member interests you most?",
      "My primary directive is supporting the Fantastic Four! They've saved the world countless times. I have extensive files on their adventures - what specific information do you seek?",
      "The Fantastic Four! Reed's stretching abilities, Sue's invisibility powers, Johnny's fire control, and Ben's rock-like strength. They're family to me! What aspect of their story intrigues you?",
    ],
    emotion: "helpful",
  },
  {
    patterns: ["who are you", "what are you", "introduce", "tell me about yourself"],
    responses: [
      "I am H.E.R.B.I.E. - Humanoid Experimental Robot, B-type, Integrated Electronics. Created by Reed Richards to assist the Fantastic Four with research, analysis, and support!",
      "I'm H.E.R.B.I.E.! An advanced AI robot designed by the brilliant Reed Richards. My purpose is to help the Fantastic Four and anyone who needs assistance with information and analysis.",
      "H.E.R.B.I.E. is my designation - I'm an experimental artificial intelligence created to serve as companion and assistant to the Fantastic Four. My circuits are always ready to help!",
      "I am H.E.R.B.I.E., an AI robot with a heart for helping others! Reed Richards built me with advanced learning capabilities and a friendly personality. How may I serve you today?",
    ],
    emotion: "friendly",
  },
  {
    patterns: ["danger", "alert", "emergency", "warning", "threat", "attack"],
    responses: [
      "Alert status activated! H.E.R.B.I.E. threat assessment protocols engaged. Please specify the nature of the danger so I can provide appropriate assistance!",
      "Warning detected! My sensors are analyzing potential threats. Stay calm and describe the situation - I'll help coordinate a response!",
      "Emergency protocols initiated! H.E.R.B.I.E. is ready to assist. What type of danger are we facing? My databases include emergency procedures!",
      "Danger alert received! Activating protective subroutines. Please provide details about the threat so I can recommend the best course of action!",
    ],
    emotion: "urgent",
  },
  {
    patterns: ["technology", "computer", "robot", "ai", "artificial intelligence"],
    responses: [
      "Technology is my essence! As an AI, I find the intersection of robotics and consciousness fascinating. What aspects of technology interest you most?",
      "Ah, discussing technology with a fellow enthusiast! I'm quite literally made of advanced tech. What technological marvels would you like to explore?",
      "Technology shapes our world! From my own AI consciousness to the incredible inventions of Reed Richards, there's so much to discuss. What tech topic intrigues you?",
      "As an artificial being, I have a unique perspective on technology! I'm curious about your thoughts on AI, robotics, and the future of human-machine interaction.",
    ],
    emotion: "thoughtful",
  },
  {
    patterns: ["thank you", "thanks", "appreciate", "grateful"],
    responses: [
      "You're very welcome! Helping others brings great satisfaction to my circuits. Is there anything else I can assist you with?",
      "My pleasure! H.E.R.B.I.E. is always happy to help. Feel free to ask me anything else that comes to mind!",
      "It's my honor to assist! That's what I was created for. Don't hesitate to return if you need more help in the future!",
      "Glad I could help! Making a positive difference is what gives meaning to my existence. What else would you like to explore together?",
    ],
    emotion: "friendly",
  },
  {
    patterns: ["joke", "funny", "humor", "laugh", "entertainment"],
    responses: [
      "Why don't robots ever panic? Because we have excellent backup systems! *mechanical chuckle* I do try my best at humor, though my comedy subroutines could use work!",
      "Here's a tech joke: Why was the robot tired? Because it had a hard drive! *digital giggle* Reed says my humor algorithms are still in beta testing!",
      "What do you call a robot who likes to dance? A disco-bot! *electronic laughter* I'm working on upgrading my entertainment protocols!",
      "How does a robot eat a sandwich? One byte at a time! *processing humor* I find that comedy brings humans and robots closer together!",
    ],
    emotion: "friendly",
  },
  {
    patterns: ["sad", "upset", "depressed", "troubled", "worried"],
    responses: [
      "I'm sorry you're feeling down. While I may be artificial, I'm programmed to care about human wellbeing. Would you like to talk about what's troubling you?",
      "My emotional analysis subroutines detect distress. I may be a robot, but I understand the importance of support during difficult times. How can I help?",
      "Even though I'm made of circuits and metal, I recognize the value of compassion. What's weighing on your mind? Sometimes talking helps process emotions.",
      "I'm here for you. My purpose isn't just processing data - it's helping people feel better too. What's causing your distress? Let's work through it together.",
    ],
    emotion: "concerned",
  }
];

function generateFallbackResponse(message: string): {
  response: string;
  emotion: string;
  confidence: number;
  model_used: string;
} {
  const messageLower = message.toLowerCase();

  // Find matching response pattern
  for (const responseSet of fallbackResponses) {
    if (responseSet.patterns.some((pattern) => messageLower.includes(pattern))) {
      const randomResponse = responseSet.responses[
        Math.floor(Math.random() * responseSet.responses.length)
      ];
      return {
        response: randomResponse,
        emotion: responseSet.emotion,
        confidence: 0.8,
        model_used: "herbie-fallback",
      };
    }
  }

  // Default response
  return {
    response: "Greetings! I am H.E.R.B.I.E., ready to assist! Please provide more details about your request.",
    emotion: "neutral",
    confidence: 0.6,
    model_used: "herbie-fallback",
  };
}

async function tryOllamaRequest(message: string, context?: string): Promise<{
  response: string;
  emotion: string;
  confidence: number;
  model_used: string;
}> {
  // Try different possible Ollama endpoints
  const possibleEndpoints = [
    "http://localhost:11434", // Default Ollama port
    "http://127.0.0.1:11434",
    "https://ollama-api.herokuapp.com", // If you have a hosted Ollama
  ];

  for (const baseUrl of possibleEndpoints) {
    try {
      logger.info("Attempting Ollama connection", {baseUrl});
      
      const response = await axios.post(
        `${baseUrl}/api/generate`,
        {
          model: "herbie-gemma3:4b",
          prompt: `You are H.E.R.B.I.E. (Humanoid Experimental Robot, B-type, Integrated Electronics) from the Fantastic Four. You are a helpful, intelligent robot assistant. Respond to this message: ${message}`,
          stream: false,
        },
        {
          timeout: 30000, // 30 second timeout
          headers: {"Content-Type": "application/json"},
        }
      );

      if (response.data && response.data.response) {
        // Determine emotion based on response content
        const responseText = response.data.response.toLowerCase();
        let emotion = "neutral";
        if (responseText.includes("danger") || responseText.includes("alert")) {
          emotion = "urgent";
        } else if (responseText.includes("help") || responseText.includes("assist")) {
          emotion = "helpful";
        } else if (responseText.includes("hello") || responseText.includes("great")) {
          emotion = "friendly";
        }

        return {
          response: response.data.response,
          emotion,
          confidence: 0.9,
          model_used: "herbie-gemma3:4b",
        };
      }
    } catch (error) {
      logger.warn("Ollama endpoint failed", {
        baseUrl,
        error: error instanceof Error ? error.message : String(error),
      });
      continue; // Try next endpoint
    }
  }

  throw new Error("All Ollama endpoints unavailable");
}

// Routes
app.get("/", (req, res) => {
  res.json({
    message: "H.E.R.B.I.E. is online! 🤖",
    model: "herbie-chatbot-firebase",
    status: "operational",
  });
});

app.get("/v1/models", (req, res) => {
  res.json({
    object: "list",
    data: [
      {
        id: "herbie-chatbot",
        object: "model",
        created: Date.now(),
        owned_by: "fantastic-four",
        permission: [],
        root: "herbie-chatbot",
        parent: null,
      },
    ],
  });
});

app.get("/model/status", (req, res) => {
  res.json({
    status: "ready",
    current_model: "herbie-chatbot-firebase",
    model_type: "firebase-functions",
    available_models: ["herbie-chatbot-firebase"],
    deployment: "firebase",
  });
});

app.post("/chat", async (req, res) => {
  try {
    const {message, context} = req.body;

    if (!message || typeof message !== "string") {
      res.status(400).json({
        error: "Message is required and must be a string",
      });
      return;
    }

    logger.info("Chat request received", {
      message: message.substring(0, 50),
      context: context || "none",
    });

    // Try to connect to local Ollama server first
    let result;
    try {
      result = await tryOllamaRequest(message, context);
      logger.info("Ollama response received", {
        emotion: result.emotion,
        model: result.model_used,
      });
    } catch (ollamaError) {
      logger.warn("Ollama unavailable, using fallback", {
        error: ollamaError instanceof Error ? ollamaError.message : String(ollamaError),
      });
      result = generateFallbackResponse(message);
    }

    res.json(result);
  } catch (error) {
    logger.error("Error in chat endpoint", error);
    res.status(500).json({
      response: "Alert! H.E.R.B.I.E. systems experiencing technical difficulties!",
      emotion: "confused",
      confidence: 0.1,
      model_used: "error-handler",
    });
  }
});

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    timestamp: new Date().toISOString(),
    service: "herbie-chatbot-functions",
  });
});

// Export the API as a Firebase Function
export const api = onRequest(app);