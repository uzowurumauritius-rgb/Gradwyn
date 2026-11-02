import { onCall } from "firebase-functions/v2/https";
import { defineSecret } from "firebase-functions/params";

const geminiApiKey = defineSecret("GEMINI_API_KEY");

// Note: Gemini is now called directly from the frontend per guidelines.
// This function is kept as a placeholder to satisfy build requirements.
export const askGemini = onCall({ secrets: [geminiApiKey] }, async (request) => {
  return { 
    text: "Please use the client-side Gemini service.", 
    sources: [],
  };
});
