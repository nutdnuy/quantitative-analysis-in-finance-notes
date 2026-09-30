เพราะว่า $E[k(n)]=p\ln(1+u)+(1-p)\ln(1+d)=\mu\tau$ (9.55)

และ $\operatorname{Var}[k(n)]=p(\ln(1+u)-E[k(n)])^2+(1-p)(\ln(1+d)-E[k(n)])^2$

$$=p(\ln(1+u)-\mu\tau)^2+(1-p)(\ln(1+d)-\mu\tau)^2=\sigma^2\tau\qquad(9.56)$$

เมื่อแก้ระบบสมการ (9.55) และ (9.56) จะได้

$$\ln(1+u)=\mu\tau+\sigma\sqrt\tau\left(\sqrt{\frac{1-p}{p}}\right)\quad\text{และ}\quad\ln(1+d)=\mu\tau-\sigma\sqrt\tau\left(\sqrt{\frac{p}{1-p}}\right)\qquad(9.57)$$

โดยเฉพาะอย่างยิ่ง ถ้า $p=0.5$ (ความน่าจะเป็นที่หุ้นขึ้นและลงในแต่ละเวลาเท่ากัน) จะได้

$$\ln(1+u)=\mu\tau+\sigma\sqrt\tau\quad\text{และ}\quad\ln(1+d)=\mu\tau-\sigma\sqrt\tau\qquad(9.58)$$

**ตัวอย่างที่ 9.17** จงหา $E[k(n)]$ และ $\operatorname{Var}[k(n)]$ สำหรับทุกๆ $n=1,2,...,12$ เมื่อกำหนด $u=0.02$, $d=-0.01$ และ $p=0.5$

**วิธีทำ** เพราะว่า $E[k(n)]=0.5(\ln(1+u)+\ln(1+d))$ และ

$\operatorname{Var}[k(n)]=0.5(\ln(1+u)-E[k(n)])^2+0.5(\ln(1+d)-E[k(n)])^2$

ดังนั้น $E[k(n)]=0.5(\ln(1+0.02)+\ln(1-0.01))\approx0.0049$

$\operatorname{Var}[k(n)]\approx0.5(\ln(1+0.02)-0.0049)^2+0.5(\ln(1-0.01)-0.0049)^2$

$$\approx0.00022280$$

□

ต่อไปจะเขียน $k(n)$ ในเทอมของ $\mu$ และ $\sigma$ จากสมการ

$$k(n)=\begin{cases}\ln(1+u);\quad\text{probability }p\\\ln(1+d);\quad\text{probability }1-p\end{cases}$$

และจากสูตร (9.57) จะได้ว่า

$$k(n)=\begin{cases}\mu\tau+\sigma\sqrt\tau\left(\sqrt{\dfrac{1-p}{p}}\right);\quad\text{probability }p\\\mu\tau-\sigma\sqrt\tau\left(\sqrt{\dfrac{p}{1-p}}\right);\quad\text{probability }1-p\end{cases}=\mu\tau+\sigma\lambda(n)\qquad(9.58)$$

ดังนั้น $k(n)=\mu\tau+\sigma\lambda(n)$ (9.59)
