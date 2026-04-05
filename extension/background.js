const API_BASE_URL = "http://localhost:8000";

// 1. Authenticate and save tokens
async function loginUser(email, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    
    if (response.ok) {
      const data = await response.json();
      // Store JWTs in Chrome Local Storage
      await chrome.storage.local.set({ 
        access_token: data.access_token, 
        refresh_token: data.refresh_token 
      });
      console.log("Logged in successfully!");
      return data;
    } else {
      console.error("Login failed", await response.json());
      return null;
    }
  } catch (error) {
    console.error("Network error during login:", error);
  }
}

// Helper to reliably get the JWT token
async function getAccessToken() {
  return new Promise((resolve) => {
    chrome.storage.local.get(["access_token"], (result) => {
      resolve(result.access_token);
    });
  });
}

// 2. Make authenticated LLM query
async function queryLLM(promptText) {
  const token = await getAccessToken();
  if (!token) {
    console.error("No access token found. Please login first.");
    return null;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/llm/query`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt: promptText })
    });

    if (response.ok) {
      const data = await response.json();
      return data.response;
    } else if (response.status === 401) {
      console.warn("Token expired or unauthorized. Need to call /auth/refresh.");
    } else if (response.status === 429) {
      console.warn("Rate limit exceeded for the free tier.");
    }
    return null;
  } catch (error) {
    console.error("API error during LLM query:", error);
  }
}

// 3. Fetch token/request usage from protected route
async function fetchUsage() {
  const token = await getAccessToken();
  if (!token) return null;

  try {
    const response = await fetch(`${API_BASE_URL}/usage/`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log(`Usage today: ${data.request_count} requests, ${data.tokens_used} tokens`);
      return data;
    }
  } catch (error) {
    console.error("Error fetching usage stats:", error);
  }
}

// Listen for messages from popup.js or content.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "LOGIN") {
    loginUser(request.email, request.password).then(sendResponse);
    return true; // Keep message channel open for async response
  }
  
  if (request.action === "QUERY_LLM") {
    queryLLM(request.prompt).then(sendResponse);
    return true;
  }

  if (request.action === "GET_USAGE") {
    fetchUsage().then(sendResponse);
    return true;
  }
});
