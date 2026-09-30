ได้รับเงิน $\frac{(1+u)C_d-(1+d)C_u}{(u-d)e^\delta}$ บาท

- ซื้อสัญญาคอลออปชั่น 1 สัญญา จ่ายเงิน $C(0)$ บาท

ดังนั้นจะเหลือเงิน $\frac{C_u-C_d}{u-d}+\frac{(1+u)C_d-(1+d)C_u}{(u-d)e^\delta}-C(0)>0$ บาท (โดยสมมติฐาน)

นำเงินที่เหลือ $\frac{C_u-C_d}{u-d}+\frac{(1+u)C_d-(1+d)C_u}{(u-d)e^\delta}-C(0)$ บาท ไปซื้อตราสารหนี้

ดังนั้นมูลค่าเงินของพอร์ตลงทุนที่เวลา $t=0$ คือ $V(0)=0$

ที่เวลา $t=1$ สามารถทำธุรกรรมได้ดังนี้

- ขายคอลออปชั่น 1สัญญาได้รับเงิน $C(1)=\begin{cases}C_u=\max\{(1+u)S(0)-K,0\};&\uparrow\\C_d=\max\{(1+d)S(0)-K,0\};&\downarrow\end{cases}$ บาท
- ขายตราสารจากที่ลงทุน $\frac{C_u-C_d}{u-d}+\frac{(1+u)C_d-(1+d)C_u}{(u-d)e^\delta}-C(0)$ บาท ได้รับเงิน $(\frac{C_u-C_d}{u-d}+\frac{(1+u)C_d-(1+d)C_u}{(u-d)e^\delta}-C(0))e^\delta$ บาท
- ซื้อหุ้นคืน $\frac{C_u-C_d}{(u-d)S(0)}$ หน่วย จ่ายเงิน $\begin{cases}(1+u)\left(\frac{C_u-C_d}{u-d}\right);&\uparrow\\(1+d)\left(\frac{C_u-C_d}{u-d}\right);&\downarrow\end{cases}$ บาท
- ซื้อตราสารหนี้คืน $\frac{(1+u)C_d-(1+d)C_u}{(u-d)e^\delta A(0)}$ ตราสาร จ่ายเงิน $\frac{(1+u)C_d-(1+d)C_u}{u-d}$ บาท

จะได้

$$\begin{aligned}V(1)&=\begin{cases}C_u;&\uparrow\\C_d;&\downarrow\end{cases}+(C(0)-\frac{C_u-C_d}{u-d}-\frac{(1+u)C_d-(1+d)C_u}{(u-d)e^\delta})e^\delta\\&\quad-\begin{cases}(1+u)\left(\frac{C_u-C_d}{u-d}\right);&\uparrow\\(1+d)\left(\frac{C_u-C_d}{u-d}\right);&\downarrow\end{cases}-\frac{(1+u)C_d-(1+d)C_u}{u-d}\\&=(C(0)-\frac{C_u-C_d}{u-d}-\frac{(1+u)C_d-(1+d)C_u}{(u-d)e^\delta})e^\delta>0\end{aligned}$$

ทำให้ได้ว่า $V(1)>0$ ซึ่งขัดแย้งกับ หลักการปราศจากการค้ากำไร

จากกรณี 1) และ กรณี 2) จึงทำให้สรุปได้ว่า $C(0)=\frac{C_u-C_d}{u-d}+\frac{(1+u)C_d-(1+d)C_u}{(u-d)e^\delta}$ □
