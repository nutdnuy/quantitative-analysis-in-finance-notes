# การวิเคราะห์เชิงปริมาณทางการเงิน

Lecture Notes จากหนังสือ *การวิเคราะห์เชิงปริมาณทางการเงิน* โดย ดร.วิชัย วิทยาเกียรติเลิศ พิมพ์ครั้งที่ 2 พ.ศ. 2560

อ่านออนไลน์ได้ที่ [Quantitative Analysis in Finance Notes](https://nutdnuy.github.io/quantitative-analysis-in-finance-notes/) หลัง GitHub Pages เผยแพร่จากสาขา `main`

หน้าอ่านอ้างอิงโครงสร้างจาก [Quantitative Finance Notes](https://nutdnuy.github.io/quantitative-finance-notes/) มีหน้า Welcome, สารบัญด้านซ้าย, สารบัญหัวข้อในบท, ค้นหาข้อความ, โหมดมืด, ปุ่มพิมพ์ และหน้าแยกตามบททั้ง 10 บท

## เนื้อหา

- ถอดข้อความจาก [PDF ต้นฉบับ](assets/QAF-completed-handbook.pdf) ครบ 369 หน้าที่มีเนื้อหาในบทที่ 1–10 และ 21 หน้าของส่วนต้น/ท้าย รวม 390 หน้า ปกอยู่ในหน้า Welcome และอีก 16 หน้าเป็นหน้าว่างเนื้อหาตามต้นฉบับ
- คงถ้อยคำ ตัวเลข เครื่องหมาย และแม้แต่จุดที่ดูเหมือนคำผิดตามหนังสือ แต่ละหน้ามีลิงก์เปิดหน้า PDF เพื่อเทียบต้นฉบับ
- ข้อความเป็น HTML ที่เลือกคัดลอกได้ สมการใช้ MathML และตารางใช้ HTML ภาพประกอบใช้ภาพจาก PDF ต้นฉบับ
- มี [ไฟล์ Markdown รายบท](chapters/) และ [PDF รายบท](assets/chapters/) ให้ดาวน์โหลด
- หน้า Welcome เป็นหน้าแนะนำของเว็บ ไม่ใช่เนื้อหาบทจากหนังสือ

[สถานะการตรวจเทียบทีละหน้า](REVIEW_STATUS.md) บันทึกจำนวนหน้า วิธีตรวจ และเงื่อนไขก่อนเผยแพร่

## เปิดดูในเครื่อง

```sh
python3 scripts/build_transcript.py --require-complete
python3 scripts/build_site.py
python3 -m http.server 8763 --directory site
```

เปิด [http://localhost:8763/](http://localhost:8763/) เพื่ออ่าน เว็บที่สร้างอยู่ใน `site/` และไม่นำไดเรกทอรีนี้เข้า Git

หากเปลี่ยน PDF ต้นฉบับ ให้เตรียมภาพหน้า PDF รายบท และสารบัญใหม่ด้วย `python3 scripts/prepare_source.py` การเตรียมต้นฉบับต้องมี `pypdf`, `Pillow`, Poppler (`pdftotext`, `pdftoppm`, `pdftohtml`) และ `cwebp` หลังเปลี่ยนต้นฉบับต้องตรวจเทียบและลงชื่อรับรองทุกหน้าใหม่

GitHub Actions จะสร้างและเผยแพร่เว็บเมื่อ push ไปยัง `main` คำสั่งสร้างเว็บสำหรับเผยแพร่จะหยุดหากหน้าใดไม่มีการรับรองตรงกับ PDF และไฟล์ข้อความฉบับปัจจุบัน

## สิทธิ์

หนังสือและเนื้อหาต้นฉบับเป็นลิขสิทธิ์ของผู้เขียน เจ้าของโปรเจกต์แจ้งว่าได้รับอนุญาตจากผู้เขียนให้เผยแพร่ ดู [RIGHTS.md](RIGHTS.md) และ [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
