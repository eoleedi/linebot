all:
	git add .
	git commit -m "regular update"
	git push -f heroku master
