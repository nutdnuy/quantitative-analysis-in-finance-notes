เมื่อ $\lambda(2)=\begin{cases}\sqrt\tau;\quad\text{probability }0.5\\-\sqrt\tau;\quad\text{probability }0.5\end{cases}$ และ $\lambda(1)+\lambda(2)=\begin{cases}2\sqrt\tau;\quad\text{probability }0.25\\0;\quad\text{probability }0.5\\-2\sqrt\tau;\quad\text{probability }0.25\end{cases}$ □

### 9.9.1 การเดินสุ่ม

กำหนดให้ $w(n)$ เป็นตัวแปรเชิงสุ่มนิยาม โดย

$$w(n)=\lambda(1)+\lambda(2)+...+\lambda(n)\quad\text{สำหรับทุกๆ }n=1,2,...\qquad(9.60)$$

และ $w(0)=0$

เราเรียก $w(n)$ ว่า *การเดินสุ่ม* ( Random Walk) และเรียก $w(n)$ ว่า *การเดินสุ่มสมมาตร* (Symmetric Random Walk) ถ้า $\lambda(n)=\begin{cases}\sqrt\tau;\quad\text{probability }0.5\\-\sqrt\tau;\quad\text{probability }0.5\end{cases}$

เห็นได้ชัดว่า $\lambda(n)=w(n)-w(n-1)$ (9.61)

**ทฤษฎีบท 9.31** สำหรับเวลา $t=\tau n$, $n=1,2,...$ จะได้ว่า ราคาหุ้น $S(t)$ อยู่ในรูป

$$S(t)=S(0)e^{\mu t+\sigma w(t)}\qquad(9.62)$$

**พิสูจน์** โดยทฤษฎีบท 9.5,

$$S(t)=S(\tau n)=S(0)e^{k(0,\tau n)}=S(0)e^{k(1\tau)+k(2\tau)+...+k(n\tau)}=S(0)e^{\sum_{i=1}^n k(i\tau)}\qquad(9.63)$$

จากสูตร (9.59), $k(i\tau)=\mu\tau+\sigma\lambda(i\tau)$, $i=1,2,...,n$ เมื่อแทนใน (9.63) จะได้

$$\begin{aligned}S(t)&=S(0)e^{\sum_{i=1}^n(\mu\tau+\sigma\lambda(i\tau))}=S(0)e^{\mu\tau+\sigma\sum_{i=1}^n\lambda(i\tau)}\\&=S(0)e^{\mu n\tau+\sigma w(n\tau)}=S(0)e^{\mu t+\sigma w(t)}\end{aligned}$$

□
