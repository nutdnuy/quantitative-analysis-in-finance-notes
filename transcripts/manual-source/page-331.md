$$S_N\left(t+\frac1N\right)-S_N(t)\approx\left(\mu+\frac{\sigma^2}2\right)S_N(t)\frac1N+\sigma\left(w_N\left(t+\frac1N\right)-w_N(t)\right)S_N(t)\qquad(9.76)$$

ถ้ากำหนดให้ $N\to\infty$ จะได้ว่า $S_N(t)\to S(t)$ สำหรับบางตัวแปรเชิงสุ่ม $S(t)$

ดังนั้น จากสมการ (9.76) แบบจำลองราคาหุ้น $S(t)$ สำหรับเวลาต่อเนื่องจึงอยู่ในรูป

$$dS(t)=\left(\mu+\frac{\sigma^2}2\right)S(t)dt+\sigma S(t)dW(t)\qquad(9.77)$$

หรืออยู่ในอีกรูปหนึ่งคือ

$$\frac{dS(t)}{dt}=\left(\mu+\frac{\sigma^2}2\right)S(t)+\sigma S(t)\frac{dW(t)}{dt}\qquad(9.78)$$

เมื่อ $dS(t)=S(t+dt)-S(t)$ และ $dW(t)=W(t+dt)-W(t)$ เป็นส่วนเพิ่มของตัวแปรเชิงสุ่ม $S(t)$ และ $W(t)$ เหนือช่วงเวลาเล็กๆ $dt$

และในทำนองเดียวกัน จากสูตร (9.62) สำหรับเวลาไม่ต่อเนื่อง $t=n\tau$ เมื่อ $\tau=\dfrac1N$ จะได้ว่า

$$S_N(t)=S(0)e^{\mu t+\sigma w_N(t)}\qquad(9.79)$$

และถ้าให้ $N\to\infty$ จะได้ว่า สำหรับเวลาต่อเนื่อง $t\geq0$,

$$S(t)=S(0)e^{\mu t+\sigma W(t)}\qquad(9.80)$$

หากดำเนินการด้วยลอการิทึมฐานธรรมชาติทั้งสองข้าง จะได้

$$\ln S(t)=\ln S(0)+\mu t+\sigma W(t)\qquad(9.81)$$

และเขียนได้ในอีกรูปหนึ่งเป็น

$$\ln\frac{S(t)}{S(0)}=\mu t+\sigma W(t)\qquad(9.82)$$

เพราะว่า $W(t)\sim N(0,t)$ ดังนั้น $\ln S(t)\sim N(\ln S(0)+\mu t,\sigma^2t)$
