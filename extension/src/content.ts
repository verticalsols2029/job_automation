import { Readability } from "@mozilla/readability"
import type { PlasmoCSConfig } from "plasmo"

export const config: PlasmoCSConfig = {
  matches: ["<all_urls>"]
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "EXTRACT_JOB_DATA") {
    const docClone = document.cloneNode(true) as Document
    const article = new Readability(docClone).parse()
    const content = article?.textContent || document.body.innerText
    const cleanText = content.replace(/\s+/g, " ").trim()

    sendResponse({ success: true, text: cleanText })
  }
  return true
})