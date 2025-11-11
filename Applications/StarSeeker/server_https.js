// server_https.js — HTTPS statique propre (sans Express)
// Sert ./public en HTTPS :8443 + redirige HTTP :8080 → HTTPS
// Prérequis : key.pem et cert.pem à la racine du projet

const https = require("https");
const http = require("http");
const fs = require("fs");
const path = require("path");

const HOST = "0.0.0.0";
const HTTPS_PORT = 8443;
const HTTP_PORT = 8080;
const ROOT = path.join(__dirname, "public");

// ---- Certificats ----
const KEY = path.join(__dirname, "key.pem");
const CRT = path.join(__dirname, "cert.pem");
if (!fs.existsSync(KEY) || !fs.existsSync(CRT)) {
  console.error("❌ key.pem / cert.pem manquants. Place-les à la racine du projet.");
  process.exit(1);
}
const tlsOptions = {
  key: fs.readFileSync(KEY),
  cert: fs.readFileSync(CRT),
};

// ---- MIME types ----
const MIME = {
  ".html": "text/html; charset=utf-8",
  ".htm":  "text/html; charset=utf-8",
  ".js":   "application/javascript; charset=utf-8",
  ".mjs":  "application/javascript; charset=utf-8",
  ".css":  "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".geojson": "application/geo+json; charset=utf-8",
  ".csv":  "text/csv; charset=utf-8",
  ".txt":  "text/plain; charset=utf-8",
  ".png":  "image/png",
  ".jpg":  "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif":  "image/gif",
  ".svg":  "image/svg+xml",
  ".ico":  "image/x-icon",
  ".webp": "image/webp",
  ".mp4":  "video/mp4",
  ".mov":  "video/quicktime",
  ".pdf":  "application/pdf",
};

// ---- Helpers ----
function send(res, code, body, headers = {}) {
  res.writeHead(code, {
    "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate",
    "Pragma": "no-cache",
    "Expires": "0",
    "Access-Control-Allow-Origin": "*",
    ...headers,
  });
  if (Buffer.isBuffer(body)) res.end(body);
  else res.end(body ?? "");
}

function notFound(res) {
  send(res, 404, "Not Found\n", { "Content-Type": "text/plain; charset=utf-8" });
}

function serveStatic(req, res) {
  const urlPath = decodeURIComponent((req.url || "/").split("?")[0]);

  // Route par défaut → index.html
  let filePath = urlPath === "/" ? path.join(ROOT, "index.html") : path.join(ROOT, urlPath);

  // Sécurité : rester dans ROOT
  try {
    const resolved = path.resolve(filePath);
    if (!resolved.startsWith(path.resolve(ROOT))) {
      return send(res, 403, "Forbidden\n", { "Content-Type": "text/plain; charset=utf-8" });
    }
  } catch {
    return notFound(res);
  }

  // Si dossier → index.html dans ce dossier
  if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
    filePath = path.join(filePath, "index.html");
  }

  fs.readFile(filePath, (err, data) => {
    if (err) return notFound(res);
    const ext = path.extname(filePath).toLowerCase();
    const type = MIME[ext] || "application/octet-stream";
    send(res, 200, data, { "Content-Type": type });
  });
}

// ---- HTTPS server (principal) ----
https
  .createServer(tlsOptions, (req, res) => {
    if (req.method === "GET" || req.method === "HEAD") return serveStatic(req, res);
    return send(res, 405, "Method Not Allowed\n", { "Content-Type": "text/plain; charset=utf-8" });
  })
  .listen(HTTPS_PORT, HOST, () => {
    console.log(`✅ HTTPS statique sur https://localhost:${HTTPS_PORT}`);
    console.log(`   Sert: ${ROOT}`);
  });

// ---- HTTP → redirection HTTPS (facultatif mais pratique) ----
http
  .createServer((req, res) => {
    const host = (req.headers.host || "").replace(/:\d+$/, "");
    res.writeHead(301, { Location: `https://${host}:${HTTPS_PORT}${req.url}` });
    res.end();
  })
  .listen(HTTP_PORT, HOST, () => {
    console.log(`↪️  HTTP ${HTTP_PORT} redirige vers HTTPS ${HTTPS_PORT}`);
  });
