"""Lọc sạn trên mốc từng từ: nói hụt/lặp, tiếng đệm, khoảng lặng dài — rồi mới cắt video.

    python loc_dem.py transcript.json am-16k.wav ke-hoach.json giu.json [--cau-hinh cau-hinh.json]

am-16k.wav : tiếng nguồn mono 16 kHz  (ffmpeg -i nguon.mp4 -ac 1 -ar 16000 am-16k.wav)
ke-hoach.json:
    {"doan": [{"s": 358.52, "e": 454.61}, ...],      # các đoạn đã chọn, theo thứ tự phát (móc trước, thân sau)
     "chot": "cụm câu chốt",                        # tuỳ chọn: giữ nguyên khoảng lặng ngay trước câu này
     "bo_noi_dung": [["cụm đầu", "cụm cuối", "lý do"]]}  # tuỳ chọn: quyết định bỏ nội dung (ghi sổ riêng)
Ra giu.json: {"giu": [[s, e], ...] (giây nguồn, đã làm tròn theo khung), "so": [...sổ cắt...], "tho": giây, "con": giây}

Mặc định cho tiếng Việt nói; đổi bằng --cau-hinh (các khoá như hằng số viết hoa bên dưới).
Luật an toàn đã cài sẵn — đọc references/04-phu-de.md trước khi nới:
- không bao giờ bỏ từ phủ định (trừ khi chính nó là bản nói hụt);
- cụm lặp CÓ CHỦ Ý (vd. "ai ai" = đọc chữ AI) không bị coi là nói hụt — khai trong GIU_LAP;
- đại từ lặp sau giới từ ("của mình mình") không bị coi là nói hụt;
- khoảng lặng chỉ cắt khi năng lượng tiếng thật sự thấp (khe giữa từ mà vẫn có tiếng thì giữ).
"""
import argparse
import json
import wave

import numpy as np

from chung import doc_tu, tim_cum

FPS = 30
PHU_DINH = ["không", "chưa", "đừng", "chẳng", "chả", "hông", "hổng"]
DEM_DON = ["à", "ừ", "ờ", "ờm", "ưm", "ừm", "ầy", "hử", "ơ", "ừa", "hừ"]
DEM_DUOI = [["vậy", "đó"], ["các", "bạn", "ơi"], ["nha"], ["nhé"]]      # chỉ bỏ khi đứng riêng (lặng hai bên)
CUM_DEM = [["nói", "chung", "là"], ["nói", "thật", "ra", "là"], ["thì", "là", "mà"]]
DAI_TU = ["mày", "tao", "tôi", "em", "anh", "chị", "bạn", "mình", "họ", "nó"]
GIU_LAP = [["ai", "ai"], ["mãi", "mãi"]]   # lặp có chủ ý: "ai ai" = máy nghe chữ "AI"; "mãi mãi" là điệp từ
LANG_TOI_DA, LANG_GIU = 0.55, 0.25        # khoảng lặng > 0,55s rút còn 0,25s

ap = argparse.ArgumentParser()
ap.add_argument("transcript"); ap.add_argument("wav"); ap.add_argument("ke_hoach"); ap.add_argument("ra")
ap.add_argument("--cau-hinh")
g = ap.parse_args()
if g.cau_hinh:
    for k, v in json.load(open(g.cau_hinh, encoding="utf-8")).items():
        globals()[k] = v
PHU_DINH, DEM_DON, DAI_TU = set(PHU_DINH), set(DEM_DON), set(DAI_TU)

W = doc_tu(g.transcript)
KH = json.load(open(g.ke_hoach, encoding="utf-8"))
with wave.open(g.wav) as f:
    A = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32) / 32768
    if f.getframerate() != 16000:
        raise SystemExit("cần wav mono 16 kHz")
HOP = 160
DB = 20 * np.log10(np.sqrt(np.maximum(1e-12, np.convolve(A ** 2, np.ones(HOP) / HOP, "same")[::HOP])))


def lap_co_y(A1, A2):
    t = [W[i]["t"] for i in A1 + A2]
    return any(t[k:k + len(p)] == p for p in GIU_LAP for k in range(len(t) - len(p) + 1))


