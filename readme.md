This is Application Chatbot Healthy for anyone, Devep By Betime Solution Developer Team.

config
    - config.yalm (save all config about embedding or path for data)

explain each folder 

    - config : นี่คือโฟลเดอร์ที่เก็บไฟล์ config ที่ set ค่า paramiter ต่างๆที่ใช่ใน หลายๆที่ใน code หากต้องการเปลี่ยนแปลงค่าบางอย่าง ก็สามารถมาเปลี่ยนที่นี่ได้เลย
    - data :
        - chroma : vector database สร้างจากไฟล์ txt จาก folder data_source
        - data_source : ข้อมูลต่างๆที่อาจจำเป็น เช่น ข้อมูลความรู้ในการลดความอ้วน 
        - data_user : folder สำหรับเก็บข้อมูล user มีทั้งเป็น json และ txt 
    - decision : 
        - semantic_routing : เป็นไฟล์สำหรับใช้งาน LLM ในการตัดสินใจว่าจะ extract ข้อมูลอะไรไหม จาก input ที่ผู้ใช้ส่งมา 
    - embedding : 
        - embedding_data : embedding all data many type of file in to vector databae (chroma folder)
    - flowbot 
        - function_flow : นี่คือ flow การทำงานตั้งแต่ 
            - การสร้างพร้อมท์ 
            - ใส่ memory 
            - ส่งผ่าน input ต่างๆเข้าไปใน LLM
            - RAG 
            ผลลัพธ์ สุดท้ายคือส่งคืนคำตอบกลับมา จากคำถามของผู้ใช้ที่ส่งเข้าไป 
    -  memory 
        - (Coming) : ต้องสร้างคลาสมาบริหารจัดการหน่วยความจำ memory ในการสนทนา รวมไปถึงต้องเก็บข้อความทั้งหมดไว้ใน log หรือ database รวมสักตัวหนึ่ง เพื่อไว้ใช้งานในอนาคต
    -  prompt 
        - promtp_template : คือไฟล์เก็บค่า prompt ทั้งหมดที่ใช้ หรือจะใช้ 
    -  tool 
        - function_tool & custom_tool : คือไฟล์สำหรับการใช้ LLM ในการ extract ข้อมูลที่เราต้องการออกมาจาก input ของผู้ใช้งาน โดย การจะใช้งานฟังก์ชั่นนี้หรือไม่ จะผ่านการตัดสินใจมาจาก class semantic_routing อีกที
    - line_bot
        - เป็น folder ไว้ทดสอบการติดต่อกับ Line API and Dialogflow
    - utils : เป็นโฟลเดอร์ไว้เก็บไฟล์ test หรือไฟล์ทั่วไป ซึ่งตอนนี้ยังไม่มีไฟล์ที่สำคัญๆที่ถูกเรียกใช้งาน
    - app.py : application 
# Thai-Health
