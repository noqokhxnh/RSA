async function generateKeysFromAPI() {
    const p = parseInt(document.getElementById('primeP').value);
    const q = parseInt(document.getElementById('primeQ').value); // Sửa lỗi typo
    const e = parseInt(document.getElementById('publicExponent').value);
    if (!p || !q || !e || isNaN(p) || isNaN(q) || isNaN(e)) {
        alert('Vui lòng nhập đầy đủ và đúng định dạng cho p, q và e!');
        return;
    }
    const result = await apiGenerateKeys(p, q, e);
    if (result.error) {
        alert(result.error);
        return;
    }
    document.getElementById('publicKey').value = `(${result.public_key[0]}, ${result.public_key[1]})`;
    document.getElementById('privateKey').value = `(${result.private_key[0]}, ${result.private_key[1]})`;
    console.log('Public key:', result.public_key);
}

// Lưu lịch sử ký và xác minh trong session (có thể thay bằng localStorage nếu muốn lưu lâu dài)
let signatureHistory = [];

function saveHistory(entry) {
    signatureHistory.push(entry);
    // Nếu muốn lưu lâu dài, dùng localStorage:
    localStorage.setItem('signatureHistory', JSON.stringify(signatureHistory));
    renderHistory();
}

// function renderHistory() {
//     let table = `<table border="1" style="width:100%;margin-top:20px;text-align:left;font-size:14px;">
//         <tr><th>Thời gian</th><th>Thông điệp/File</th><th>Chữ ký</th><th>Trạng thái</th></tr>`;
//     for (let i = signatureHistory.length - 1; i >= 0; i--) {
//         const h = signatureHistory[i];
//         table += `<tr><td>${h.time}</td><td>${h.message}</td><td style="word-break:break-all;">${h.signature}</td><td>${h.status || ''}</td></tr>`;
//     }
//     table += '</table>';
//     const historyDiv = document.getElementById('historyTable');
//     if (historyDiv) historyDiv.innerHTML = table;
// }

// Lưu lịch sử khi ký
async function signMessageFromAPI() {
    const message = document.getElementById('message').value;
    const privateKey = document.getElementById('privateKey').value.replace(/[()]/g, '').split(',').map(x => x.trim());
    const result = await apiSignMessage(message, privateKey);
    const now = new Date().toLocaleString();
    if (result.error) {
        alert(result.error);
        saveHistory({ time: now, message, signature: '-', status: 'Lỗi: ' + result.error });
        return;
    }
    document.getElementById('signature').textContent = result.signature;
    saveHistory({ time: now, message, signature: result.signature, status: 'Đã ký' });
    alert('Tạo chữ ký thành công!');
}

// Lưu lịch sử khi xác minh
async function verifySignatureFromAPI() {
    const message = document.getElementById('message').value;
    const signature = document.getElementById('signature').textContent;
    const publicKey = document.getElementById('publicKey').value.replace(/[()]/g, '').split(',').map(x => x.trim());
    const result = await apiVerifySignature(message, signature, publicKey);
    const now = new Date().toLocaleString();
    let status = '';
    if (result.error) {
        status = 'Lỗi: ' + result.error;
        alert(result.error);
    } else {
        status = result.is_valid ? '✅ Hợp lệ' : '❌ Không hợp lệ';
        alert(result.is_valid ? '✅ Chữ ký hợp lệ' : '❌ Chữ ký không hợp lệ');
    }
    saveHistory({ time: now, message, signature, status });
}

function toggleHashVisibility() {
    const receivedMessage = document.getElementById('receivedMessage').value;
    if (!receivedMessage) {
        alert('Vui lòng nhập thông điệp trước!');
        return;
    }
    const hash = CryptoJS.SHA256(receivedMessage).toString(CryptoJS.enc.Hex);
    alert(`Hash của thông điệp "${receivedMessage}" là: ${hash}`);
}

function generateRandomPrimes() {
    const isPrime = (num) => {
        if (num <= 1) return false;
        for (let i = 2; i * i <= num; i++) {
            if (num % i === 0) return false;
        }
        return true;
    };

    const generatePrime = () => {
        let prime;
        do {
            prime = Math.floor(Math.random() * 10000000) + 10000000;
            if (prime % 2 === 0) prime += 1;
        } while (!isPrime(prime));
        return prime;
    };

    document.getElementById('primeP').value = generatePrime();
    document.getElementById('primeQ').value = generatePrime();
}

function togglePrivateKeyVisibility() {
    const privateKeyElement = document.getElementById('privateKey');
    const eyeIcon = document.getElementById('eyeIcon');
    if (privateKeyElement.type === 'password') {
        privateKeyElement.type = 'text';
        eyeIcon.className = 'fa-solid fa-eye-slash';
        setTimeout(() => {
            privateKeyElement.type = 'password';
            eyeIcon.className = 'fa-solid fa-eye';
        }, 3000);
    } else {
        privateKeyElement.type = 'password';
        eyeIcon.className = 'fa-solid fa-eye';
    }
}

