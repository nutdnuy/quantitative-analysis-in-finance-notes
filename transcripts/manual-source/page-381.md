พิจารณายูโรเปียนคอลออปชั่น จากสมการ (10.53) จะได้

$$\begin{aligned}C^E(0)&=e^{-\delta T}E^{*}[[S(T)-K]^+]\\&=E^{*}[[S(T)e^{-\delta T}-Ke^{-\delta T}]^+]\\&=E^{*}[[S(0)e^{-\delta T+\mu T+\sigma W(T)}-Ke^{-\delta T}]^+]\\&=E^{*}[[S(0)e^{-(\mu+\frac12\sigma^2)T+\mu T+\sigma W(T)}-Ke^{-\delta T}]^+]\\&=E^{*}[[S(0)e^{-\frac12\sigma^2T+\sigma W(T)}-Ke^{-\delta T}]^+]\end{aligned}$$

$$=\int_{-d_2\sqrt{T}}^{\infty}\left(S(0)e^{-\frac12\sigma^2T+\sigma x}-Ke^{-\delta T}\right)\frac{1}{\sqrt{2\pi T}}e^{-x^2/(2T)}dx$$

$$=S(0)\int_{-d_2\sqrt{T}}^{\infty}e^{-\frac12\sigma^2T+\sigma x}\frac{1}{\sqrt{2\pi T}}e^{-x^2/(2T)}dx-Ke^{-\delta T}\int_{-d_2\sqrt{T}}^{\infty}\frac{1}{\sqrt{2\pi T}}e^{-x^2/(2T)}dx$$

$$=S(0)\int_{-d_2\sqrt{T}}^{\infty}\frac{1}{\sqrt{2\pi T}}e^{-(x^2-2T\sigma x+\sigma^2T^2)/(2T)}dx-Ke^{-\delta T}\int_{-d_2\sqrt{T}}^{\infty}\frac{1}{\sqrt{2\pi T}}e^{-x^2/(2T)}dx$$

$$=S(0)\int_{-d_2\sqrt{T}}^{\infty}\frac{1}{\sqrt{2\pi T}}e^{-(x-\sigma T)^2/(2T)}dx-Ke^{-\delta T}\int_{-d_2}^{\infty}\frac{1}{\sqrt{2\pi}}e^{-y^2/2}dy$$

$$=S(0)\int_{-d_1}^{\infty}\frac{1}{\sqrt{2\pi}}e^{-y^2/2}dy-Ke^{-\delta T}\int_{-d_2}^{\infty}\frac{1}{\sqrt{2\pi}}e^{-y^2/2}dy$$

นั่นคือ

$$C^E(0)=S(0)N(d_1)-Ke^{-\delta T}N(d_2)\qquad(10.61)$$

เมื่อ $d_1=\dfrac{\ln\dfrac{S(0)}{K}+(\delta+0.5\sigma^2)T}{\sigma\sqrt{T}}$, $d_2=\dfrac{\ln\dfrac{S(0)}{K}+(\delta-0.5\sigma^2)T}{\sigma\sqrt{T}}$ และ

$$N(x)=\int_{-\infty}^{x}\frac{1}{\sqrt{2\pi}}e^{-y^2/2}dy=\int_{-x}^{\infty}\frac{1}{\sqrt{2\pi}}e^{-y^2/2}dy\qquad(10.62)$$

จะเห็นว่า $N(x)$ เป็นฟังก์ชันค่าสะสมของการกระจายความน่าจะเป็นแบบปกติมาตรฐาน $N(0,1)$ นั่นคือ $N(x)=P(z\leq x)=P(z\geq-x)$ ดังนั้นสามารถคำนวณค่า $N(x)$ ได้จากตารางความน่าจะเป็นสะสมของการแจงแจงแบบปกติซึ่งปรากฏอยู่ในภาคผนวก หรือเพื่อความสะดวกอาจจะใช้คำสั่งฟังก์ชัน NORMSDIST(z) ในโปรแกรม EXCEL ก็ได้
