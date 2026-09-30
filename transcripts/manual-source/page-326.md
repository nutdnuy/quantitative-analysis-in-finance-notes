เมื่อ $\lambda(n)=\begin{cases}\sqrt\tau\left(\sqrt{\dfrac{1-p}{p}}\right);\quad\text{probability }p\\-\sqrt\tau\left(\sqrt{\dfrac{p}{1-p}}\right);\quad\text{probability }1-p\end{cases}$ เป็นตัวแปรเชิงสุ่ม สำหรับทุกๆ $n=1,2,...$

โดยเฉพาะอย่างยิ่ง ถ้า $p=0.5$ จะได้ $\lambda(n)=\begin{cases}\sqrt\tau;\quad\text{probability }p\\-\sqrt\tau;\quad\text{probability }1-p\end{cases}$

**ตัวอย่างที่ 9.18** จงเขียน $S(1)$ และ $S(2)$ ในเทอมของ $\mu$, $\sigma$, $\lambda(1)$ และ $\lambda(2)$ เมื่อกำหนดให้ $p=0.5$

**วิธีทำ** เพราะว่า $k(n)=\begin{cases}\mu\tau+\sigma\sqrt\tau;\quad\text{probability }0.5\\\mu\tau-\sigma\sqrt\tau;\quad\text{probability }0.5\end{cases}=\mu\tau+\sigma\lambda(n)$ และ

$$1+K(n)=e^{k(n)}=\begin{cases}e^{\mu\tau+\sigma\sqrt\tau};\quad\text{probability }0.5\\e^{\mu\tau-\sigma\sqrt\tau};\quad\text{probability }0.5\end{cases}$$

จากแผนภาพต้นไม้ทวิภาคจะได้

$$S(1)=\begin{cases}e^{\mu\tau+\sigma\sqrt\tau}S(0);\quad\text{probability }p\\e^{\mu\tau-\sigma\sqrt\tau}S(0);\quad\text{probability }1-p\end{cases}=S(0)e^{\mu\tau+\sigma\lambda(1)}$$

เมื่อ $\lambda(1)=\begin{cases}\sqrt\tau;\quad\text{probability }0.5\\-\sqrt\tau;\quad\text{probability }0.5\end{cases}$

และ

$$S(2)=\begin{cases}e^{2(\mu\tau+\sigma\sqrt\tau)}S(0);\quad\text{probability }0.25\\e^{(\mu\tau+\sigma\sqrt\tau)}e^{(\mu\tau-\sigma\sqrt\tau)}S(0)=e^{2\mu\tau}S(0);\quad\text{probability }0.5\\e^{2(\mu\tau-\sigma\sqrt\tau)}S(0);\quad\text{probability }0.25\end{cases}$$

$$=\begin{cases}e^{2(\mu\tau+\sigma\sqrt\tau)}S(0);\quad\text{probability }0.25\\e^{(\mu\tau+\sigma\sqrt\tau)}e^{(\mu\tau-\sigma\sqrt\tau)}S(0)=e^{2\mu\tau}S(0);\quad\text{probability }0.5\\e^{2(\mu\tau-\sigma\sqrt\tau)}S(0);\quad\text{probability }0.25\end{cases}$$

$$=S(0)e^{2\mu\tau+\sigma(\lambda(1)+\lambda(2))}$$
