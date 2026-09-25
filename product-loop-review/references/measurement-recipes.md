# Công thức đo trong trang

Chạy bằng công cụ chạy JS của trình duyệt tự động (vd `javascript_tool`). Mỗi đoạn trả về một object — dán thẳng con số vào bảng phản hồi.

> Ảnh chụp khi giả lập viewport rộng thường bị thu nhỏ, khó đọc. **Tin phép đo hơn tin mắt**: đo bằng `getBoundingClientRect` / `getComputedStyle`, ảnh chỉ để minh hoạ.

## Vùng chạm nhỏ (chuẩn 44px)
```js
[...document.querySelectorAll('button, a, [role=tab], input')]
  .filter(e => { const r = e.getBoundingClientRect(); return r.width && r.height && r.height < 40 && r.top < innerHeight; })
  .map(e => `${Math.round(e.getBoundingClientRect().height)}px ${(e.textContent || e.title || e.placeholder || '').trim().slice(0, 20)}`)
```

## Cuộn ngang / phần tử tràn
```js
({
  pageOverflowX: document.documentElement.scrollWidth > innerWidth,
  sideScrollers: [...document.querySelectorAll('*')]
    .filter(e => e.scrollWidth > e.clientWidth + 2 && /(auto|scroll)/.test(getComputedStyle(e).overflowX))
    .map(e => e.className.toString().slice(0, 60)),
})
```

## Input làm iOS phóng to (chữ < 16px)
```js
[...document.querySelectorAll('input, textarea, select')].map(i => getComputedStyle(i).fontSize)
```

## Modal có nằm trong màn hình không
```js
const d = document.querySelector('[role=dialog]'); const r = d.getBoundingClientRect();
({ left: r.left, right: r.right, vw: innerWidth, fits: r.left >= 0 && r.right <= innerWidth })
```

## Cuộn lồng nhau (hai thanh cuộn tranh nhau)
```js
[...document.querySelectorAll('*')].filter(e => /(auto|scroll)/.test(getComputedStyle(e).overflowY) && e.scrollHeight > e.clientHeight + 2).map(e => e.className.toString().slice(0, 60))
```

## Hiệu ứng nào chạy khi gõ
Cài bộ ghi, gõ vài chữ, đọc lại:
```js
window.__anim = []; window.__mut = 0;
const rec = e => window.__anim.push(`${e.type}:${e.animationName || e.propertyName}@${String(e.target.className).slice(0, 50)}`);
['animationstart', 'transitionstart'].forEach(t => document.addEventListener(t, rec, true));
new MutationObserver(m => { window.__mut += m.length; }).observe(document.body, { subtree: true, childList: true });
// … gõ … rồi:
({ mutations: window.__mut, anim: [...new Set(window.__anim)] })
```
Không có animation mà vẫn "trông kỳ" → thường là **focus**: đọc `getComputedStyle(input).outline` — hệ thiết kế hay vẽ vòng focus lên input nằm trong một khung đã có viền.

## Dark mode — màu thật, không đoán
```js
document.documentElement.classList.add('dark'); // hoặc cách repo bật dark
const el = document.querySelector('h3'); const cs = getComputedStyle(el);
({ color: cs.color, bg: getComputedStyle(el.closest('[class*=bg-]') || document.body).backgroundColor })
```
Nhớ tắt lại và **tải lại trang** trước khi kiểm light mode (class bật tay + class app tự quản có thể chồng nhau giữa lúc chuyển).

## Múi giờ
```js
({ tz: Intl.DateTimeFormat().resolvedOptions().timeZone, offsetMin: -new Date().getTimezoneOffset() })
```
So giá trị lưu (vd `…T18:00:00+07:00`) với chữ hiện ra. Máy người đo không ở múi giờ nghiệp vụ là cơ hội tốt để bắt lỗi này.

## Biểu đồ có vẽ thật không (hay chỉ ảnh chụp trống)
```js
[...document.querySelectorAll('.rounded-2xl')].map(c => ({ h: Math.round(c.getBoundingClientRect().height), svg: !!c.querySelector('svg'), text: c.textContent.slice(0, 40) }))
```
Ảnh chụp giữa lúc cuộn hay trắng một mảng — kiểm bằng DOM trước khi kết luận "biểu đồ hỏng".

## Thử luồng có `window.confirm` mà không treo trình duyệt
Hộp thoại gốc chặn mọi lệnh tự động. Tạm thay rồi trả lại:
```js
const o = window.confirm; const asked = [];
window.confirm = m => { asked.push(m); return false; };  // bấm "Huỷ"
document.querySelector('.close-btn').click();
window.confirm = o;
({ asked, stillOpen: !!document.querySelector('[role=dialog]') })
```

## Tìm nút theo chữ (khi `find` không ra)
```js
[...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Chi tiết')?.click()
```

## Luật đằng sau (không phải JS)
- Tìm luật lọc/lưu trữ ở backend: `git grep -n "window === 'recent'"` hoặc tên tham số API.
- Tìm lời hứa bị bỏ quên: `git grep -n "SLA_"`, class CSS không ai dùng.
- Luôn đọc **nhánh được deploy** (vd `origin/dev`), không đọc thư mục làm việc có thể cũ.
