from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import logging
from models import NewPartData
# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add-new-part/")
def add_new_part(new_part_data: NewPartData, db: Session = Depends(get_db)):
    return crud.add_new_part(db, new_part_data)


@app.get("/parts-with-times/")
def read_parts_with_times(db: Session = Depends(get_db)):
    try:
        logging.info("Fetching parts with times")
        data = crud.get_parts_with_times(db)
        if data is None:
            logging.warning("No data found")
            raise HTTPException(status_code=404, detail="Data not found")
        logging.info(f"Data retrieved successfully: {data}")
        return data
    except Exception as e:
        logging.error(f"Error in read_parts_with_times: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-excel/")
def download_excel(db: Session = Depends(get_db)):
    try:
        file_path = crud.generate_excel_file(db)
        return FileResponse(file_path, filename=os.path.basename(file_path), headers={
            'Content-Disposition': f'attachment; filename="{os.path.basename(file_path)}"'
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_name = f"uploaded_{file.filename}"
        file_path = os.path.join("uploads", file_name)
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        processed_file_path = crud.process_excel_file(db, file_path)
        
        return {"message": "Excel file uploaded and processed successfully",
                "file_path": processed_file_path}
    except Exception as e:
        logging.error(f"Error in upload_excel: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/times/")
def read_times(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        times = crud.get_times(db, skip=skip, limit=limit)
        if not times:
            raise HTTPException(status_code=404, detail="Times not found")
        return times
    except Exception as e:
        logging.error(f"Error in read_times: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
