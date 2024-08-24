# คำแนะนำการ Deploy บน Docker

## สิ่งที่ต้องมี
- ตรวจสอบว่าports 8000,8080,5432 ต้องไม่มีการใช้งานอยู่


## ขั้นตอนการ Deploy
1. เปิด terminal ของโฟลเดอร์ CodeTest2

2. ทำการ docker-compose up --build 

3. แอปพลิเคชันควรจะทำงานแล้ว สามารถเข้าถึงได้ที่:
   - หน้าเว็บ (Frontend): http://localhost:8080
   - API สำหรับ Backend: http://localhost:8000
   - ฐานข้อมูล: localhost:5432 (สามารถเข้าถึงได้จากเครื่องโฮสต์)

## การแก้ไขปัญหาเบื้องต้น
- ตรวจสอบ logs: `docker-compose logs`
- รีสตาร์ท services: `docker-compose restart`
- สร้าง services ใหม่: `docker-compose up -d --build`