function displayFileContent() {
    const fileInput = document.getElementById('fileToSign');
    const fileContentElement = document.getElementById('fileContent');
    if (!fileInput.files.length) {
        fileContentElement.value = '';
        return;
    }
    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = function(event) {
        fileContentElement.value = event.target.result.trim();
    };
    reader.readAsText(file, 'UTF-8');
}

async function createSignature() {
    const fileInput = document.getElementById('fileToSign');
    const privateKey = document.getElementById('privateKey').value.replace(/[()]/g, '').split(',').map(x => x.trim());
    if (!fileInput.files.length || !privateKey) {
        alert('Vui lòng chọn file');
        return;
    }
    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = async function(event) {
        const fileContent = event.target.result.trim();
        console.log('File content to sign:', fileContent);
        const result = await apiSignMessage(fileContent, privateKey);
        const now = new Date().toLocaleString();
        if (result.error) {
            alert(result.error);
            saveHistory({ time: now, message: file.name, signature: '-', status: 'Lỗi: ' + result.error });
            return;
        }
        const blob = new Blob([result.signature], { type: 'text/plain' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `${file.name}.sig`;
        link.click();
        document.getElementById('signature').textContent = result.signature;
        saveHistory({ time: now, message: file.name, signature: result.signature, status: 'Đã ký file' });
        console.log('Signature:', result.signature);
        alert('Tạo chữ ký thành công!');
    };
    reader.readAsText(file, 'UTF-8');
}

async function verifySignature() {
    const originalFileInput = document.getElementById('originalFile');
    const encryptedFileInput = document.getElementById('encryptedFile');
    const publicKeyE = document.getElementById('verifyE').value;
    const publicKeyN = document.getElementById('verifyN').value;
    if (!originalFileInput.files.length || !encryptedFileInput.files.length || !publicKeyE || !publicKeyN) {
        alert('Vui lòng chọn cả file gốc, file chữ ký và nhập khóa công khai!');
        return;
    }
    console.log('Public key E:', publicKeyE,'\n','Public key N:', publicKeyN);
    const originalFile = originalFileInput.files[0];
    const encryptedFile = encryptedFileInput.files[0];
    const originalReader = new FileReader();
    const encryptedReader = new FileReader();
    originalReader.onload = async function(event) {
        encryptedReader.onload = async function(event) {
            const signature = event.target.result.trim();
            console.log('Signature:', signature);
            const publicKey = [publicKeyE, publicKeyN];
            const result = await apiVerifySignature(originalContent, signature, publicKey);
            if (result.error) {
                alert(result.error);
                return;
            }
            alert(result.is_valid ? '✅ Chữ ký hợp lệ' : '❌ Chữ ký không hợp lệ');
        };
        encryptedReader.readAsText(encryptedFile, 'UTF-8');
    };
    originalReader.readAsText(originalFile, 'UTF-8');
}

function showCreateRSA() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="section create">
            <h2>Tạo chữ ký số</h2>
            <div>
                <label>Chọn 2 số nguyên tố ngẫu nhiên:</label><br>
                <input type="number" id="primeP" placeholder="p" >
                <input type="number" id="primeQ" placeholder="q" >
                <button onclick="generateRandomPrimes()">Ngẫu nhiên</button>
            </div>
            <div>
                <label>Nhập số e:</label><br>
                <input type="number" id="publicExponent">
            </div>
            <div>
                <label>Khóa bí mật:</label><br>
                <div style="position: relative;">
                    <input type="password" id="privateKey" readonly style="width: calc(100% - 30px);">
                    <button onclick="togglePrivateKeyVisibility()" style="position: absolute; right: 0; top: 0; height: 100%; width: 30px;">
                        <i id="eyeIcon" class="fa-solid fa-eye"></i>
                    </button>
                </div>
            </div>
            <div>
                <label>Khóa công khai:</label><br>
                <input type="text" id="publicKey" readonly>
            </div>
            <button onclick="generateKeysFromAPI()">Sinh khóa</button>
            <div style="margin-top: 20px;">
                <label>Hoặc chọn file thông điệp để ký:</label><br>
                <input type="file" id="fileToSign" onchange="displayFileContent()">
                <textarea id="fileContent" readonly style="width: 100%; margin-top: 10px;"></textarea>
                <button onclick="createSignature()" style="margin-top: 10px;">Tạo chữ ký từ file</button>
            </div>
           
            <div id="historyTable"></div>
        </div>
    `;
    // renderHistory();
}

function showVerifySignature() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="section check">
            <h2>Kiểm tra chữ ký số</h2>
            <div>
                <label>Khóa công khai:</label><br>
                <input type="number" id="verifyE" placeholder="e =">
                <input type="number" id="verifyN" placeholder="n =">
            </div>
            <div>
                <label>Tải file gốc:</label><br>
                <input type="file" id="originalFile">
            </div>
            <div>
                <label>Tải file chữ ký:</label><br>
                <input type="file" id="encryptedFile">
            </div>
            <button onclick="verifySignature()">Xác minh chữ ký</button>
        </div>
    `;
}