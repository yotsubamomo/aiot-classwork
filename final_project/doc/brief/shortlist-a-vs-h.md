# 短名單比較：A. EV 電池健康 Agent vs H. 車輛能耗偵探

> 狀態：比較完成，等待選定 ⑧ 領域（2026-10-24）
> 前提：⑨ 已定為「實作 L2，L3 延伸」；實際一人、週末進行；不能用公司資料。
> 資料來源：兩份平行的網路調查，加上我對關鍵事實的抽查。抽查結果標在「查證狀態」欄；未查證的項目引用前要回頭看原文。

## 結論

建議選 **H. 車輛能耗偵探**，但先花一個週末做資料驗證（spike）再定案。

理由：

1. **IoT 是真的。** H 可以用自己的車（RPi 5 + OBD-II）收集真實資料；A 的 IoT 只能重播資料集。這門課叫 AIoT，去年 20 多組裡只有一組有真實感測資料。
2. **資料單純。** H 只靠一個資料集（VED，Apache-2.0，壓縮後約 180 MB）。A 要整合 NASA、CALCE、Oxford、MATR 好幾種格式，資料工程量大。
3. **研究缺口清楚。** 調查沒有找到用 LLM Agent 解釋行程能耗、做節能駕駛教練的論文。A 的缺口也成立，但電池領域已經有 BatteryAgent 這類 LLM Agent（做故障診斷）。
4. **跟課程接得上。** L6 多元迴歸是自然的 baseline；HW1 用過的氣象署 API 可以用在台灣的即時示範。
5. **跟台灣更相關。** 2025 年台灣新車中電動車約佔 7.9%，路上大多數是燃油車和油電車，而 VED 的主體正好是燃油車和油電車。
6. **工作量較小。** L2 粗估 8–10 個週末，A 粗估 10–12 個週末。

A 的優勢是研究深度和法規題材更強（歐盟電池法、UN GTR 22、Euro 7），如果 H 的資料驗證失敗，A 是穩健的備案。

## 比較表

| 面向 | A. EV 電池健康 | H. 車輛能耗偵探 |
| --- | --- | --- |
| 使用者問題 | 這顆電池還健康嗎、還能用多久、充電習慣傷不傷電池 | 為什麼這個月特別耗油（電）：天氣、路線還是開法？能省多少 |
| 主要資料 | NASA PCoE、CALCE、Oxford、Severson/MATR（實驗室電芯）；Liu 2025 真實車隊資料（GitHub 只有 1 台車的樣本，完整資料要向車廠網站申請） | VED：383 台車一年的 OBD-II 紀錄（264 燃油、92 油電、27 插電／純電） |
| 正確答案 | 每圈實測容量（實驗室）；真實車隊的容量本身是估算值 | 車速、MAF、車外溫度等實測訊號；燃油車油耗要由 MAF 推算 |
| 資料主要限制 | 實驗室電芯和真實車輛差距大；格式多 | 純電車只有 3 台；燃油車只有 43.6% 的紀錄有車外溫度；行程頭尾被裁掉（冷啟動看不到）；資料在美國密西根 |
| 分析任務 | SOH 估計、RUL 預測、異常衰退偵測 | 行程能耗迴歸、把能耗拆成天氣／速度／怠速／空調的貢獻、異常行程偵測、what-if 模擬 |
| Baseline（課堂方法） | L5 自迴歸（RUL）、L6 多元迴歸（SOH） | L6 多元迴歸（行程能耗）、L5 自迴歸（行程內功率） |
| 進階方法 | 梯度提升、高斯過程（含不確定性）、PINN | LightGBM + SHAP、物理模型 + ML 殘差的混合模型、Isolation Forest |
| L3 延伸 | 只能重播資料集模擬 BMS 遙測；可加真實環境溫度感測器 | RPi 5 + OBD-II 讀取器記錄自己的車（只讀、被動記錄） |
| 2025–2026 證據 | Geotab 2026：22,700+ 台 EV 平均每年衰退 2.3%；歐盟電池護照 2027-02-18；UK 調查只有 3% 有信心買二手 EV | Recurrent 2025：0°C 平均剩 78% 續航；NAF 2026 極寒測試平均比 WLTP 少 38%；ICCT：PHEV 實際 CO₂ 是認證值的 3.5–4.6 倍 |
| 技術演進故事 | 等效電路／電化學模型 → 特徵式 ML → DL/Transformer → PINN → LLM Agent | 物理模型（VT-CPEM）→ 迴歸／ML → LSTM/Transformer → 物理 + 殘差混合、不確定性模型 |
| 專家爭論（Deep Research） | 快充到底傷不傷電池；實驗室測試代不代表真實使用；80% SOH 當報廢線合不合理 | 節能駕駛能省多少、效果會不會消退；物理模型 vs 資料驅動；實驗室認證和實際油耗的落差，以及熱天的影響 |
| 研究缺口 | 現有電池 Agent 都做故障診斷，沒有做給消費者的 SOH/RUL 決策 | 沒有找到用 LLM Agent 解釋行程能耗或做節能教練的研究 |
| 和去年題目重疊 | 無 | 無；結構類似去年「天氣預測蔬菜價錢」 |
| L2 工作量粗估 | 10–12 個週末 | 8–10 個週末（L3 再加 3–4 個） |
| 和工作的距離 | 較近（BMS 是車用晶片的應用領域），要自行確認公司對同領域課外研究的規定 | 較遠 |

