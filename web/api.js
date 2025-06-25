// Hàm gửi yêu cầu sinh khóa RSA lên server
async function apiGenerateKeys(p, q, e) {
    try {
        const response = await fetch('http://localhost:5000/generate_keys', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ p, q, e })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Lỗi không xác định!');
        return data;
    } catch (err) {
        return { error: err.message };
    }
}

// Hàm gửi yêu cầu ký thông điệp lên server
async function apiSignMessage(message, private_key) {
    try {
        const response = await fetch('http://localhost:5000/sign_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, private_key })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Lỗi không xác định!');
        return data;
    } catch (err) {
        return { error: err.message };
    }
}

// Hàm gửi yêu cầu xác minh chữ ký lên server
async function apiVerifySignature(message, signature, public_key) {
    try {
        const response = await fetch('http://localhost:5000/verify_signature', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, signature, public_key })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Lỗi không xác định!');
        return data;
    } catch (err) {
        return { error: err.message };
    }
}
