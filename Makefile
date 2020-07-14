all:
	@echo "TODO"

wifi:
	sudo create_ap/create_ap wlo1 wlo1 -d MyAccessPoint -g 192.168.12.1

analyze:
	sudo python3 server/analyze.py --phone-ip `./script/getPhoneIp.sh` --local-ip 192.168.12.1

test_phone_1:
	python3 server/analyze.py -f traces/package_init_phone_sony.pcapng -i -p 192.168.12.243

test_phone_2:
	python3 server/analyze.py -f traces/package_init_phone_acer.pcapng -i -p 192.168.12.225
