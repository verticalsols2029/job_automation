import { useState } from "react"


function IndexPopup() {
  const [status, setStatus] = useState("Ready to help with your application!")

  // Placeholder functions for your extension logic
  const handleAutofill = () => setStatus("✨ Autofilling application...")
  const handleTailorAutofill = () => setStatus("✨ Tailoring & Autofilling application...")
  const handleSaveJob = () => setStatus("🔖 Job saved successfully!")
  const handleTailorResume = () => setStatus("🔖 Resume tailored successfully!")

  return (
    <div
      style={{
        width: 320,
        padding: 20,
        fontFamily: "system-ui, -apple-system, sans-serif",
        backgroundColor: "#FFFFFF",
        borderRadius: 12,
      }}>
      
      <div style={{ borderBottom: "1px solid #eee", paddingBottom: 12, marginBottom: 16 }}>
        <h2 style={{ margin: 0, fontSize: "18px", color: "#111827" }}>
          Fast Apply ⚡️
        </h2>
      </div>

      <p style={{ fontSize: "13px", color: "#6B7280", marginBottom: 20, minHeight: "20px" }}>
        {status}
      </p>

      <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
        <button 
          onClick={handleAutofill} 
          style={{...baseButtonStyle, backgroundColor: "#4F46E5", color: "white"}}
        >
          Autofill Application
        </button>

        <button 
          onClick={handleTailorAutofill} 
          style={{...baseButtonStyle, backgroundColor: "#8B5CF6", color: "white"}}
        >
          Tailor & Autofill
        </button>

        <button 
          onClick={handleTailorResume} 
          style={{...baseButtonStyle, backgroundColor: "#10B981", color: "white"}}
        >
          Tailor Resume
        </button>

        <button 
          onClick={handleSaveJob} 
          style={{...baseButtonStyle, backgroundColor: "#F3F4F6", color: "#374151", border: "1px solid #D1D5DB"}}
        >
          Save Job
        </button>
      </div>
    </div>
  )
}

const baseButtonStyle = {
  padding: "12px 16px",
  borderRadius: "8px",
  border: "none",
  fontSize: "14px",
  fontWeight: "600",
  cursor: "pointer",
  transition: "opacity 0.2s ease",
  width: "100%",
  display: "block"
}

export default IndexPopup