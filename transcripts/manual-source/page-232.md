$$\begin{aligned}&=\left(\frac{\left(\sum_{k=1}^{n}v^{t_k}p_k\right)\left(\sum_{k=1}^{n}(t_k)^2v^{t_k-1}p_k\right)-\left(\sum_{k=1}^{n}t_kv^{t_k}p_k\right)\left(\sum_{k=1}^{n}t_kv^{t_k-1}p_k\right)}{\left(\sum_{k=1}^{n}v^{t_k}p_k\right)^2}\right)(-v^2)\\&=\left(\frac{\left(\sum_{k=1}^{n}v^{t_k}p_k\right)\left(\sum_{k=1}^{n}(t_k)^2v^{t_k}p_k\right)-\left(\sum_{k=1}^{n}t_kv^{t_k}p_k\right)\left(\sum_{k=1}^{n}t_kv^{t_k}p_k\right)}{\left(\sum_{k=1}^{n}v^{t_k}p_k\right)^2}\right)(-v)\\&=\left(\frac{\sum_{k=1}^{n}(t_k)^2v^{t_k}p_k}{\sum_{k=1}^{n}v^{t_k}p_k}-(\mathcal{D}^{mac})^2\right)(-v)\\&=\left(\frac{\sum_{k=1}^{n}(t_k-\mathcal{D}^{mac})^2v^{t_k}p_k}{\sum_{k=1}^{n}v^{t_k}p_k}\right)(-v)\end{aligned}$$

เพราะว่า $\dfrac{\sum_{k=1}^{n}(t_k-\mathcal{D}^{mac})^2v^{t_k}p_k}{\sum_{k=1}^{n}v^{t_k}p_k}>0$ และ $-v<0$ ดังนั้น $\dfrac{d\mathcal{D}^{mac}}{di}<0$

นั่นแสดงว่า $\mathcal{D}^{mac}$ เป็นฟังก์ชันลดในตัวแปร $i$ หรือกล่าวอีกนัยหนึ่งคือ อัตราผลตอบแทน $i$ เพิ่มขึ้น ก็ต่อเมื่อ ดูเรชันแมคคอเลย์ ลดลง ซึ่งหมายความว่า ถ้าอัตราผลตอบแทนเพิ่มขึ้นจะได้รับเงินคืนกลับมาเร็ว

**ความไว**

ต่อไปจะพิจารณาดูเรชันแมคคอเลย์ในเทอมของอนุพันธ์ของฟังก์ชันมูลค่าปัจจุบัน เราทราบว่าฟังก์ชันมูลค่าปัจจุบันรวมของเงินสดรับ $P(i)=\sum_{k=1}^{n}v^{t_k}p_k$ โดยที่ $v=\dfrac{1}{1+i}$ หากพิจารณาอนุพันธ์ของ $P$ เทียบกับ อัตราดอกเบี้ย $i$ จะได้

$$\begin{aligned}\frac{dP(i)}{di}&=\frac{d}{di}\left(\sum_{k=1}^{n}v^{t_k}p_k\right)\frac{dv}{di}\\&=\left(\sum_{k=1}^{n}t_kv^{t_k-1}p_k\right)(-(1+i)^{-2})=-v\sum_{k=1}^{n}t_kv^{t_k}p_k\qquad(7.14)\end{aligned}$$
