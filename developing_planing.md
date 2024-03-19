Finished
1. LLM Decision for Extract Data or not 
2. LLM Extract Data to stucture and unstructur data
3. Embedding for all file in folder to vector Database (and metadata)
4. Chatbot with Instruction Healthy + RAG 
5. Memory Conversation FromScratch 
6. Updata การทำงานให้เข้ากับ UUID หรือก็คือรหัสหลักเฉพาะตัวของแต่ละคนที่เป็นแบบ Personal โดยจะมีข้อมูลส่วนตัวที่เป็น text, vector เป็นโฟลเดอร์ตาม ID นั้นๆ และทำการดึงข้อมูลมาจากเฉพาะ ID นั้นๆ (ตอนนี้ยังเป็น โฟลเดอร์แบบ general อยู่)

Will Doing
1. Update performance RAG with Agent ก็คือตอนนี้เรายัง RAG ในทุกๆรอบของการแชท ขั้นต่อไปของการพัฒนาคือการให้ LLM ช่วยตัดสินว่าว่าจะ RAG ไหม อาจทำเป็น Agen หรือใช้ LLM ธรรมดาก็ได้ (ท่าคล้ายๆ Information Extraction น่ะละนะ)
2. สร้าง database จริงที่เป็น sql และ vector database โดย fix ตาม id 
3. พัฒนา RAG ให้เป็นแบบ Hybride search ตาม personal ID 
4. พัฒนาระบบ Dynamic prompt และ desing Persona Promt from CSV
5. Clean Code and Reveiw Code in Detail all function, method, class and work-flow for improve efficient, undersatnding and easy to maintanant.
6. พัฒนา Multimodal and Multimodal database RAG ()
7. Chain of Table to anaysis transaction data to user 
