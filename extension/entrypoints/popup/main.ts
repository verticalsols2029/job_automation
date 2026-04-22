import '@/assets/style.css';

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div class="w-80 p-5 bg-white flex flex-col gap-4 font-sans text-slate-800">
    <div class="border-b pb-3">
      <h1 class="text-lg font-bold">Job Autofill</h1>
      <p class="text-xs text-slate-500">v0.0.02 - Greenhouse Dev</p>
    </div>

    <div class="flex items-center justify-between text-sm">
      <span class="font-medium text-slate-600">Profile Data:</span>
      <span id="status-badge" class="bg-amber-100 text-amber-700 px-2 py-0.5 rounded text-xs font-semibold">
        Not Synced
      </span>
    </div>

    <div class="flex flex-col gap-2 mt-2">
      <button id="btn-sync" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition-colors text-sm">
        Sync Database
      </button>

      <button id="btn-autofill" class="w-full bg-slate-800 hover:bg-slate-900 text-white font-medium py-2 px-4 rounded transition-colors text-sm">
        Autofill Here
      </button>
    </div>
  </div>
`;

const btnSync = document.querySelector<HTMLButtonElement>('#btn-sync');
const btnAutofill = document.querySelector<HTMLButtonElement>('#btn-autofill');
const statusBadge = document.querySelector<HTMLSpanElement>('#status-badge');

// Mock Sync
btnSync?.addEventListener('click', async () => {
  btnSync.textContent = "Syncing...";
  setTimeout(() => {
    btnSync.textContent = "Sync Database";
    statusBadge!.textContent = "Synced";
    statusBadge!.className = "bg-green-100 text-green-700 px-2 py-0.5 rounded text-xs font-semibold";
  }, 1000); 
});

// Trigger Autofill Pipeline
btnAutofill?.addEventListener('click', async () => {
  btnAutofill.textContent = "Scanning...";
  btnAutofill.disabled = true;
  
  try {
    const [tab] = await browser.tabs.query({ active: true, currentWindow: true });
    
    if (tab?.id) {
      // 1. Ask content script for the clean field schema
      const scanResponse = await browser.tabs.sendMessage(tab.id, { action: 'SCAN_FIELDS' });
      
      if (scanResponse && scanResponse.success) {
        console.log("Received schema from page:", scanResponse.data);
        btnAutofill.textContent = "Processing AI...";

        // 2. Mocking the LLM generation time (1.5 seconds)
        setTimeout(async () => {
          
          // 3. This is the dummy data we will eventually replace with real LLM output
          const mockLLMOutput = [
            { id: "first_name", value: "Jane" },
            { id: "last_name", value: "Doe" },
            { id: "email", value: "jane.doe@example.com" },
            { id: "phone", value: "+1234567890" },
            { id: "gdpr_demographic_data_consent_given_1", value: true }
          ];

          btnAutofill.textContent = "Filling Form...";

          // 4. Send the data back to the content script to be injected
          await browser.tabs.sendMessage(tab.id!, { 
            action: 'FILL_FORM', 
            data: mockLLMOutput 
          });

          btnAutofill.textContent = "Done!";
          btnAutofill.classList.replace('bg-slate-800', 'bg-green-600');
          btnAutofill.classList.replace('hover:bg-slate-900', 'hover:bg-green-700');

          // Reset button after a few seconds
          setTimeout(() => {
            btnAutofill.textContent = "Autofill Here";
            btnAutofill.disabled = false;
            btnAutofill.classList.replace('bg-green-600', 'bg-slate-800');
            btnAutofill.classList.replace('hover:bg-green-700', 'hover:bg-slate-900');
          }, 2000);

        }, 1500); // Wait 1.5 seconds to simulate LLM think time
      }
    }
  } catch (error) {
    console.error("Extension communication failed. Is the script injected?", error);
    btnAutofill.textContent = "Error - Try Reloading";
    btnAutofill.disabled = false;
  }
});