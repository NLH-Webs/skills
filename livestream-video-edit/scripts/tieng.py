"""Làm tiếng cuối cho video đã dựng (giữ nguyên hình): giọng sạch + tiếng động + nhạc nền né giọng
→ chuẩn độ to → nén AAC → ĐO LẠI SAU KHI NÉN, vượt trần thì hạ trần limiter và làm lại.

    python tieng.py dung.mp4 ra.mp4 --nhac bai1.mp3 bai2.mp3 [--sfx sfx.wav] [--rnnoise cb.rnnn]
                    [--lufs -12.7] [--tran -1.0] [--len 0:4 95:100] [--muc-nhac 0.32]

- Giọng lấy từ chính tiếng của dung.mp4 (tiếng thô đã cắt theo hình).
- --rnnoise: mô hình RNNoise cho bộ lọc arnndn (bộ BSD của richardpl/arnndn-models). Không có thì chỉ dùng afftdn.
- --len: các quãng (giây) nhạc được nâng lên (thẻ tiêu đề, thẻ kết) — ngoài quãng này nhạc nằm dưới giọng ~18 LU.
- Nhiều bài nhạc: nối chéo 3s theo thứ tự, không lặp một bài (bài có đuôi tắt dần sẽ tạo "lỗ" giữa video).
Vì sao đo sau AAC: một tiếng động gắt có thể làm đỉnh thật vọt +3 dB khi nén, dù bản WAV đã đạt.
"""
import argparse
import os
import tempfile

from chung import FF, chay, dai, do_tieng

ap = argparse.ArgumentParser()
ap.add_argument("vao"); ap.add_argument("ra")
ap.add_argument("--nhac", nargs="*", default=[]); ap.add_argument("--sfx"); ap.add_argument("--rnnoise")
ap.add_argument("--lufs", type=float, default=-12.7); ap.add_argument("--tran", type=float, default=-1.0)
ap.add_argument("--len", nargs="*", default=[]); ap.add_argument("--muc-nhac", type=float, default=0.32)
g = ap.parse_args()

T = dai(g.vao)
tmp = tempfile.mkdtemp(prefix="tieng-")
p = lambda n: os.path.join(tmp, n)

# 1) giọng sạch: lọc ồn, nén nhẹ, cổng êm giữa câu (m của dynaudnorm ≤ 6, cao hơn sẽ kéo to cả tiếng ồn lúc nghỉ)
rnn = f"arnndn=m='{g.rnnoise.replace(os.sep, '/')}':mix=0.9," if g.rnnoise else ""
af = (f"aresample=48000,pan=mono|c0=0.5*c0+0.5*c1,highpass=f=90,lowpass=f=13500,{rnn}afftdn=nr=10:nf=-48:tn=1,"
      "acompressor=threshold=-26dB:ratio=3:attack=6:release=150:makeup=5,dynaudnorm=f=200:g=11:p=0.9:m=4:r=0.4,"
      "agate=threshold=0.018:ratio=2.5:range=0.2:attack=4:release=220:knee=6,"
      "acompressor=threshold=-16dB:ratio=4:attack=3:release=80:makeup=2,dynaudnorm=f=100:g=5:p=0.95:m=6:r=0.35,"
      f"apad=whole_dur={T:.3f},atrim=0:{T:.3f}")
chay([FF, "-v", "error", "-y", "-i", g.vao, "-vn", "-af", af, "-c:a", "pcm_s24le", p("giong.wav")])

# 2) nhạc nền: nối chéo, vào 1,5s / ra 3s, nâng ở các quãng --len
vao = [p("giong.wav")]
fc = ["[0:a]asplit=2[v1][vsc]", "[vsc]asplit=2[sc1][sc2]"]
n_in = 1
if g.sfx:
    vao.append(g.sfx); fc += [f"[{n_in}:a]aresample=48000,volume=0.9,apad=whole_dur={T:.3f}[sx]",
                              "[sx][sc1]sidechaincompress=threshold=0.126:ratio=4:attack=5:release=250[sd]"]; n_in += 1
else:
    fc.append("[sc1]anullsink")
if g.nhac:
    k0 = n_in
    for f in g.nhac:
        vao.append(f); n_in += 1
    fc += [f"[{k0 + i}:a]aresample=48000,pan=mono|c0=0.5*c0+0.5*c1[m{i}]" for i in range(len(g.nhac))]
    lab = "m0"
    for i in range(1, len(g.nhac)):
        fc.append(f"[{lab}][m{i}]acrossfade=d=3:c1=tri:c2=tri[x{i}]"); lab = f"x{i}"
    quang = [tuple(map(float, q.split(":"))) for q in g.len]
    tang = "+".join(f"between(t,{a:.2f},{b:.2f})" for a, b in quang) or "0"
    fc += [f"[{lab}]apad=whole_dur={T:.3f},atrim=0:{T:.3f},asetpts=N/SR/TB,volume='{g.muc_nhac}*(1+1.24*({tang}))':eval=frame,"
           f"afade=t=in:d=1.5,afade=t=out:st={max(0, T - 3):.3f}:d=3[nh]",
           "[nh][sc2]sidechaincompress=threshold=0.05:ratio=6:attack=30:release=600:makeup=1[nd]"]      # né giọng, nhả chậm
else:
    fc.append("[sc2]anullsink")
tron = "[v1]" + ("[sd]" if g.sfx else "") + ("[nd]" if g.nhac else "")
so = 1 + bool(g.sfx) + bool(g.nhac)
fc.append(f"{tron}amix=inputs={so}:normalize=0,atrim=0:{T:.3f}[mx]" if so > 1 else "[v1]atrim=0:{:.3f}[mx]".format(T))
cmd = [FF, "-v", "error", "-y"]
for f in vao:
    cmd += ["-i", f]
chay(cmd + ["-filter_complex", ";".join(fc), "-map", "[mx]", "-c:a", "pcm_s24le", p("tron.wav")])

# 3) độ to + trần, nén AAC, đo lại trên file nén
gain, tran = 0.0, g.tran - 0.2           # trần limiter bắt đầu thấp hơn đích 0,2 dB
ra_tam = g.ra + ".tmp.mp4"
for _ in range(5):
    for _ in range(10):
        chay([FF, "-v", "error", "-y", "-i", p("tron.wav"), "-af",
              f"volume={gain:.2f}dB,aresample=192000,alimiter=limit={10 ** (tran / 20):.4f}:attack=1:release=60:level=false,aresample=48000",
              "-c:a", "pcm_s24le", p("tieng.wav")])
        I, _tp = do_tieng(p("tieng.wav"))
        if abs(I - g.lufs) < 0.08:
            break
        gain += (g.lufs - I) * 0.9
    chay([FF, "-v", "error", "-y", "-i", g.vao, "-i", p("tieng.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
          "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{T:.3f}", "-movflags", "+faststart", ra_tam])
    I, tp = do_tieng(ra_tam)
    if tp <= g.tran + 0.2:
        break
    tran -= tp - g.tran
os.replace(ra_tam, g.ra)
print(f"{g.ra}: {I} LUFS, {tp} dBTP (đo trên file đã nén)")
