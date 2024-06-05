import React, { useState } from "react";
import "./ChatBot.css";

const Chatbot: React.FC = () => {
  const [message, setMessage] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [isReceiving, setIsReceiving] = useState<boolean>(false);

  const sendMessage = async () => {
    setResponse(""); // Clear previous response
    setIsReceiving(true); // Start receiving data
    try {
      const res = await fetch("http://localhost:8000/chatbot/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ message }),
      });

      const reader = res.body?.getReader();
      const decoder = new TextDecoder("utf-8");

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            setIsReceiving(false); // Stop receiving data
            break;
          }
          const chunk = decoder.decode(value, { stream: true });
          console.log("Received chunk:", chunk); // Log received chunk
          setResponse((prev) => prev + chunk);
        }
      }
    } catch (error) {
      console.error("Erreur:", error);
      setIsReceiving(false); // Stop receiving data in case of error
    }
  };

  return (
    <div className="chatbot-container">
      <h1>Chatbot</h1>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={sendMessage}>Envoyer</button>
      <p>
        Réponse: {response}
        {isReceiving && <span className="cursor"></span>}
      </p>
    </div>
  );
};

export default Chatbot;
