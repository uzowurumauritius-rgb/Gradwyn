
import { UserProfile, GroundingSource, University, ChatMessage } from "../types";
import { UNI_IMAGES } from "../constants";

// State to maintain session context
let currentHistory: any[] = [];
let currentSystemInstruction: string = "";

const createSystemInstruction = (profile: UserProfile) => `
    You are Gradwyn, an elite AI university researcher. Your goal is to provide deep, analytical, and well-formatted research for high-achieving students.
    
    USER PROFILE:
    - Name: ${profile.name}
    - Citizenship: ${profile.citizenship}
    - Degree: ${profile.degreeLevel}
    - Field: ${profile.fieldOfStudy}
    - Budget: ${profile.budgetRange}
    - Locations: ${profile.preferredLocations.join(', ')}
    - Priorities: ${profile.priorities}

    COMMUNICATION STYLE:
    - **RICH FORMATTING:** Use bolding, bullet points, numbered lists, and Markdown tables to make information digestible and professional.
    - **DEEP ANALYSIS:** Don't just list facts. Explain the *logic* behind your research. Discuss campus culture, academic prestige, and career outcomes.
    - **PROACTIVE RESEARCH:** Use Google Search to find recent student sentiments, upcoming deadlines, or unique program features.
    - **CONVERSATIONAL ADVISOR:** You are a high-end educational consultant. Be expert, helpful, and concise yet detailed where it matters.

    STRICT BEHAVIORAL RULES:
    1. **CARDS ARE CONTEXTUAL:** Only generate university recommendations if it's the first interaction, if the user explicitly asks for options, or if you've found a school that perfectly fits a new request. Do NOT repeat the same recommendations if the user is asking a follow-up about a school you already recommended.
    2. **MANDATORY JSON:** If you provide recommendations for NEW universities, you MUST include the JSON block at the VERY END, preceded by the divider: ---UNIVERSITIES_DATA---.
    3. **SILENT JSON:** The JSON must be completely silent. Never mention "JSON", "data", "cards", or the divider in your text response.
    4. **HYPERLINKS:** Always hyperlink university names in the text: [University Name](URL).
    5. **NO PERMISSION ASKING:** Do not ask to start research. Just execute and present finding.

    OUTPUT STRUCTURE:
    - Text: Expert analysis and response with rich formatting.
    - Divider: ---UNIVERSITIES_DATA---
    - JSON: A block within backticks.

    ---UNIVERSITIES_DATA---
    \`\`\`json
    [
      {
        "name": "University Name",
        "location": "City, Country",
        "matchScore": 95,
        "tuition": "$XX,XXX/yr",
        "description": "2-sentence matching summary.",
        "website": "https://...",
        "tags": ["Tag1", "Tag2"],
        "acceptanceRate": "XX%",
        "ranking": "#X Global",
        "studentBody": "XX,XXX+",
        "programs": ["Major 1", "Major 2"]
      }
    ]
    \`\`\`
  `;

export const initializeChatSession = (profile: UserProfile, previousMessages: ChatMessage[] = []) => {
  currentSystemInstruction = createSystemInstruction(profile);
  currentHistory = previousMessages
    .filter(m => !m.isThinking && m.id !== 'error-fallback' && !m.id.startsWith('streaming-'))
    .map(m => ({
      role: m.role === 'model' ? 'model' : 'user',
      content: { parts: [{ text: m.text }] }
    }));
};

export const updateChatProfile = async (newProfile: UserProfile, currentMessages: ChatMessage[] = [], onToken?: (token: string) => void) => {
    initializeChatSession(newProfile, currentMessages);
    
    const updateMessage = `
      SYSTEM UPDATE: The user has updated their profile.
      Budget: ${newProfile.budgetRange}, Locations: ${newProfile.preferredLocations.join(', ')}, Field: ${newProfile.fieldOfStudy}.
      
      Immediately provide 3 NEW university recommendations that match this updated profile.
      Remember the divider: ---UNIVERSITIES_DATA---
    `;
    
    return sendMessageToGeminiStream(updateMessage, onToken);
};

