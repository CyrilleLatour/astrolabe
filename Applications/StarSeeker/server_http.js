// server_https.js — HTTPS statique ultra-minimal sur 8443 (sans Express)
const https = require("https");
const fs = require("fs");
const path = require("path");
const http = require("http");

const HOST = "0.0.0.0";
const PORT = 8443;
const ROOT = path.join(__dirname, "public");

// chemins des certifs (self-signed)
const KEY = path.join(__dirname, "key.pem");
const CRT = path.join(__dirname, "cert.pem");

// MIME basique
const MIME = {
  ".html": "text/html; charset=utf-8",
  ".htm":  "text/html; charset=utf-8",
  ".js":   "application/javascript; charset=utf-8",
  ".css":  "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".geojson":"application/geo+json; charset=utf-8",
  ".csv":  "text/csv; charset=utf-8",
  ".png":  "image/png",
  ".jpg":  "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif":  "image/gif",
  ".svg":  "image/svg+xml",
  ".ico":  "image/x-icon",
  ".txt":  "text/plain; charset=utf-8"
};

function send(res, code, body, headers = {}) {
  res.writeHead(code, {
    "Cache-Control":"no-store, no-cache, must-revalidate, proxy-revalidate",
    "Pragma":"no-cache",
    "Expires":"0",
    "Access-Control-Allow-Origin":"*",
    ...headers
  });
  res.end(body);
}

function serveFile(req, res) {
  const urlPath = decodeURIComponent(req.url.split("?")[0]);
  let filePath = path.normalize(path.join(ROOT, urlPath));

  // rester dans ROOT
  if (!filePath.startsWith(ROOT)) return send(res, 403, "Forbidden");

  // répertoire -> index.html
  if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
    filePath = path.join(filePath, "index.html");
  }
  // racine -> index.html
  if (urlPath === "/") filePath = path.join(ROOT, "index.html");

  fs.readFile(filePath, (err, data) => {
    if (err) return send(res, 404, "Not Found");
    const ext = path.extname(filePath).toLowerCase();
    const type = MIME[ext] || "application/octet-stream";
    send(res, 200, data, { "Content-Type": type });
  });
}

// vérif certifs
if (!fs.existsSync(KEY) || !fs.existsSync(CRT)) {
  console.error("❌ Certificats manquants. Place key.pem et cert.pem à la racine.");
  process.exit(1);
}

const options = {
  key: fs.readFileSync(KEY),
  cert: fs.readFileSync(CRT)
};

https.createServer(options, (req, res) => {
  if (req.method === "GET" || req.method === "HEAD") return serveFile(req, res);
  return send(res, 405, "Method Not Allowed");
}).listen(PORT, HOST, () => {
  console.log(`✅ HTTPS statique sur https://localhost:${PORT}`);
  console.log(`   Sert: ${ROOT}`);
});

// (facultatif) petit serveur HTTP 8080 qui redirige vers HTTPS
http.createServer((req, res) => {
  const host = (req.headers.host || "").replace(/:\d+$/, "");
  res.writeHead(301, { Location: `https://${host}:${PORT}${req.url}` });
  res.end();
}).listen(8080, HOST, () => {
  console.log("↪️  HTTP 8080 redirige vers HTTPS 8443");
});
