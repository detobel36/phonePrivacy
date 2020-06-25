all:
	@echo "TODO"

wifi:
	sudo create_ap/create_ap wlo1 wlo1 -d MyAccessPoint

server:
	cd server
	sudo python3 analyze.py
