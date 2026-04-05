// Function to extract visible text
function getVisibleText() {
    // Clone body to avoid modifying the actual page
    const clone = document.body.cloneNode(true);
    
    // Remove scripts, styles, and hidden elements
    const quietElements = clone.querySelectorAll('script, style, noscript, nav, footer, header, [aria-hidden="true"]');
    quietElements.forEach(el => el.remove());
    
    // Get text content
    let text = clone.innerText;
    
    // Basic cleanup
    text = text.replace(/\s+/g, ' ').trim();
    
    return text.substring(0, 15000); // Limit context size
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getPageContent") {
        const text = getVisibleText();
        sendResponse({ content: text });
    }
    return true; // Keep channel open for async response
});