## A 的重點

**優勢：**

- 法規題材強：歐盟電池法第 14 條要求 BMS 保存 SOH 資訊、電池護照 2027-02-18 強制、UN GTR 22（5 年／10 萬公里內須保有 80% 能量）、Euro 7 納入電池耐久。
- 論文多，技術演進完整，從 Severson 2019 一路到 2024 的 PINN 和 2025 的 BatteryAgent。
- 研究缺口：給消費者或車隊的 SOH/RUL 決策 Agent，結合法規和保固條款。

**風險：**

- 最大的問題是實驗室電芯訓練的模型，能不能對一台真實的二手車給出可信的 SOH。
- 真實車隊資料：Liu 2025 的 GitHub 只有 1 台車的樣本，完整資料要向車廠網站申請，資料授權還沒確認。
- 不能在家自己做電池充放電老化實驗，有熱失控的危險。

## H 的重點

**優勢：**

- VED 的動態資料欄位已確認，包含 `Outside Air Temperature[DegC]`、`Vehicle Speed[km/h]`、`MAF[g/sec]`、`Fuel Rate[L/hr]`、`Air Conditioning Power[kW]`、`Heater Power[Watts]`、`HV Battery SOC[%]` 等。
- `DayNum` 是從 2017-11-01 起算的天數，可以換回真實日期，用來對接 NOAA 的歷史天氣，補上缺少的車外溫度。
- VED 論文的案例：-8°C 時油耗比 20°C 高 46%（中位數 MPG 23.6 vs 34.4），可以直接當 Introduction 的開頭數據。
- 自己的車只要支援標準 OBD-II，就能讀到車速、轉速、MAF、進氣溫度，部分車款還有車外溫度和燃油流量。

**風險：**

- 純電車只有 3 台，所以要把題目定位成「燃油車和油電車為主」，不要宣稱能分析電動車。
- 燃油車的燃油流量欄位幾乎是空的，要依論文的演算法從 MAF 推算，會帶進誤差。
- 行程頭尾被裁掉，所以「預熱車廂能省多少」這類 what-if 不可靠，要避開。
- 模型在密西根訓練、在台灣示範，這個轉移要寫進限制。
- 自己的車要先確認支援哪些 OBD-II 參數；行車中不能操作，警示只能用語音或行程結束後顯示。

## 建議下一步：H 的資料驗證（一個週末）

在定案 ⑧ 之前，先用一個週末確認 H 最大的未知數：VED 能不能撐起可信的行程能耗拆解。

