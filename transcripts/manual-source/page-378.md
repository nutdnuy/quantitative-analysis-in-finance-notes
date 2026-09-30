เราสามารถคำนวณราคา $P^A(0)$ ได้เช่นเดียวกับกรณีที่หุ้นอ้างอิงไม่มีการจ่ายเงินปันผล โดยเริ่มจากคำนวณมูลค่าแฝงของพุทออปชั่น ได้ดังนี้

<figure class="source-figure"><img src="assets/figures/example-10-17-intrinsic.png" alt="ต้นไม้มูลค่าแฝงของพุทออปชั่นหลังหักปันผล"></figure>

ต่อไปคำนวณ

$$ (1.05^{-1})(0.75[100-1.1S(1)]^++0.25[100-0.9S(1)]^+)$$

$$=(1.05^{-1})\left(0.75\begin{Bmatrix}0\\15.90\end{Bmatrix}+0.25\begin{Bmatrix}15.90\\32.10\end{Bmatrix}\right)$$

$$=\begin{Bmatrix}(1.05^{-1})(0.75(0)+0.25(15.90))\\(1.05^{-1})(0.75(15.90)+0.25(32.10))\end{Bmatrix}=\begin{Bmatrix}3.7857\\19\end{Bmatrix}$$

เพื่อความสะดวกกำหนดให้

$$f_1(x)=\max\{[100-x]^+,(1.05^{-1})[0.75[100-1.1x]^++0.25[100-0.9x]^+]\}$$

จะได้

$$\begin{aligned}f_1(S(1))&=\max\{[100-S(1)]^+,(1.05^{-1})[0.75[100-1.1S(1)]^+\\&\hspace{7em}+0.25[100-0.9S(1)]^+]\}\\&=\max\left\{\begin{Bmatrix}1\\19\end{Bmatrix},\begin{Bmatrix}3.7857\\19\end{Bmatrix}\right\}=\begin{Bmatrix}3.7857\\19\end{Bmatrix}\end{aligned}$$

ดังนั้นจากลำดับของราคาพุทออปชั่นได้ดังนี้

$$P^A(2)=[100-S(2)]^+=\begin{cases}0&;\uparrow\uparrow\\15.9&;\uparrow\downarrow\text{ or }\downarrow\uparrow\\32.1&;\downarrow\downarrow\end{cases}$$

$$P^A(1)=f_1(S(1))=\begin{Bmatrix}3.7857\\19\end{Bmatrix}$$

$$P^A(0)=\max\{10,(1.05)^{-1}(0.75(3.7857)+0.25(19))\}=\max\{10,7.2279\}=10$$

นั่นคือ ราคาของพุทออปชั่น $P^A(0)=10$ บาท $\square$
