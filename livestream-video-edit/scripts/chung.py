"""Hàm dùng chung cho các script: đọc transcript mốc từng từ, gọi ffmpeg.

Transcript chuẩn của skill (JSON):
    {"segments": [{"words": [{"w": "chữ", "s": 12.34, "e": 12.61}, ...]}, ...]}
- w: chữ như máy nghe (có thể kèm dấu câu), s/e: giây bắt đầu/kết thúc trong video nguồn.
Bóc chữ bằng faster-whisper (word_timestamps=True) rồi ghi đúng dạng này — xem references/01-nguon-va-chon-doan.md.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):      # console Windows mặc định cp1252 → chữ Việt lỗi
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
FP = os.environ.get("FFPROBE") or shutil.which("ffprobe") or "ffprobe"


def chuan(t):
    """chữ để so khớp: NFC, chữ thường, bỏ dấu câu"""
    return re.sub(r"[.,?!…:;\"“”]", "", unicodedata.normalize("NFC", t).lower()).strip()


def doc_tu(duong_dan):
    d = json.load(open(duong_dan, encoding="utf-8"))
    W = [w for s in d["segments"] for w in s["words"]]
    for w in W:
        w["t"] = chuan(w["w"])
    return W


def tim_cum(W, cum, a=0.0, b=1e12, cuoi=False):
    """chỉ số từ đầu của cụm (đã chuẩn hoá) trong khoảng giây [a, b]; cuoi=True lấy lần xuất hiện cuối"""
    p = chuan(cum).split()
    hit = [k for k in range(len(W) - len(p) + 1) if a - 0.5 <= W[k]["s"] <= b and [x["t"] for x in W[k:k + len(p)]] == p]
    if not hit:
        return None
    return (hit[-1] if cuoi else hit[0]), len(p)


def chay(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise RuntimeError(" ".join(map(str, cmd))[:300] + "\n" + r.stderr[-1500:])
    return r


def do_tieng(duong_dan):
    """(LUFS tích hợp, đỉnh thật dBTP) của file tiếng hoặc video"""
    r = chay([FF, "-hide_banner", "-nostats", "-i", duong_dan, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    return I, tp


def dai(duong_dan):
    return float(chay([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", duong_dan]).stdout.strip())
