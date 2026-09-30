### 9.9.2 การเคลื่อนที่แบบบราวน์เนียน

นิยามตัวแปรเชิงสุ่ม $x(n)$ โดย

$$x(n)=\frac{k(n)-\mu\tau}{\sigma\sqrt\tau}\quad\text{สำหรับทุกๆ }n=1,2,...\qquad(9.68)$$

เนื่องจาก $k(n)$ เป็นตัวแปรเชิงสุ่มอิสระ ดังนั้น $x(n)$ เป็นตัวแปรเชิงสุ่มอิสระด้วย

เพราะว่า $E[k(n)]=\mu\tau$ และ $\operatorname{Var}[k(n)]=\sigma^2\tau$

ดังนั้น จะได้ $E[x(n)]=\dfrac{E[k(n)]-\mu\tau}{\sigma\sqrt\tau}=0$ (9.69)

และ $\operatorname{Var}[x(n)]=\operatorname{Var}[\dfrac{k(n)-\mu\tau}{\sigma\sqrt\tau}]=\dfrac1{\sigma^2\tau}\operatorname{Var}[k(n)]=1$ (9.70)

โดยทฤษฎีลิมิตเข้าสู่ศูนย์กลาง (The Central Limit Theorem) จะได้ว่า

$$\frac{x(1)+x(2)+...+x(n)}{\sqrt n}\to X\quad\text{เมื่อ }n\to\infty\qquad(9.71)$$

โดยที่ $X$ เป็นตัวแปรเชิงสุ่มที่มีการแจกแจงแบบปกติมาตรฐาน ($X\sim N(0,1)$)

**หมายเหตุ** ถ้า $X\sim N(\mu,\sigma^2)$ แล้วฟังก์ชันความหนาแน่นการแจกแจงความน่าจะเป็น คือ

$$f(x)=\frac1{\sigma\sqrt{2\pi}}e^{-\frac12\left(\frac{x-\mu}{\sigma}\right)^2}\qquad(9.72)$$

เนื่องจาก $k(n)=\mu\tau+\sigma\lambda(n)$ ทำให้ได้

$$\lambda(n)=\frac{k(n)-\mu\tau}{\sigma}=\sqrt\tau\frac{k(n)-\mu\tau}{\sigma\sqrt\tau}=\sqrt\tau x(n)\qquad(9.73)$$

กำหนดให้ $\tau=\dfrac1N$ จะได้ $\lambda(n)=\dfrac{x(n)}{\sqrt N}$

เนื่องจาก $w(n)=\lambda(1)+\lambda(2)+...+\lambda(n)$ ดังนั้นจะได้
