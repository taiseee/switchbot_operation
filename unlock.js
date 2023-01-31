const token = "efde79485d13de0bd56c96b8d87907f7d5526961006ee8dbfad7283b88069983873b64454db42e1a487378a9388a3c44";
const secret = "4b4d4c7d1c34385cc094a49fc1d37f4e";
const t = Date.now();
const nonce = "requestID";
const data = token + t + nonce;
const crypto = require('crypto');
const https = require('https');
const signTerm = crypto.createHmac('sha256', secret)
    .update(Buffer.from(data, 'utf-8'))
    .digest();
const sign = signTerm.toString("base64");
console.log(sign);

const body = JSON.stringify({
    "command": "unlock",
    "parameter": "default",
    "commandType": "command"
});
const deviceId = "D778CBF7D61A";
const options_unlock = {
    hostname: 'api.switch-bot.com',
    port: 443,
    path: `/v1.1/devices/${deviceId}/commands`,
    method: 'POST',
    headers: {
        "Authorization": token,
        "sign": sign,
        "nonce": nonce,
        "t": t,
        'Content-Type': 'application/json',
        'Content-Length': body.length,
    },
};


const req = https.request(options_unlock, res => {
    console.log(`statusCode: ${res.statusCode}`);
    res.on('data', d => {
        process.stdout.write(d);
    });
});

req.on('error', error => {
    console.error(error);
});

req.write(body);
req.end();