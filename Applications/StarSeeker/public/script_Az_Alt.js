// ===== AZ/ALT — VERSION STABLE =====
(() => {
  const $ = s => document.querySelector(s);
  const vals = $("#vals");
  const msg  = $("#msg");
  const bStart=$("#btnStart"), bMode=$("#btnMode"), bCal=$("#btnCal"), bInv=$("#btnInv");

  const norm360 = d => ((d % 360) + 360) % 360;
  const clamp   = (x,a,b)=>Math.max(a,Math.min(b,x));
  const toRad   = d => d*Math.PI/180, toDeg = r => r*180/Math.PI;

  const note = t => { if (msg) msg.textContent = t || ""; };

  // --- heading & screen rotation ---
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
    const wkh = e && e.webkitCompassHeading;
    if (typeof wkh === "number" && isFinite(wkh) && wkh >= 0) return norm360(wkh); // iOS
    if (e && e.absolute === true && typeof e.alpha === "number") return norm360(e.alpha + getScreenRotationDeg());
    if (typeof e.alpha === "number"){ let h = 360 - e.alpha; h += getScreenRotationDeg(); return norm360(h); }
    return null;
  }

  // --- altitude via matrices (vecteur avant (0,0,-1)) ---
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

    const fz = -R[2][2]; // composante z du vecteur avant (0,0,-1)
    const alt = toDeg(Math.asin(clamp(fz,-1,1)));
    return clamp(alt, -90, 90);
  }

  // --- modes & calibration ---
  // 0: N-CW; 1: E-CW; 2: N-CCW; 3: E-CCW
  let azMode   = Number(localStorage.getItem("azMode") ?? "0") % 4;
  let azOffset = Number(localStorage.getItem("azOffset") ?? "0");
  let altInvert= Number(localStorage.getItem("altInvert") ?? "1"); // 1 ou -1

  function mapHeadingToAz(heading){
    let A;
    switch(azMode){
      case 0: A = heading; break;
      case 1: A = heading - 90; break;
      case 2: A = 360 - heading; break;
      case 3: A = 90 - heading; break;
      default: A = heading; break;
    }
    return norm360(A + azOffset);
  }

  // --- lissage ---
  let emaAz=null, emaAlt=null, lastAzU=null;
  const K = 0.10;
  function unwrap(x, ref){ let d=x-ref; if (d>180) x-=360; else if (d<-180) x+=360; return x; }

  function render(AzDeg, AltDeg){
    vals.textContent = `Az: ${AzDeg.toFixed(1)}°  |  Alt: ${AltDeg.toFixed(1)}°`;
  }

  function onOrient(e){
    const heading = headingFromEvent(e);
    if (heading == null) return;

    const alt = altitudeFromEuler(e.alpha||0, e.beta||0, e.gamma||0) * (altInvert === 1 ? 1 : -1);
    const azM = mapHeadingToAz(heading);

    if (lastAzU == null) lastAzU = azM;
    const azU = unwrap(azM, lastAzU);

    if (emaAz == null){ emaAz = azU; emaAlt = alt; lastAzU = azU; }

    emaAz  = (1-K)*emaAz  + K*azU;
    emaAlt = (1-K)*emaAlt + K*alt;
    lastAzU = emaAz;

    render(norm360(emaAz), emaAlt);
  }

  function addListeners(){
    window.addEventListener("deviceorientationabsolute", onOrient, {passive:true});
    window.addEventListener("deviceorientation",          onOrient, {passive:true});
  }

  async function start(){
    try{
      if (typeof DeviceOrientationEvent !== "undefined" &&
          typeof DeviceOrientationEvent.requestPermission === "function"){
        const btn = document.createElement("button");
        btn.textContent = "Démarrer capteurs";
        btn.style.cssText = "position:fixed;left:50%;bottom:24px;transform:translateX(-50%);padding:10px 14px;border:0;border-radius:10px;background:#2d7cff;color:#fff;font-weight:700;z-index:9999";
        btn.onclick = async () => {
          try{
            const p = await DeviceOrientationEvent.requestPermission();
            if (p === "granted"){ addListeners(); btn.remove(); note("Capteurs actifs."); }
            else note("Autorise l’accès aux capteurs.");
          }catch{ note("Capteurs refusés."); }
        };
        document.body.appendChild(btn);
        note("Appuie sur « Démarrer capteurs » et autorise l’accès.");
      } else {
        addListeners();
        note("Capteurs actifs.");
      }
    }catch(err){
      console.error(err);
      note("Capteurs indisponibles.");
    }
  }

  // Boutons
  bMode?.addEventListener("click", ()=>{
    azMode = (azMode + 1) % 4;
    localStorage.setItem("azMode", String(azMode));
    note(`Mode Azimut: ${["N-CW","E-CW","N-CCW","E-CCW"][azMode]}`);
  });
  bCal?.addEventListener("click", ()=>{
    if (emaAz == null){ note("Bouge un peu puis calibre."); return; }
    const Acur = norm360(emaAz);
    azOffset = norm360(-Acur);
    localStorage.setItem("azOffset", String(azOffset));
    note("Calibration Nord appliquée.");
  });
  bInv?.addEventListener("click", ()=>{
    altInvert = (altInvert === 1 ? -1 : 1);
    localStorage.setItem("altInvert", String(altInvert));
    note(`Inversion Alt: ${altInvert===1?"OFF":"ON"}`);
  });

  start();
})();
