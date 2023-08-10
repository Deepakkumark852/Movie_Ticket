# Movie_Ticket

To run the server flask :
 	move to server
 	python install -r requirements.txt
 	python3 app.py
 
 	create another bash terminal for celery worker
 	celery -A app.celery worker -l info
 	sudo systemctl start redis-server
 	
 	create one more bash terminal for celery beat
 	celery -A app.celery beat --max-interval 2  -l info
 	
 	
To run Client Vue3:
	move to client
	npm install
	move to movieserver (cd movieserver)
	npm run dev
	
