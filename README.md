
# PID 控制器模擬三版本比較

本專案為論文中使用的 PID 控制器模擬，包含三種不同階段的實作方式，分別使用 Jupyter Notebook（ipywidgets）與 PyQt6 GUI，展示程式的演進過程與設計思路。

---

## 📁 檔案說明

### `1.pid_widget_basic.ipynb`
- **開發背景**：最初自寫版本，嘗試使用 `ipywidgets` 模擬 PID 控制器。
- **特色**：介面簡單，能用滑桿調整 Kp/Ki/Kd，並即時更新曲線。
- **限制**：未加入曲線平滑處理，輸出較為跳動。

### `2.pid_widget_improved.ipynb`
- **開發背景**：在第一版基礎上改進，加入 `lowpassFilter` 做曲線平滑。
- **參考來源**：[jeremy7710/Simple-PID](https://github.com/jeremy7710/Simple-PID) 中的圖表曲線處理方法。
- **特色**：模擬曲線更接近實際系統響應。
- **限制**：仍使用 `ipywidgets`，在 PyCharm 中執行需改副檔名為 `.ipynb`，且畫面刷新會閃爍。

### `3.pid_gui_pyqt6.py`
- **開發背景**：最終版本，使用 PyQt6 製作 GUI，改善刷新閃爍問題。
- **參考來源**：[jeremy7710/Simple-PID](https://github.com/jeremy7710/Simple-PID) 的控制邏輯與模擬曲線邏輯。
- **特色**：介面滑順、支援實時滑桿調整參數、不依賴瀏覽器或 Jupyter。

---

## 🛠 執行方式

### Jupyter Notebook 版本
需使用 Jupyter 或 Google Colab 開啟 `.ipynb` 檔案。

```bash
jupyter notebook
```

### PyQt6 GUI 版本
需先安裝 PyQt6：

```bash
pip install PyQt6 matplotlib numpy
```

再執行程式：

```bash
python 3.pid_gui_pyqt6.py
```

---

## 📚 參考資料

- [jeremy7710/Simple-PID](https://github.com/jeremy7710/Simple-PID)：提供 PID 演算法與視覺化範例，為改善版本與 GUI 版的設計參考來源。