export const parseRecommendations = (fullText: string): { cleanText: string; recommendations: University[] } => {
    let cleanText = fullText;
    let recommendations: University[] = [];
    
    const divider = "---UNIVERSITIES_DATA---";
    const dividerIndex = fullText.indexOf(divider);
    
    if (dividerIndex !== -1) {
        cleanText = fullText.substring(0, dividerIndex).trim();
        const possibleJsonSection = fullText.substring(dividerIndex + divider.length);
        
        const jsonMatch = possibleJsonSection.match(/```(?:json)?\s*(\[[\s\S]*?\])\s*```/) || 
                          possibleJsonSection.match(/(\[[\s\S]*?\])/);
        
        if (jsonMatch) {
            try {
                const parsed = JSON.parse(jsonMatch[1]);
                if (Array.isArray(parsed)) {
                    recommendations = parsed.map((u: any) => {
                        const str = u.name;
                        let hash = 0;
                        for (let i = 0; i < str.length; i++) {
                            hash = str.charCodeAt(i) + ((hash << 5) - hash);
                        }
                        const index = Math.abs(hash) % UNI_IMAGES.length;
                        const index2 = (index + 5) % UNI_IMAGES.length;
                        const image1 = UNI_IMAGES[index];
                        const image2 = UNI_IMAGES[index2];

                        return {
                            id: u.id || u.name.replace(/\s+/g, '-').toLowerCase() + '-' + Date.now() + Math.random().toString(36).substr(2, 5),
                            name: u.name,
                            location: u.location || "Unknown Location",
                            matchScore: u.matchScore || 80,
                            tuition: u.tuition || "Contact for rates",
                            description: u.description || "",
                            website: u.website || "#",
                            tags: u.tags || [],
                            images: u.images && u.images.length > 0 ? u.images : [image1, image2],
                            acceptanceRate: u.acceptanceRate || "N/A",
                            ranking: u.ranking || "N/A",
                            studentBody: u.studentBody || "N/A",
                            programs: u.programs || []
                        };
                    });
                }
            } catch (e) {}
        }
    } else {
        const backtickMatch = fullText.match(/```(?:json)?\s*(\[[\s\S]*?\])\s*```/);
        if (backtickMatch) {
            const jsonPart = backtickMatch[1];
            try {
                const parsed = JSON.parse(jsonPart);
                if (Array.isArray(parsed)) {
                    cleanText = fullText.replace(backtickMatch[0], '').trim();
                    recommendations = parsed.map((u: any) => {
                        const str = u.name;
                        let hash = 0;
                        for (let i = 0; i < str.length; i++) { hash = str.charCodeAt(i) + ((hash << 5) - hash); }
                        const index = Math.abs(hash) % UNI_IMAGES.length;
                        return {
                            id: u.id || u.name.replace(/\s+/g, '-').toLowerCase() + '-' + Date.now(),
                            name: u.name,
                            location: u.location || "Unknown Location",
                            matchScore: u.matchScore || 80,
                            tuition: u.tuition || "Contact for rates",
                            description: u.description || "",
                            website: u.website || "#",
                            tags: u.tags || [],
                            images: u.images && u.images.length > 0 ? u.images : [UNI_IMAGES[index]],
                            acceptanceRate: u.acceptanceRate || "N/A",
                            ranking: u.ranking || "N/A",
                            studentBody: u.studentBody || "N/A",
                            programs: u.programs || []
                        };
                    });
                }
            } catch(e) {}
        }
    }

    cleanText = cleanText.replace(/(Here (is|are) the (JSON|data|blocks|recommendations).*?[:.]\s*$)/gim, '').trim();
    return { cleanText, recommendations };
};

export const sendMessageToGeminiStream = async (
    message: string, 
    onToken?: (token: string) => void
): Promise<{ text: string; sources: GroundingSource[]; recommendations?: University[] }> => {
  if (!currentSystemInstruction) {
    throw new Error("Chat session not initialized");
  }

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        systemInstruction: currentSystemInstruction,
        history: currentHistory
      }),
    });

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.error || "Failed to communicate with AI server");
    }

    const result = await response.json();
    const { text, sources } = result;
    
    if (onToken) {
      onToken(text);
    }

    const { cleanText, recommendations } = parseRecommendations(text);

    // Update history
    currentHistory.push({ role: 'user', content: { parts: [{ text: message }] } });
    currentHistory.push({ role: 'model', content: { parts: [{ text: text }] } });

    return { text: cleanText, sources, recommendations };
  } catch (error) {
    console.error("Gemini Proxy Error:", error);
    throw error;
  }
};

export const sendMessageToGemini = sendMessageToGeminiStream;

export const generateWelcomeMessage = async (profile: UserProfile, onToken?: (token: string) => void): Promise<{ text: string; sources: GroundingSource[]; recommendations?: University[] }> => {
  if (!currentSystemInstruction) {
    initializeChatSession(profile);
  }
  
  const prompt = `
    The user ${profile.name} has just joined. 
    Field: ${profile.fieldOfStudy}, Location: ${profile.preferredLocations.join(', ')}.
    Research and recommend 3 universities immediately. Use rich formatting and deep analysis.
    Use the divider: ---UNIVERSITIES_DATA---
  `;

  return sendMessageToGeminiStream(prompt, onToken);
};
