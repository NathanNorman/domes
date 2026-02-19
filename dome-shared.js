// ===================================================================
// dome-shared.js — Constants and drawing utilities shared across views
// ===================================================================

// --- Structural constants ---
var DOME_R = 16.5;
var BACK_WALL_LEN = 30.0;
var CONN_ANGLE_DEG = 20.0;
var WALL_ANGLE_DEG = -25.0;
var LEFT_WALL_H = 20.0;
var RIGHT_POST_H = 8.0;
var ROOF_DROP = LEFT_WALL_H - RIGHT_POST_H; // 12
var INTERIOR_WALL_H = 12.0;

// --- Math constants ---
var DEG2RAD = Math.PI / 180;
var RAD2DEG = 180 / Math.PI;

// ===================================================================
// Canvas setup — HiDPI-aware
// ===================================================================
function setupCanvas(canvas) {
  var dpr = window.devicePixelRatio || 1;
  var rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  var ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);
  return { ctx: ctx, w: rect.width, h: rect.height };
}

// ===================================================================
// World-to-screen coordinate transform
// pad: fraction of canvas size used as padding (default 0.05)
// ===================================================================
function makeTransform(w, h, xMin, xMax, yMin, yMax, pad) {
  if (pad === undefined) pad = 0.05;
  var padX = pad * w, padY = pad * h;
  var drawW = w - 2 * padX;
  var drawH = h - 2 * padY;
  var scaleX = drawW / (xMax - xMin);
  var scaleY = drawH / (yMax - yMin);
  var scale = Math.min(scaleX, scaleY);
  var offsetX = padX + (drawW - scale * (xMax - xMin)) / 2;
  var offsetY = padY + (drawH - scale * (yMax - yMin)) / 2;
  return {
    tx: function(x) { return offsetX + (x - xMin) * scale; },
    ty: function(y) { return h - (offsetY + (y - yMin) * scale); },
    scale: scale
  };
}

// ===================================================================
// Primitive drawing helpers (all take ctx + transform t)
// ===================================================================
function drawLine(ctx, t, x1, y1, x2, y2, color, lw) {
  ctx.beginPath();
  ctx.moveTo(t.tx(x1), t.ty(y1));
  ctx.lineTo(t.tx(x2), t.ty(y2));
  ctx.strokeStyle = color || '#000';
  ctx.lineWidth = lw || 2;
  ctx.stroke();
}

function drawDot(ctx, t, x, y, r, color) {
  ctx.beginPath();
  ctx.arc(t.tx(x), t.ty(y), r || 4, 0, 2 * Math.PI);
  ctx.fillStyle = color || '#000';
  ctx.fill();
}

function drawSquare(ctx, t, x, y, size, color) {
  var s = size || 6;
  ctx.fillStyle = color || '#000';
  ctx.fillRect(t.tx(x) - s / 2, t.ty(y) - s / 2, s, s);
}

function drawText(ctx, t, x, y, text, opts) {
  opts = opts || {};
  ctx.save();
  ctx.font = (opts.weight || 'bold') + ' ' + (opts.size || 12) + 'px -apple-system, sans-serif';
  ctx.fillStyle = opts.color || '#333';
  ctx.textAlign = opts.align || 'center';
  ctx.textBaseline = opts.baseline || 'middle';
  var sx = t.tx(x), sy = t.ty(y);
  if (opts.rotation) {
    ctx.translate(sx, sy);
    ctx.rotate(-opts.rotation * DEG2RAD);
    ctx.fillText(text, 0, 0);
  } else {
    ctx.fillText(text, sx, sy);
  }
  ctx.restore();
}

function drawGrid(ctx, t, xMin, xMax, yMin, yMax, majorStep, minorStep) {
  ctx.strokeStyle = '#ccc';
  ctx.lineWidth = 0.3;
  ctx.globalAlpha = 0.4;
  for (var x = Math.ceil(xMin / minorStep) * minorStep; x <= xMax; x += minorStep) {
    ctx.beginPath(); ctx.moveTo(t.tx(x), t.ty(yMin)); ctx.lineTo(t.tx(x), t.ty(yMax)); ctx.stroke();
  }
  for (var y = Math.ceil(yMin / minorStep) * minorStep; y <= yMax; y += minorStep) {
    ctx.beginPath(); ctx.moveTo(t.tx(xMin), t.ty(y)); ctx.lineTo(t.tx(xMax), t.ty(y)); ctx.stroke();
  }
  ctx.strokeStyle = '#aaa';
  ctx.lineWidth = 0.5;
  ctx.globalAlpha = 0.5;
  for (var x2 = Math.ceil(xMin / majorStep) * majorStep; x2 <= xMax; x2 += majorStep) {
    ctx.beginPath(); ctx.moveTo(t.tx(x2), t.ty(yMin)); ctx.lineTo(t.tx(x2), t.ty(yMax)); ctx.stroke();
  }
  for (var y2 = Math.ceil(yMin / majorStep) * majorStep; y2 <= yMax; y2 += majorStep) {
    ctx.beginPath(); ctx.moveTo(t.tx(xMin), t.ty(y2)); ctx.lineTo(t.tx(xMax), t.ty(y2)); ctx.stroke();
  }
  ctx.globalAlpha = 1.0;
}
