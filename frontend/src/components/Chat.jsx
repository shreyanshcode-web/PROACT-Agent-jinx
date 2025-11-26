import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Chat() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const navigate = useNavigate();
    const token = localStorage.getItem('token');

    useEffect(() => {
        if (!token) {
            navigate('/login');
        }
    }, [token, navigate]);

    const sendMessage = async () => {
        if (!input.trim()) return;
        const userMsg = { role: 'user', content: input.trim() };
        setMessages((prev) => [...prev, userMsg]);
        setInput('');
        try {
            const res = await fetch('/api/prompt', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: userMsg.content }),
            });
            const data = await res.json();
            const botMsg = { role: 'bot', content: data.reply };
            setMessages((prev) => [...prev, botMsg]);
        } catch (e) {
            console.error('Chat error', e);
        }
    };

    const handleKey = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gray-900 text-white p-4">
            <h1 className="text-2xl font-bold mb-4 text-center">Jinx Chat</h1>
            <div className="flex-1 overflow-y-auto mb-4 space-y-2" id="chat-scroll">
                {messages.map((msg, i) => (
                    <div
                        key={i}
                        className={`p-2 rounded ${msg.role === 'user' ? 'bg-blue-600 self-end' : 'bg-gray-700 self-start'}`}
                    >
                        {msg.content}
                    </div>
                ))}
            </div>
            <div className="flex gap-2">
                <textarea
                    className="flex-1 p-2 rounded bg-gray-800 text-white focus:outline-none"
                    rows={1}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKey}
                    placeholder="Type a message..."
                />
                <button
                    className="px-4 py-2 bg-green-600 rounded hover:bg-green-500"
                    onClick={sendMessage}
                >
                    Send
                </button>
            </div>
        </div>
    );
}

export default Chat;
