<figure class="source-figure"><img src="assets/figures/example-7-7.png" width="422" height="102" alt="แผนภาพกระแสเงินสดหุ้นสามัญตัวอย่างที่ 7.7"></figure>

จะได้

$$\begin{aligned}\mathcal{D}^{mac}&=\frac{\sum_{k=1}^{\infty}kv^k1.02^{k-1}D}{\sum_{k=1}^{\infty}v^k1.02^{k-1}D}=\frac{\sum_{k=1}^{\infty}kv^k1.02^k}{\sum_{k=1}^{\infty}v^k1.02^k}\\&=\frac{\sum_{k=1}^{\infty}k(1.04)^{-k}(1.02)^k}{\sum_{k=1}^{\infty}(1.04)^{-k}(1.02)^k}=\frac{\sum_{k=1}^{\infty}k\left(1+\dfrac{0.02}{1.02}\right)^{-k}}{\sum_{k=1}^{\infty}\left(1+\dfrac{0.02}{1.02}\right)^{-k}}\\&=\lim_{n\to\infty}\left(\frac{\uparrow a_{\overline{n}|0.02/1.02}}{a_{\overline{n}|0.02/1.02}}\right)=\lim_{n\to\infty}\left(\frac{\dfrac{\ddot{a}_{\overline{n}|0.02/1.02}-nv^n}{0.02/1.02}}{a_{\overline{n}|0.02/1.02}}\right)\\&=\lim_{n\to\infty}\left(\frac{\dfrac{\dfrac{1-(1+0.02/1.02)^{-n}}{(0.02/1.02)(1+0.02/1.02)^{-1}}-n(1+0.02/1.02)^{-n}}{0.02/1.02}}{\dfrac{1-(1+0.02/1.02)^{-n}}{0.02/1.02}}\right)\\&=\frac{1}{(0.02/1.02)(1+0.02/1.02)^{-1}}=52\ \text{ปี}\end{aligned}$$

□

**ดูเรชันเมื่ออัตราดอกเบี้ยแปรเปลี่ยน**

ต่อไปจะศึกษาดูเรชันเมื่ออัตราดอกเบี้ยแปรเปลี่ยน ด้วยการพิจารณาอนุพันธ์ของ $\mathcal{D}^{mac}$ (สูตร 7.11) เทียบกับอัตราดอกเบี้ย $i$ จะได้

$$\frac{d\mathcal{D}^{mac}}{di}=\left(\frac{d\mathcal{D}^{mac}}{dv}\right)\left(\frac{dv}{di}\right)=\left(\frac{d}{dv}\frac{\sum_{k=1}^{n}t_kv^{t_k}p_k}{\sum_{k=1}^{n}v^{t_k}p_k}\right)\left(\frac{d(1+i)^{-1}}{di}\right)$$