so, giu_het, tho = [], [], 0.0
chot_s = None
for part in KH["doan"]:
    a, b = part["s"], part["e"]
    tho += b - a
    ws = [i for i, w in enumerate(W) if w["s"] >= a - 0.05 and w["e"] <= b + 0.35 and w["s"] < b - 0.05]
    bo, nd = set(), set()
    # 0) quyết định nội dung (không phải sạn)
    for x, y, ly in KH.get("bo_noi_dung", []):
        i, j = tim_cum(W, x, a, b), tim_cum(W, y, a, b)
        if i and j:
            for k in range(i[0], j[0] + j[1]):
                bo.add(k); nd.add(k)
            so.append(dict(loai="nội dung (quyết định)", s=W[i[0]]["s"], e=W[j[0] + j[1] - 1]["e"], ly_do=ly))
    # 1) nói hụt / lặp: cụm n từ lặp ngay sau, giữ lần sau
    for n in range(14, 0, -1):
        k = 0
        while k + 2 * n <= len(ws):
            A1, A2 = ws[k:k + n], ws[k + n:k + 2 * n]
            if any(i in bo for i in A1 + A2):
                k += 1; continue
            t1, t2 = [W[i]["t"] for i in A1], [W[i]["t"] for i in A2]
            truoc = W[A1[0] - 1]["t"] if A1[0] > 0 else ""
            chu_ngu = n == 1 and t1[0] in DAI_TU and truoc in {"chính", "với", "của", "cho"}
            if t1 == t2 and W[A2[0]]["s"] - W[A1[0]]["s"] <= (2.0 if n <= 4 else 10.0) and not chu_ngu and not lap_co_y(A1, A2):
                for i in A1:
                    bo.add(i)
                so.append(dict(loai="hụt" if n <= 4 else "lặp", s=W[A1[0]]["s"], e=W[A1[-1]]["e"], chu=" ".join(W[i]["w"] for i in A1)))
                k += n
            else:
                k += 1
    # 2) tiếng đệm
    for i in ws:
        if i not in bo and W[i]["t"] in DEM_DON:
            bo.add(i); so.append(dict(loai="đệm", s=W[i]["s"], e=W[i]["e"], chu=W[i]["w"]))
    for mau in DEM_DUOI + CUM_DEM:
        n = len(mau)
        for p in range(len(ws) - n + 1):
            seg = ws[p:p + n]
            if any(i in bo for i in seg) or [W[i]["t"] for i in seg] != mau:
                continue
            if mau in DEM_DUOI:
                truoc = W[seg[0]]["s"] - (W[ws[p - 1]]["e"] if p > 0 else a)
                sau = (W[ws[p + n]]["s"] if p + n < len(ws) else b) - W[seg[-1]]["e"]
                if not (truoc > 0.2 and sau > 0.2):
                    continue
            for i in seg:
                bo.add(i)
            so.append(dict(loai="đệm", s=W[seg[0]]["s"], e=W[seg[-1]]["e"], chu=" ".join(W[i]["w"] for i in seg)))
    # bẫy: không bao giờ bỏ phủ định (trừ bản lặp của chính nó)
    for i in list(bo):
        if W[i]["t"] in PHU_DINH and i not in nd and not any(x["loai"] in ("hụt", "lặp") and x["s"] <= W[i]["s"] <= x["e"] for x in so):
            bo.discard(i); so.append(dict(loai="GIỮ phủ định", s=W[i]["s"], e=W[i]["e"], chu=W[i]["w"]))
    # khoảng giữ theo từ (không cắt giữa từ)
    spans, cur = [], None
    for i in ws:
        if i in bo:
            if cur: spans.append(cur); cur = None
            continue
        cur = [W[i]["s"], W[i]["e"]] if cur is None else [cur[0], W[i]["e"]]
    if cur: spans.append(cur)
    if spans and ws and ws[0] not in bo: spans[0][0] = min(spans[0][0], a)
    if spans and ws and ws[-1] not in bo: spans[-1][1] = max(spans[-1][1], b)
    # 3) khoảng lặng theo năng lượng
    cp = tim_cum(W, KH["chot"], a, b) if KH.get("chot") else None
    if cp: chot_s = W[cp[0]]["s"]
    ra = []
    for s0, e0 in spans:
        fr = np.arange(int(s0 * 100), min(int(e0 * 100), len(DB)))
        if len(fr) == 0: continue
        db = DB[fr]; nguong = min(-38.0, np.percentile(db, 10) + 9); lang = db < nguong
        khe, k = [], 0
        while k < len(lang):
            if lang[k]:
                j = k
                while j < len(lang) and lang[j]: j += 1
                khe.append((fr[k] / 100, fr[j - 1] / 100 + 0.01)); k = j
            else:
                k += 1
        for p in range(len(ws) - 1):
            g0, g1 = W[ws[p]]["e"], W[ws[p + 1]]["s"]
            if g1 - g0 > LANG_TOI_DA and s0 <= g0 and g1 <= e0 and ws[p] not in bo and ws[p + 1] not in bo:
                q = lang[int(g0 * 100) - fr[0]:int(g1 * 100) - fr[0]]
                if len(q) and q.mean() >= 0.6: khe.append((g0, g1))
                else: so.append(dict(loai="GIỮ khe có tiếng", s=g0, e=g1))
        khe.sort(); gop = []
        for x in khe:
            if gop and x[0] <= gop[-1][1]: gop[-1] = (gop[-1][0], max(gop[-1][1], x[1]))
            else: gop.append(x)
        pos = s0
        for g0, g1 in gop:
            if g1 - g0 <= LANG_TOI_DA or g0 - s0 < 0.05 or e0 - g1 < 0.05: continue
            if chot_s is not None and 0 <= chot_s - g1 < 0.4:
                so.append(dict(loai="GIỮ lặng trước câu chốt", s=g0, e=g1)); continue
            c0, c1 = g0 + LANG_GIU / 2, g1 - LANG_GIU / 2
            ra.append([pos, c0]); pos = c1
            so.append(dict(loai="lặng", s=c0, e=c1, chu=f"{g1 - g0:.2f}s → {LANG_GIU}s"))
        ra.append([pos, e0])
    for s0, e0 in ra:
        if giu_het and 0 <= s0 - giu_het[-1][1] < 1 / FPS: giu_het[-1][1] = e0
        else: giu_het.append([s0, e0])

giu = []
for s0, e0 in giu_het:
    s1, e1 = round(s0 * FPS) / FPS, round(e0 * FPS) / FPS
    if e1 - s1 >= 2 / FPS: giu.append([round(s1, 4), round(e1, 4)])
con = sum(e - s for s, e in giu)
for x in so:
    x["s"], x["e"] = round(x["s"], 3), round(x["e"], 3)
json.dump(dict(giu=giu, so=sorted(so, key=lambda x: x["s"]), tho=round(tho, 2), con=round(con, 2), chot_nguon=chot_s),
          open(g.ra, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
dem = {}
for x in so: dem[x["loai"]] = dem.get(x["loai"], 0) + 1
canh = "  <-- cắt hơn 1/3: xem lại sổ cắt" if con < tho * 2 / 3 else ""
print(f"thô {tho:.1f}s → {con:.1f}s ({con / max(tho, 1e-9):.0%}), {len(giu) - 1} nhát | {dem}{canh}")
