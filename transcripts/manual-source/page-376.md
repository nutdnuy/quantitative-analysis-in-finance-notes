<figure class="source-figure"><img src="assets/figures/example-10-16-stock.png" alt="ต้นไม้ราคาหุ้นอ้างอิงของตัวอย่างที่ 10.16"></figure>

ในที่นี้ $r=0.20/4=0.05$ ต่อคาบเวลา และคำนวณความน่าจะเป็นความเป็นกลางต่อความเสี่ยง

$$p^{*}=\frac{0.05+0.1}{0.1+0.1}=0.75$$

เราจะคำนวณ $P^A(0)$ จาก (10.54) โดยการสร้างลำดับราคาของพุทออปชั่น ดังนี้

$$P^A(2)=[100-S(2)]^+$$

$$\begin{aligned}P^A(1)&=\max\{[100-S(1)]^+,(1+r)^{-1}[p^{*}[100-(1+u)S(1)]^+\\&\hspace{6em}+(1-p^{*})[100-(1+d)S(1)]^+]\}\equiv f_1(S(1))\end{aligned}$$

$$P^A(0)=\max\{f(S(0)),(1+r)^{-1}[p^{*}f_1((1+u)S(0))+(1-p^{*})f_1((1+d)S(0))]\}$$

ต่อไปคำนวณค่าต่างๆ ที่เกี่ยวข้องดังนี้

คำนวณมูลค่าแฝง $[100-S(t)]^+$, $t=0,1,2$ ซึ่งแสดงได้ด้วยต้นไม้ดังนี้

<figure class="source-figure"><img src="assets/figures/example-10-16-intrinsic.png" alt="ต้นไม้มูลค่าแฝงของพุทออปชั่นตัวอย่างที่ 10.16"></figure>

ต่อไปคำนวณ

$$ (1.05^{-1})(0.75[100-1.1S(1)]^++0.25[100-0.9S(1)]^+)$$

$$=(1.05^{-1})\left(0.75\left[100-\begin{Bmatrix}108.9\\89.1\end{Bmatrix}\right]^++0.25\left[100-\begin{Bmatrix}89.1\\72.9\end{Bmatrix}\right]^+\right)$$

$$=(1.05^{-1})\left(0.75\begin{Bmatrix}0\\10.9\end{Bmatrix}+0.25\begin{Bmatrix}10.9\\27.1\end{Bmatrix}\right)=\begin{Bmatrix}2.5952\\14.2381\end{Bmatrix}$$
