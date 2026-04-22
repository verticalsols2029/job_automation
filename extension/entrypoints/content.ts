export default defineContentScript({
  matches: ['*://*.greenhouse.io/*'],
  allFrames: true,
  main() {
    browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
      if (message.action === 'SCAN_FIELDS') {
        console.log("✅ Scanning fields...");
        const schema = scanAndCleanFields();
        console.log("📊 Extracted Schema:", schema);
        sendResponse({ success: true, data: schema });
      } 
      else if (message.action === 'FILL_FORM') {
        console.log("✅ Filling form...");
        fillForm(message.data);
        sendResponse({ success: true });
      }
    });
  },
});

function scanAndCleanFields() {
  const fields = document.querySelectorAll(
    'input:not([type="hidden"]):not([type="submit"]):not([type="button"]), textarea, select'
  ) as NodeListOf<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>;

  const rawSchema: any[] = [];

  // 1. THE HIJACK: Grab all script data on the page
  // This ensures we catch the JSON whether Greenhouse uses Next.js, Remix, or raw React state.
  const allScripts = Array.from(document.querySelectorAll('script'))
    .map(script => script.textContent || "")
    .join(" ");

  fields.forEach((field, index) => {
    const closestLabel = field.closest('label')?.textContent?.trim();
    const explicitLabel = field.id ? document.querySelector(`label[for="${field.id}"]`)?.textContent?.trim() : null;

    let options = undefined;

    // 2a. Standard HTML Dropdowns (Country lists often still use this)
    if (field.tagName === 'SELECT') {
      options = Array.from((field as HTMLSelectElement).options)
        .map(opt => ({ value: opt.value, text: opt.text.trim() }))
        .filter(opt => opt.value !== "" && opt.text.toLowerCase() !== "select...");
    } 
    // 2b. React Custom Dropdowns (The Hydration Hunt)
    else if (field.tagName === 'INPUT') {
      const targetId = field.id; 
      
      // Greenhouse IDs are usually "question_12345" or just "12345"
      const numericIdMatch = targetId.match(/\d+/);
      
      if (numericIdMatch) {
        const numericId = numericIdMatch[0];
        
        // Regex hunt: Look for the exact field ID, followed by its "choices" array
        // We use [^]*? to safely jump over other JSON keys without skipping to a different question
        const searchRegex = new RegExp(`"id":\\s*${numericId}[^]*?"choices":\\s*(\\[[^\\]]*\\])`);
        const match = allScripts.match(searchRegex);
        
        if (match && match[1]) {
          try {
            // Parse the extracted array
            const parsedChoices = JSON.parse(match[1]);
            
            // Map it to our clean format
            options = parsedChoices.map((choice: any) => ({
              // Greenhouse usually stores the real value in 'value', 'name', or 'id'
              value: choice.value || choice.name || choice.label || choice.id?.toString(),
              text: choice.label || choice.name || choice.value?.toString()
            })).filter((opt: any) => opt.text !== "Select..."); // Drop placeholders
            
            console.log(`🕵️ Hijacked options for ${targetId}!`);
          } catch (e) {
            console.warn(`Found choices for ${targetId} but couldn't parse the JSON blob.`, match[1]);
          }
        }
      }
    }

    rawSchema.push({
      index: index,
      tagName: field.tagName,
      type: field.type,
      name: field.name,
      id: field.id,
      label: explicitLabel || closestLabel || 'none',
      options: options // This will now contain the beautifully formatted array
    });
    
    // Visual debugger
    field.style.border = "2px solid red"; 
  });

  // 3. Clean up the final payload
  return rawSchema.filter(field => {
    if (!field.id || field.id.trim() === "") return false;
    if (field.label === "none") return false;
    return true;
  });
}

function fillForm(formData: any[]) {
  formData.forEach(item => {
    const field = document.getElementById(item.id) as HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement;
    
    if (!field) {
      console.warn(`⚠️ Field with ID ${item.id} not found.`);
      return;
    }

    // Security block: Browsers will throw an error if you try to autofill a file input
    if (field.type === 'file') {
      console.log(`📁 Skipping file input: ${item.id} (Requires manual upload)`);
      return; 
    }

    // Handle Checkboxes/Radios
    if (field.type === 'checkbox' || field.type === 'radio') {
      (field as HTMLInputElement).checked = item.value === true;
    } 
    // Handle standard inputs and selects
    else {
      field.value = item.value;
    }

    // Dispatch events to trigger Greenhouse's React state updates
    field.dispatchEvent(new Event('input', { bubbles: true }));
    field.dispatchEvent(new Event('change', { bubbles: true }));

    field.style.border = "2px solid green"; 
  });

  console.log("✅ FORM FILL COMPLETE.");
}