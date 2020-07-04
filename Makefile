all:
	@echo "TODO"

wifi:
	sudo create_ap/create_ap wlo1 wlo1 -d MyAccessPoint -g 192.168.12.1

analyze:
	sudo python3 server/analyze.py --phone-ip `./script/getPhoneIp.sh` --local-ip 192.168.12.1
