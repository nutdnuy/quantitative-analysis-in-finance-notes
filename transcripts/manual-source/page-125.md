**บทนิยาม 4.11** กำหนดให้ $D$ เป็นค่าเสื่อมราคารวม และ อัตราดอกเบี้ยของกองทุนสมมติ $j$ ต่อปี เรียก การกำหนดค่าเสื่อมราคาในปีที่ $t$ โดย

$$D_t=\frac{(1+j)^{t-1}}{s_{\overline{n}|j}}D\qquad(4.17)$$

ว่า *ค่าเสื่อมราคาวิธีเงินทุนจม*

จากนิยามค่าเสื่อมราคาวิธีเงินทุนจมเราสามารถพิจารณา $\dfrac{(1+j)^{t-1}}{s_{\overline{n}|j}}=\dfrac{j(1+j)^{t-1}}{(1+j)^n-1}$ เป็นสัดส่วนของค่าเสื่อมราคาที่ถูกหักเป็นค่าใช้จ่ายของสินทรัพย์ปีที่ $t$ ใดๆ

**ทฤษฎีบท 4.12** กำหนดให้ $D_t$ เป็นค่าเสื่อมราคาวิธีเงินทุนจม จะได้

$$B_t=P_0-\frac{s_{\overline{t}|j}}{s_{\overline{n}|j}}D\qquad(4.18)$$

สำหรับทุกๆ $t=0,1,...,n$

**พิสูจน์** เนื่องจากมูลค่าตามบัญชีปลายปีที่ $t$ , $B_t$ เท่ากับ ราคาของสินทรัพย์หักด้วยค่าเสื่อมราคาตั้งแต่ปีที่ 1 ถึงปีที่ $t$ นั่นคือ

$$\begin{aligned}B_t&=P_0-(D_1+D_2+...+D_t)\\&=P_0-\left(\frac{1}{s_{\overline{n}|j}}D+\frac{(1+j)}{s_{\overline{n}|j}}D+...+\frac{(1+j)^{t-1}}{s_{\overline{n}|j}}D\right)\\&=P_0-\left(\frac{D}{s_{\overline{n}|j}}\right)\left(1+(1+j)+...+(1+j)^{t-1}\right)=P_0-\left(\frac{s_{\overline{t}|j}}{s_{\overline{n}|j}}\right)D\end{aligned}$$

<figure class="source-figure"><div class="source-figure-images"><img src="assets/figures/figure-4-4a.png" width="386" height="315" alt="กราฟค่าเสื่อมราคาวิธีทุนจม"><img src="assets/figures/figure-4-4b.png" width="352" height="344" alt="กราฟมูลค่าตามบัญชีวิธีทุนจม"></div><figcaption><em>รูปที่ 4.4 กราฟแสดงค่าเสื่อม และ มูลค่าตามบัญชีของสินทรัพย์ด้วยวิธีทุนจม</em></figcaption></figure>
