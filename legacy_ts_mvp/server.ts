import express from "express";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { GoogleGenerativeAI } from "@google/generative-ai";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // Health check for Cloud Run / Load Balancers
  app.get("/api/health", (req, res) => {
    res.json({ status: "ok", timestamp: new Date().toISOString() });
  });

  // Safe Gemini API endpoint
  app.post("/api/chat", async (req, res) => {
    try {
      const { message, systemInstruction, history } = req.body;
      const apiKey = process.env.GEMINI_API_KEY;

      if (!apiKey) {
        return res.status(500).json({ error: "GEMINI_API_KEY is not configured on the server." });
      }

      const genAI = new GoogleGenerativeAI(apiKey);
      const model = genAI.getGenerativeModel({ 
        model: "gemini-2.0-flash",
        systemInstruction: systemInstruction 
      });

      // Start chat with history
      const chat = model.startChat({
        history: (history || []).map((h: any) => ({
          role: h.role === 'model' ? 'model' : 'user',
          parts: [{ text: h.content?.parts?.[0]?.text || h.parts?.[0]?.text || "" }]
        })),
        tools: [{ googleSearch: {} }] as any
      });

      const result = await chat.sendMessage(message);
      const response = await result.response;
      const text = response.text();

      // Extract sources from grounding metadata if present
      const sources = [];
      const metadata = response.candidates?.[0]?.groundingMetadata;
      if (metadata?.groundingChunks) {
          for (const chunk of metadata.groundingChunks) {
              if (chunk.web) {
                  sources.push({
                      title: chunk.web.title,
                      uri: chunk.web.uri
                  });
              }
          }
      }

      res.json({ text, sources });
    } catch (error: any) {
      console.error("AI Error:", error);
      res.status(500).json({ error: error.message });
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const { createServer: createViteServer } = await import("vite");
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    // Robust static file serving for production
    const distPath = path.resolve(__dirname, 'dist');
    app.use(express.static(distPath));
    
    // Explicitly handle index.html for the root
    app.get("/", (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });

    // Catch-all for SPA routing
    app.get("*all", (req, res) => {
      // Avoid catching API routes or static files that should have been handled
      if (req.url.startsWith('/api')) {
          return res.status(404).json({ error: "API route not found" });
      }
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
