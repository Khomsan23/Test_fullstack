# ขั้นต่อนการรันโปรแกรม #
1.การ create database และ เปิดปิด database server
 -เปิด terminal ของโฟลเดอร์ SQL
 -ทำการ docker-compose up --build 
 -หากต้องการหยุดการทำงานให้ใช้ docker-compose stop postgres
 -สามารถเริ่มการทำงานใหม่ได้โดย docker-compose start postgres

2.ทำการ run API 
 -เปิด terminal ของโฟลเดอร์ server
 -run โดย uvicorn main:app --reload

3.ทำการ run Frontend 
 -เปิด terminal ของโฟลเดอร์ services
 -run โดย npm run serve 