$$\begin{aligned}E[e^{-\delta t}S(t)]&=E[S(0)e^{-\delta t+\mu t+\sigma W(t)}]\\&=S(0)E[e^{-\delta t+\mu t+\sigma W(t)}]\\&=S(0)\int_{-\infty}^{\infty}e^{-\delta t+\mu t+\sigma x}\frac{1}{\sqrt{2\pi t}}e^{-x^2/(2t)}dx\\&=S(0)\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi t}}e^{(-\delta+\mu+\frac12\sigma^2)t-(x-\sigma t)^2/(2t)}dx\\&=S(0)e^{(-\delta+\mu+\frac12\sigma^2)t}\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi t}}e^{-(x-\sigma t)^2/(2t)}dx\\&=S(0)e^{(-\delta+\mu+\frac12\sigma^2)t}\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi t}}e^{-y^2/(2t)}dy\\&=S(0)e^{(-\delta+\mu+\frac12\sigma^2)t}\qquad(10.57)\end{aligned}$$

จาก (10.57) จะเห็นว่าค่าคาดหวังของมูลค่าปัจจุบัน $S(t)$ ไม่ควรขึ้นกับเวลา $t$ นั่นคือ อัตราดอกเบี้ยทบต้นต่อเนื่อง $\delta$ จะต้องเท่ากับ $\mu+\dfrac12\sigma^2$ ซึ่งจะทำให้ $E[e^{-\delta t}S(t)]=S(0)$ ดังนั้นเงื่อนไข $\delta=\mu+\dfrac12\sigma^2$ เป็นเงื่อนไขที่เพียงพอและจำเป็นที่ทำให้มีความน่าจะเป็นความเป็นกลางต่อความเสี่ยง $p^{*}$ ซึ่ง

$$E^{*}[e^{-\delta t}S(t)]=S(0)\qquad(10.58)$$

การแสดงว่ามีความน่าจะเป็นความเป็นกลางต่อความเสี่ยง $p^{*}$ มีความยุ่งยากซับซ้อน ซึ่งในที่นี้จะไม่กล่าวถึงบทพิสูจน์

**ทฤษฎีบท 10.21** ให้ $S(t)$ เป็นราคาหุ้น ซึ่งเป็นราคาที่จะทราบ ที่เวลา $t=s$ ค่าคาดหวังความเป็นกลางต่อความเสี่ยงแบบมีเงื่อนไขของ $S(t)$ จะเท่ากับ

$$E^{*}[S(t)e^{-\delta t}\mid S(s)]=S(s)e^{-\delta s}\qquad(10.59)$$

**บทแทรก 10.22 (สมบัติของมาร์ทิงเกล)** กำหนดให้ $\widetilde{S}(s)=S(s)e^{-\delta s}$ เป็นราคาหุ้นส่วนลด ภายใต้ความน่าจะเป็นความเป็นกลางต่อความเสี่ยง จะได้ว่า

$$E^{*}[\widetilde{S}(t)\mid S(s)]=\widetilde{S}(s)\quad\text{สำหรับทุกๆ }t\geq s\geq0\qquad(10.60)$$
