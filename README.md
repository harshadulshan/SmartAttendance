<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=200&section=header&text=Smart%20Attendance%20System&fontSize=50&fontColor=fff&animation=twinkling&fontAlignY=38&desc=AI-Powered%20Face%20Recognition%20Attendance&descAlignY=58&descSize=18"/>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=22&duration=3000&pause=1000&color=00D9FF&center=true&vCenter=true&width=700&height=60&lines=🎯+Real-time+Face+Recognition;📊+Live+Analytics+Dashboard;🔒+Secure+%26+Professional;🌙+Dark+%2F+☀️+Light+Theme;📧+Auto+Email+Reports)](https://git.io/typing-svg)

<br/>

![Python](https://img.shields.io/badge/Python-3.14-0D1117?style=for-the-badge&logo=python&logoColor=00D9FF)
![OpenCV](https://img.shields.io/badge/OpenCV-Latest-0D1117?style=for-the-badge&logo=opencv&logoColor=A855F7)
![Dash](https://img.shields.io/badge/Dash-Plotly-0D1117?style=for-the-badge&logo=plotly&logoColor=00D9FF)
![Pandas](https://img.shields.io/badge/Pandas-Latest-0D1117?style=for-the-badge&logo=pandas&logoColor=A855F7)

<br/>

![GitHub stars](https://img.shields.io/github/stars/harshadulshan/SmartAttendance?style=for-the-badge&color=F59E0B)
![GitHub forks](https://img.shields.io/github/forks/harshadulshan/SmartAttendance?style=for-the-badge&color=A855F7)
![GitHub last commit](https://img.shields.io/github/last-commit/harshadulshan/SmartAttendance?style=for-the-badge&color=00D9FF)
![License](https://img.shields.io/github/license/harshadulshan/SmartAttendance?style=for-the-badge&color=22C55E)

</div>

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 🎯 What is This?

<table>
<tr>
<td width="60%" valign="top">

A **production-ready AI Attendance System** that uses **Face Recognition** to automatically identify and mark attendance in real-time via webcam.

No more manual roll calls. No more proxy attendance. Just show your face — the system does the rest! 🤖

Built with **Python**, **OpenCV**, and **Dash** — packaged with a beautiful live analytics dashboard.

</td>
<td width="40%" align="center" valign="top">

<img src="https://user-images.githubusercontent.com/74038190/229223263-cf2e4b07-2615-4f87-9c38-e37600f8381a.gif" width="250"/>

</td>
</tr>
</table>

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Features
- 📸 **Face Registration** — Register with name & ID
- 🤖 **AI Face Recognition** — Real-time detection
- ✅ **Auto Attendance** — Mark present instantly
- 🔴 **Late Arrival Detection** — Track punctuality
- ⚠️ **Unknown Face Alerts** — Security monitoring
- 📷 **Multi-Camera Support** — Use multiple webcams
- 🔍 **Duplicate Detection** — Prevent double marking

</td>
<td width="50%">

### 📊 Dashboard Features
- 🌙 **Dark / ☀️ Light Theme** — Toggle anytime
- 📅 **Today Tab** — Real-time attendance view
- 📆 **Weekly Reports** — 7-day trend analysis
- 🗓️ **Monthly Reports** — Full month analytics
- 🗺️ **Attendance Heatmap** — Pattern visualization
- 📥 **Export to Excel** — One click download
- 📧 **Auto Email Reports** — Daily summaries
- 🔒 **Password Protected** — Secure access

</td>
</tr>
</table>

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 📸 Screenshots

### 🌙 Dark Mode Dashboard
> Clean dark interface with real-time stats and charts

![Dark Dashboard](today_dark.PNG)

---

### ☀️ Light Mode Dashboard
> Elegant light theme for daytime use

![Light Dashboard](today_light.PNG)

---

### 📆 Weekly Analytics
> Track attendance trends across the week

![Weekly](weekly.PNG)

---

### 🗓️ Monthly Heatmap
> Visualize attendance patterns with interactive heatmap

![Monthly](monthly.PNG)

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 🛠️ Tech Stack

<div align="center">

| Category | Technology |
|---|---|
| **Language** | Python 3.14 |
| **Face Recognition** | OpenCV LBPH |
| **Dashboard** | Dash + Plotly |
| **Data Management** | Pandas |
| **Excel Export** | OpenPyXL |
| **Email Reports** | SMTP + MIMEText |
| **Authentication** | Dash-Auth |
| **Camera** | OpenCV VideoCapture |

</div>

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/harshadulshan/SmartAttendance.git
cd SmartAttendance
```

### 2️⃣ Install Dependencies
```bash
pip install opencv-python mediapipe pandas dash plotly openpyxl dash-auth
```

### 3️⃣ Register Faces
```bash
python register.py
```

### 4️⃣ Mark Attendance
```bash
python attendance.py
```

### 5️⃣ Launch Dashboard
```bash
python dashboard.py
```
Then open 👉 **http://127.0.0.1:8050**

### 6️⃣ Send Email Report
```bash
python email_report.py
```

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 📁 Project Structure

```
SmartAttendance/
│
├── 📄 register.py          ← Face registration + model training
├── 📄 attendance.py        ← Real-time attendance marking
├── 📄 dashboard.py         ← Live analytics dashboard
├── 📄 multi_camera.py      ← Multi-camera support
├── 📄 email_report.py      ← Auto email reports
│
├── 📁 dataset/             ← Registered face images (gitignored)
├── 📁 attendance/          ← Attendance CSV files (gitignored)
├── 📁 snapshots/           ← Attendance snapshots (gitignored)
└── 📁 unknown_faces/       ← Unknown detections (gitignored)
```

---

## 🎮 Controls

| Key | Action |
|---|---|
| **Q** | Quit camera window |
| **C** | Clear canvas |
| **Ctrl+C** | Stop dashboard server |

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## ⚙️ Configuration

### Dashboard Login
```python
# In dashboard.py
VALID_USERS = {
    'admin' : 'your_password_here',
}
```

### Email Setup
```python
# In email_report.py
EMAIL_CONFIG = {
    'sender_email'    : 'your_email@gmail.com',
    'sender_password' : 'your_app_password',
    'receiver_email'  : 'receiver@gmail.com',
}
```

### Late Arrival Time
```python
# In attendance.py
LATE_ARRIVAL_HOUR   = 9   # After 9:00 AM = Late
LATE_ARRIVAL_MINUTE = 0
```

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 👨‍💻 Author

<div align="center">

### Harsha Dulshan Kaldera
**MIS Undergraduate | AI Researcher | Entrepreneur**

[![GitHub](https://img.shields.io/badge/GitHub-harshadulshan-0D1117?style=for-the-badge&logo=github&logoColor=white)](https://github.com/harshadulshan)
[![Email](https://img.shields.io/badge/Email-hphdkaldera%40gmail.com-0D1117?style=for-the-badge&logo=gmail&logoColor=00D9FF)](mailto:hphdkaldera@gmail.com)

</div>

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302b63,100:0f0c29&height=120&section=footer&animation=fadeIn"/>

<div align="center">

⭐ **If this project helped you, please give it a star!** ⭐

[![GitHub stars](https://img.shields.io/github/stars/harshadulshan/SmartAttendance?style=social)](https://github.com/harshadulshan/SmartAttendance)

</div>