1. 下載 VED，挑出燃油車和油電車的行程，算出每趟行程的特徵（平均車速、加速度、怠速比例、停車次數、車外溫度）。
2. 用 MAF 推算每趟油耗。
3. 跑 L6 多元迴歸，依車輛分組做交叉驗證，看誤差和溫度係數是否合理（是否重現「越冷越耗油」）。
4. 確認自己的車支援哪些 OBD-II 參數（買讀取器之前，可以先查車款的社群資料）。

通過的標準：多元迴歸能重現溫度效應，誤差在可以解釋的範圍內。不通過就改選 A。

## 查證狀態

| 事實 | 狀態 |
| --- | --- |
| VED 欄位、車輛數（264/92/27）、Apache-2.0 授權、7z 封裝 | 已查證（GitHub README） |
| VED 論文 -8°C 比 20°C 油耗高 46% | 已查證（論文） |
| Recurrent：30,000+ 台、0°C 剩 78%、-7°C 剩 70%，2025-11-19 發布 | 已查證 |
| Geotab：22,700+ 台、每年 2.3%、DC 快充重度使用最高 3.0% | 已查證 |
| BatteryAgent（arXiv 2512.24686）做故障診斷，不做 SOH | 已查證 |
| Liu 2025 資料：GitHub 只有 1 台車樣本，完整資料在車廠網站 | 已查證；調查報告說的「CC BY-NC-SA 授權」在 repo 頁面上看不到，未確認 |
| 節能駕駛統合分析：17 篇研究、平均 6.6%、95% CI 4.9–8.3% | 未查證（原網站拒絕存取） |
| 歐盟電池法第 14 條和附錄 VII 的原文 | 未查證（只看到二手引述） |
| NAF 2026、ICCT 2026、台灣 2025 電動車銷量等其餘數據 | 未查證，引用前要看原文 |
| 兩題的工作量估計 | 粗估，不是查證項目 |

## 主要來源

- VED：[github.com/gsoh/VED](https://github.com/gsoh/VED)、[arXiv 1905.02081](https://arxiv.org/abs/1905.02081)
- eVED（加上道路、坡度資訊）：[arXiv 2203.08630](https://arxiv.org/abs/2203.08630)
- Recurrent 冬季續航：[recurrentauto.com](https://www.recurrentauto.com/research/winter-ev-range-loss)
- Geotab 電池衰退：[Electric Autonomy](https://electricautonomy.ca/ev-supply-chain/batteries/2026-01-13/latest-geotab-study-finds-ev-batteries-lose-just-2-3-life-per-year/)
- BatteryAgent：[arXiv 2512.24686](https://arxiv.org/abs/2512.24686)
- Liu 2025 真實車隊 SOH：[Nature Communications](https://pmc.ncbi.nlm.nih.gov/articles/PMC11779878/)、[GitHub](https://github.com/HoraceLiu1010/Multi-modal-SOH-estimation-framework)
- 電池資料集：[NASA PCoE](https://data.nasa.gov/dataset/li-ion-battery-aging-datasets)、[CALCE](https://calce.umd.edu/battery-data)、[Oxford](https://ora.ox.ac.uk/objects/uuid:03ba4b01-cfed-46d3-9b1a-7d4a7bdf6fac)、[BatteryML](https://github.com/microsoft/BatteryML)
- UN GTR 22 摘要：[HORIBA](https://www.horiba.com/twn/mobility/applications/emissions-performance-and-durability/exhaust-emissions/gtr-no22/)
- 節能駕駛統合分析（未查證）：[UC Davis NCST](https://ncst.ucdavis.edu/research-product/average-impact-and-important-features-onboard-eco-driving-feedback-meta-analysis)
- OBD-II 參數：[Wikipedia OBD-II PIDs](https://en.wikipedia.org/wiki/OBD-II_PIDs)、[python-obd](https://python-obd.readthedocs.io/en/latest/)
