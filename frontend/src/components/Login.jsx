import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        try {
            const res = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || 'Login failed');
            }
            const data = await res.json();
            // store token (here just username) in localStorage
            localStorage.setItem('token', data.token);
            navigate('/chat');
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
            <form className="bg-gray-800 p-6 rounded shadow-md w-80" onSubmit={handleSubmit}>
                <h2 className="text-2xl mb-4 text-center">Login</h2>
                {error && <p className="text-red-400 mb-2">{error}</p>}
                <input
                    type="text"
                    placeholder="Username"
                    className="w-full p-2 mb-3 rounded bg-gray-700 focus:outline-none"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    className="w-full p-2 mb-3 rounded bg-gray-700 focus:outline-none"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button
                    type="submit"
                    className="w-full bg-blue-600 hover:bg-blue-500 py-2 rounded"
                >
                    Login
                </button>
                <p className="mt-4 text-center text-sm">
                    No account? <a href="/signup" className="text-blue-400 underline">Sign up</a>
                </p>
            </form>
        </div>
    );
}

export default Login;
