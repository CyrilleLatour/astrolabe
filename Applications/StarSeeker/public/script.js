// ===== Capteurs → RA/DEC (COMPLET) =====
// - Lit l’orientation du téléphone (azimut + alt via matrice).
// - Calcule LST (temps sidéral local) d’après la date/longitude.
// - Convertit Alt/Az -> RA/DEC (formules classiques).
// - Affiche Az/Alt + LST + RA/DEC dans #status.
// - Géoloc auto (fallback Valais 46N, 7E).
// - Lissage EMA + unwrap azimut pour stabilité.
// - Réutilise calibration & mode depuis localStorage (azMode, azOffset, altInvert).

(() => {
  const statusEl = document.getElementById("status");

  // ---------- Helpers ----------
  const norm360 = d => ((d % 360) + 360) % 360;
  const norm24  = h => ((h % 24) + 24) % 24;
  const clamp   = (x,a,b)=>Math.max(a,Math.min(b,x));
  const toRad   = d => d*Math.PI/180, toDeg = r => r*180/Math.PI;

  // minutes HEURES / DEGRES stables (arrondi vers le bas)
  function fmtHourMin(h){
    h = norm24(h);
    const mt = Math.floor(h*60 + 1e-9);
    const H = Math.floor(mt/60), M = mt%60;
    return `${H}h ${M}m`;
  }
  function fmtDegMin(d){
    const s = d < 0 ? "−" : (d > 0 ? "+" : "+");
    d = Math.abs(d);
    const mt = Math.floor(d*60 + 1e-9);
    const D = Math.floor(mt/60), M = mt%60;
    return `${s}${D}° ${M}′`;
  }
  const fmtDegMinUnsigned = d => {
    d = Math.abs(d);
    const mt = Math.floor(d*60 + 1e-9);
    const D = Math.floor(mt/60), M = mt%60;
    return `${D}° ${M}′`;
  };

  function setStatus(txt){
    if (statusEl) statusEl.textContent = txt;
    // console.log(txt); // utile en debug
  }

  // ---------- Géoloc ----------
  let lat = 46.0, lon = 7.0; // Valais par défaut
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      p => { lat = p.coords.latitude; lon = p.coords.longitude; },
      () => {},
      { enableHighAccuracy:true, maximumAge:5000, timeout:5000 }
    );
  }

  // ---------- LST (GMST + longitude) ----------
  const julianDate = (d)=> d.getTime()/86400000 + 2440587.5;
  function gmstHours(date){
    const jd = julianDate(date), T = (jd - 2451545)/36525;
    const gmst = 280.46061837 + 360.98564736629*(jd-2451545) + 0.000387933*T*T - T*T*T/38710000;
    return norm24(gmst/15);
  }
  const lstHours = (date, lonDeg)=> norm24(gmstHours(date) + lonDeg/15);

  // ---------- Orientation / capteurs ----------
  function getScreenRotationDeg(){
    try{
      if (screen && typeof screen.orientation?.angle === "number") return screen.orientation.angle;
      if (typeof window.orientation === "number"){
        const o = window.orientation; return (o===90||o===-90)?90:(o===180?180:0);
      }
    }catch(_){}
    return 0;
  }
  function headingFromEvent(e){
    // heading (0°=Nord, croissant Est/CW)
    const wkh = e && e.webkitCompassHeading;
    if (typeof wkh === "number" && isFinite(wkh) && wkh >= 0) return norm360(wkh); // iOS
    if (e && e.absolute === true && typeof e.alpha === "number") return norm360(e.alpha + getScreenRotationDeg());
    if (typeof e.alpha === "number"){ let h = 360 - e.alpha; h += getScreenRotationDeg(); return norm360(h); }
    return null;
  }

  // Matrices
  function mul3(A,B){
    return [
      [
        A[0][0]*B[0][0] + A[0][1]*B[1][0] + A[0][2]*B[2][0],
        A[0][0]*B[0][1] + A[0][1]*B[1][1] + A[0][2]*B[2][1],
        A[0][0]*B[0][2] + A[0][1]*B[1][2] + A[0][2]*B[2][2]
      ],
      [
        A[1][0]*B[0][0] + A[1][1]*B[1][0] + A[1][2]*B[2][0],
        A[1][0]*B[0][1] + A[1][1]*B[1][1] + A[1][2]*B[2][1],
        A[1][0]*B[0][2] + A[1][1]*B[1][2] + A[1][2]*B[2][2]
      ],
      [
        A[2][0]*B[0][0] + A[2][1]*B[1][0] + A[2][2]*B[2][0],
        A[2][0]*B[0][1] + A[2][1]*B[1][1] + A[2][2]*B[2][1],
        A[2][0]*B[0][2] + A[2][1]*B[1][2] + A[2][2]*B[2][2]
      ]
    ];
  }

  // Altitude exacte via R = Rz(alpha)*Rx(beta)*Ry(gamma) et vecteur avant v=(0,0,-1)
  function altitudeFromEuler(alphaDeg, betaDeg, gammaDeg){
    const a = toRad(alphaDeg||0), b = toRad(betaDeg||0), g = toRad(gammaDeg||0);
    const ca=Math.cos(a), sa=Math.sin(a);
    const cb=Math.cos(b), sb=Math.sin(b);
    const cg=Math.cos(g), sg=Math.sin(g);

    const Rz = [[ca,-sa,0],[sa,ca,0],[0,0,1]];
    const Rx = [[1,0,0],[0,cb,-sb],[0,sb,cb]];
    const Ry = [[cg,0,sg],[0,1,0],[-sg,0,cg]];

    const RzRx = mul3(Rz, Rx);
    const R = mul3(RzRx, Ry);

    // v = (0,0,-1) => composante z du vecteur monde = -R[2][2]
    const fz = -R[2][2];
    const alt = toDeg(Math.asin(clamp(fz,-1,1)));
    return clamp(alt, -90, 90);
  }

  // ---------- Modes & calibration ----------
  // 0: N-CW; 1: E-CW; 2: N-CCW; 3: E-CCW (compat avec ta page Az/Alt)
  let azMode   = Number(localStorage.getItem("azMode") ?? "0") % 4;
  let azOffset = Number(localStorage.getItem("azOffset") ?? "0");
  let altInvert= Number(localStorage.getItem("altInvert") ?? "1"); // 1 ou -1

  function mapHeadingToAz(heading){
    let A;
    switch(azMode){
      case 0: A = heading; break;          // N sens horaire
      case 1: A = heading - 90; break;     // E sens horaire
      case 2: A = 360 - heading; break;    // N sens anti-horaire
      case 3: A = 90 - heading; break;     // E sens anti-horaire
      default: A = heading; break;
    }
    return norm360(A + azOffset);
  }

  // ---------- Lissage ----------
  let emaAz=null, emaAlt=null, lastAzU=null;
  const K = 0.10; // EMA
  function unwrap(x, ref){ let d=x-ref; if (d>180) x-=360; else if (d<-180) x+=360; return x; }

  // ---------- AltAz -> RA/DEC ----------
  function altAzToRaDec(altDeg, azDeg, latDeg, lonDeg, date){
    // azDeg: 0°=Nord, croissant vers l’Est (CW) — cohérent avec heading
    const h = toRad(altDeg), A = toRad(azDeg), φ = toRad(latDeg);

    // Déclinaison
    const sinδ = Math.sin(φ)*Math.sin(h) + Math.cos(φ)*Math.cos(h)*Math.cos(A);
    const δ = Math.asin(clamp(sinδ, -1, 1));

    // Angle horaire H = atan2(y, x)
    const y = -Math.sin(A)*Math.cos(h);
    const x =  Math.cos(φ)*Math.sin(h) - Math.sin(φ)*Math.cos(h)*Math.cos(A);
    const H  = Math.atan2(y, x);          // rad

    const Hh = norm24(toDeg(H)/15);       // h
    const LST= lstHours(date, lonDeg);    // h
    const RA = norm24(LST - Hh);          // h
    return { ra: RA, dec: toDeg(δ), lst: LST };
  }

  // ---------- Affichage ----------
  function render(AzDeg, AltDeg, raH, decD, lstH){
    const s =
      `Az=${fmtDegMinUnsigned(AzDeg)}  |  Alt=${fmtDegMin(decD === undefined ? AltDeg : AltDeg)}\n` + // Alt signé
      `LST=${fmtHourMin(lstH)}\n` +
      `RA=${fmtHourMin(raH)}  |  DEC=${fmtDegMin(decD)}`;
    setStatus(s);
  }

  // ---------- Handler capteurs ----------
  function onOrient(e){
    const heading = headingFromEvent(e);
    if (heading == null) return;

    let alt = altitudeFromEuler(e.alpha||0, e.beta||0, e.gamma||0) * (altInvert === 1 ? 1 : -1);
    const azM = mapHeadingToAz(heading);

    if (lastAzU == null) lastAzU = azM;
    const azU = unwrap(azM, lastAzU);

    if (emaAz == null){ emaAz = azU; emaAlt = alt; lastAzU = azU; }

    // EMA
    emaAz  = (1-K)*emaAz  + K*azU;
    emaAlt = (1-K)*emaAlt + K*alt;
    lastAzU = emaAz;

    const when = new Date();
    const { ra, dec, lst } = altAzToRaDec(emaAlt, norm360(emaAz), lat, lon, when);

    render(norm360(emaAz), emaAlt, ra, dec, lst);
  }

  // ---------- Démarrage (Android: auto ; iOS: bouton permission) ----------
  function addListeners(){
    window.addEventListener("deviceorientationabsolute", onOrient, {passive:true});
    window.addEventListener("deviceorientation",          onOrient, {passive:true});
  }

  async function start(){
    try{
      if (typeof DeviceOrientationEvent !== "undefined" &&
          typeof DeviceOrientationEvent.requestPermission === "function"){
        // iOS: demande de permission via bouton
        const btn = document.createElement("button");
        btn.textContent = "Démarrer capteurs";
        btn.style.cssText = "position:fixed;left:50%;bottom:24px;transform:translateX(-50%);padding:10px 14px;border:0;border-radius:10px;background:#2d7cff;color:#fff;font-weight:700;z-index:9999";
        btn.onclick = async () => {
          try{
            const p = await DeviceOrientationEvent.requestPermission();
            if (p === "granted"){ addListeners(); btn.remove(); setStatus("Capteurs actifs."); }
            else setStatus("Autorise l’accès aux capteurs.");
          }catch{ setStatus("Capteurs refusés."); }
        };
        document.body.appendChild(btn);
        setStatus("Appuie sur « Démarrer capteurs » et autorise l’accès.");
      } else {
        // Android: direct
        addListeners();
        setStatus("Capteurs actifs.");
      }
    }catch(err){
      console.error(err);
      setStatus("Capteurs indisponibles.");
    }
  }

  // Lancement
  setStatus("Initialisation…");
  start();
})();
