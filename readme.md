##### TODO

* [X] รูปเล่ม
* [X] ขั้นตอนการเอา collector ขึ้น gcloud
* [x] ขั้นตอนการทำ backend และการเอาขึ้น
* [x] graph
* [x] feature extraction
* [x] MODEL Train 
* [ ] PREDICTION API
    * [x] เอาข้อมูล distance ลง outbound
    * [x] เอา Model ที่เทรนแล้ว ลงใน base ในรูปแบบ blob
    * [x] เขียน predictionModelPredictor ให้เสร็จ 
        * [x] ดึงข้อมูลจากโมเดลไปใส่ linear regression model
        * [x] ทำนายข้อมูลล่าสุดได้ ได้ผลออกมาเป็น SU (SpeedUncut)
    * [x] เขียน test predictionModelTrainer
    * [ ] เขียน test predictionModelPredictor <---
    * [X] เขียนตัวแปลงจาก SU -> เวลา
    * [ ] เขียน Prediction API
        * [ ] list of segment for each route <---
        * [ ] ดึง DataSet ของทุก segment ใน เส้นทาง
        * [ ] เอา DataSet แต่ละตัวเข้า predictionModelPredictor เพื่อเอา SU ออกมา แล้วแปลงเป็น เวลา
        * [ ] เอาเวลามารวมกันตามเส้นทางที่ต้องผ่านแล้วส่งคืน
* [ ] BACKEND API
* [ ] รูป Visualize
* [ ] redesign โครงให้รองรับ model v2 ได้

##### Question

- Which logic need to be test ?
- Visualize อะไรบ้าง

# Note for remember

##### Input and Output of Model

- input is ...
- output is SU5, SU15, SU30, SU45

https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/#database-models-and-migration
https://medium.com/swlh/visualising-linear-regression-dfac98624d27
