พิจารณา $S(t+\tau)-S(t)$ สำหรับ $t=\tau n$, $n=1,2,...$ เมื่อ $\tau=\dfrac1N$ และ $N\to\infty$

ในที่นี้จะประมาณ $S(t+\tau)-S(t)$ ในเทอมของ $\tau$ ซึ่งมีดีกรีไม่เกินดีกรี 1

จากทฤษฎีบท 9.31 จะได้ว่า

$$\begin{aligned}S(t+\tau)-S(t)&=S(0)e^{\mu(t+\tau)+\sigma w(t+\tau)}-S(0)e^{\mu t+\sigma w(t)}\\&=S(0)e^{\mu t+\sigma w(t)}\left(e^{\mu\tau+\sigma(w(t+\tau)-w(t))}-1\right)\\&=S(t)\left(e^{\mu\tau+\sigma(w(t+\tau)-w(t))}-1\right)\end{aligned}\qquad(9.64)$$

โดยการกระจายอนุกรมเทย์เลอร์ของ $e^x$ รอบจุด 0 ซึ่ง $e^x\approx1+x+\dfrac{x^2}2$ ทำให้ได้

$$\begin{aligned}S(t+\tau)-S(t)&\approx S(t)\left(1+\mu\tau+\sigma(w(t+\tau)-w(t))+\frac{(\mu\tau+\sigma(w(t+\tau)-w(t)))^2}2-1\right)\\&\approx S(t)\left(\mu\tau+\sigma(w(t+\tau)-w(t))+\sigma\mu\tau(w(t+\tau)-w(t))+\frac{\sigma^2(w(t+\tau)-w(t))^2}2\right)\end{aligned}\qquad(9.65)$$

เพราะว่า $(w(t+\tau)-w(t))^2=\lambda^2(t+\tau)=\tau$ ดังนั้น

$$S(t+\tau)-S(t)\approx S(t)\left(\mu\tau+\sigma(w(t+\tau)-w(t))+\sigma\mu\tau(w(t+\tau)-w(t))+\frac{\sigma^2\tau}2\right)\qquad(9.66)$$

เพราะว่า $\sigma\mu\tau(w(t+\tau)-w(t))=\sigma\mu\tau\lambda(t+\tau)$ ซึ่งเป็นนิพจน์ของ $\tau$ ดีกรีเกิน 1

ดังนั้น $S(t+\tau)-S(t)\approx\left(\mu+\dfrac{\sigma^2}2\right)S(t)\tau+\sigma(w(t+\tau)-w(t))S(t)$ (9.67)

เนื่องจาก $t=n\tau$ เมื่อ $\tau=\dfrac1N$ ดังนั้น ราคาและการเดินเชิงสุมเชิงสมมาตรที่เวลา $t$ จึงขึ้นอยู่กับพารามิเตอร์ $N$ เพื่อให้สอดคล้องกันจะเขียนแทนราคาและการเดินเชิงสุ่มเชิงสมมาตรที่เวลา $t$ สำหรับ $N=1,2,...$ ด้วย $S_N(t)$ และ $w_N(t)$ ตามลำดับ ดังนั้น สมการ (9.67) สามารถเขียนได้ในรูป
