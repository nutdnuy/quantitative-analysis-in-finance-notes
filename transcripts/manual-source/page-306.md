<figure class="source-figure"><img src="assets/figures/figure-9-4.png" width="498" height="386" alt="ความน่าจะเป็นที่หุ้นขึ้นจำนวน i ครั้ง ตั้งแต่ 0 ถึง 10"><figcaption>รูปที่ 9.4 แสดงความน่าจะเป็นที่หุ้นขึ้นจำนวน i ครั้ง i=0,1,...,10</figcaption></figure>

จาก (9.37) ทำให้ได้ ราคาหุ้น $S(n)$ ณ เวลา $n$ เท่ากับ

$$S(n)=(1+u)^i(1+d)^{n-i}S(0)\qquad(9.38)$$

ด้วยความน่าจะเป็น $\binom ni p^i(1-p)^{n-i}$ สำหรับ $i=0,1,...,10$

**ตัวอย่างที่ 9.8** สมมติให้ราคาหุ้น $S(t)$ เป็นไปตามแบบจำลองต้นไม้ทวิภาค จงคำนวณหา $u$ และ $d$ ที่ทำให้ $S(1)=\begin{cases}87;\quad\uparrow\\76;\quad\downarrow\end{cases}$ และ $S(2)=92;\quad\uparrow$

**วิธีทำ** จากแผนภาพต้นไม้ทวิภาค จะได้

$$S(1)=\begin{cases}(1+u)S(0)\\(1+d)S(0)\end{cases}=\begin{cases}87\\76\end{cases}$$

และ

$$S(2)=\begin{cases}(1+u)^2S(0)\\(1+u)(1+d)S(0)\\(1+d)^2S(0)\end{cases}=\begin{cases}92\\?\\?\end{cases}$$

นั่นคือ $(1+u)S(0)=87$ (1)

$(1+d)S(0)=76$ (2)
